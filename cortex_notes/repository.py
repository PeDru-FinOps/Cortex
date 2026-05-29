from __future__ import annotations

import re
import shutil
from pathlib import Path


class RepositoryError(ValueError):
    pass


ALLOWED_ATTACHMENT_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
ALLOWED_UPLOAD_EXTENSIONS = {".md"} | ALLOWED_ATTACHMENT_EXTENSIONS


class NoteRepository:
    def __init__(self, root: str | Path):
        self.root = Path(root).resolve()

    def ensure_root(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)

    def resolve_note_path(self, relative_path: str) -> Path:
        normalized = relative_path.strip().replace("\\", "/")
        if not normalized:
            raise RepositoryError("Informe o caminho da nota.")
        path_parts = Path(normalized).parts
        if normalized.startswith("/") or Path(normalized).drive or ".." in path_parts:
            raise RepositoryError("Caminho invalido.")
        if not normalized.lower().endswith(".md"):
            normalized = f"{normalized}.md"

        path = (self.root / normalized).resolve()
        if self.root != path and self.root not in path.parents:
            raise RepositoryError("Caminho fora do repositorio de notas.")
        return path

    def resolve_folder_path(self, relative_path: str) -> Path:
        normalized = relative_path.strip().replace("\\", "/")
        if not normalized:
            raise RepositoryError("Informe o caminho da pasta.")
        path_parts = Path(normalized).parts
        if normalized.startswith("/") or Path(normalized).drive or ".." in path_parts:
            raise RepositoryError("Caminho invalido.")
        if Path(normalized).suffix:
            raise RepositoryError("Informe um caminho de pasta, sem extensao de arquivo.")

        path = (self.root / normalized).resolve()
        if self.root != path and self.root not in path.parents:
            raise RepositoryError("Caminho fora do repositorio de notas.")
        return path

    def create_folder(self, relative_path: str) -> str:
        path = self.resolve_folder_path(relative_path)
        path.mkdir(parents=True, exist_ok=True)
        return self.to_relative(path)

    def resolve_existing_folder_path(self, relative_path: str) -> Path:
        normalized = relative_path.strip().replace("\\", "/")
        if not normalized:
            return self.root

        path = self.resolve_folder_path(normalized)
        if not path.exists() or not path.is_dir():
            raise RepositoryError("Pasta de destino nao encontrada.")
        return path

    def write_note(self, relative_path: str, content: str) -> str:
        path = self.resolve_note_path(relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return self.to_relative(path)

    def move_note(self, relative_path: str, target_folder: str) -> str:
        source = self.resolve_note_path(relative_path)
        if not source.exists() or not source.is_file():
            raise RepositoryError("Nota de origem nao encontrada.")

        destination_folder = self.resolve_existing_folder_path(target_folder)
        destination = (destination_folder / source.name).resolve()
        if self.root != destination and self.root not in destination.parents:
            raise RepositoryError("Destino fora do repositorio de notas.")
        if destination == source:
            return self.to_relative(source)
        if destination.exists():
            raise RepositoryError("Ja existe uma nota com esse nome na pasta de destino.")

        source.replace(destination)
        return self.to_relative(destination)

    def rename_note(self, relative_path: str, new_name: str) -> str:
        source = self.resolve_note_path(relative_path)
        if not source.exists() or not source.is_file():
            raise RepositoryError("Nota de origem nao encontrada.")
        old_relative = self.to_relative(source)
        old_stem = source.stem
        normalized_name = new_name.strip().replace("\\", "/")
        if not normalized_name or "/" in normalized_name or Path(normalized_name).drive or ".." in Path(normalized_name).parts:
            raise RepositoryError("Informe apenas o novo nome da nota, sem pasta.")
        if not normalized_name.lower().endswith(".md"):
            normalized_name = f"{normalized_name}.md"
        destination = (source.parent / normalized_name).resolve()
        if self.root != destination and self.root not in destination.parents:
            raise RepositoryError("Destino fora do repositorio de notas.")
        if destination.exists() and destination != source:
            raise RepositoryError("Ja existe uma nota com esse nome.")
        source.replace(destination)
        new_relative = self.to_relative(destination)
        self.update_links_after_rename(old_relative, new_relative, old_stem, destination.stem)
        return new_relative

    def update_links_after_rename(self, old_path: str, new_path: str, old_title: str, new_title: str) -> int:
        changed = 0
        old_path_without_suffix = str(Path(old_path).with_suffix("")).replace("\\", "/")
        new_path_without_suffix = str(Path(new_path).with_suffix("")).replace("\\", "/")
        replacements = {
            old_path: new_path,
            old_path_without_suffix: new_path_without_suffix,
            old_title: new_title,
        }
        for note_path in self.iter_notes():
            content = note_path.read_text(encoding="utf-8")
            updated = replace_wiki_link_targets(content, replacements)
            if updated != content:
                note_path.write_text(updated, encoding="utf-8")
                changed += 1
        return changed

    def delete_note(self, relative_path: str) -> None:
        path = self.resolve_note_path(relative_path)
        if not path.exists() or not path.is_file():
            raise RepositoryError("Nota nao encontrada.")
        path.unlink()

    def delete_folder(self, relative_path: str) -> str:
        path = self.resolve_folder_path(relative_path)
        if path == self.root:
            raise RepositoryError("Nao e possivel apagar a pasta raiz.")
        if not path.exists() or not path.is_dir():
            raise RepositoryError("Pasta nao encontrada.")
        shutil.rmtree(path)
        parent = path.parent
        return "" if parent == self.root else self.to_relative(parent)

    def copy_note(self, relative_path: str) -> str:
        source = self.resolve_note_path(relative_path)
        if not source.exists() or not source.is_file():
            raise RepositoryError("Nota de origem nao encontrada.")
        destination = next_copy_path(source)
        destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        return self.to_relative(destination)

    def append_note_link(self, source_path: str, target_path: str) -> dict[str, str | bool]:
        source = self.read_note(source_path)
        target = self.read_note(target_path)
        link = f"[[{target['title']}]]"
        content = source["content"]
        if link in content or f"[[{target['path']}]]" in content:
            return {"path": source["path"], "link": link, "changed": False}

        content = append_approved_connection_section(content, link)

        self.write_note(source["path"], content)
        return {"path": source["path"], "link": link, "changed": True}

    def approve_connection(self, source_path: str, target_path: str) -> dict:
        forward = self.append_note_link(source_path, target_path)
        reciprocal = self.append_note_link(target_path, source_path)
        return {
            "source": forward,
            "target": reciprocal,
            "changed": bool(forward["changed"] or reciprocal["changed"]),
        }

    def append_tags(self, relative_path: str, tags: list[str]) -> dict:
        note = self.read_note(relative_path)
        normalized = normalize_tags(tags)
        existing = extract_inline_tags(note["content"])
        new_tags = [tag for tag in normalized if tag not in existing]
        if not new_tags:
            return {"path": note["path"], "tags": [], "changed": False}
        content = append_tags_to_content(note["content"], new_tags)
        self.write_note(note["path"], content)
        return {"path": note["path"], "tags": new_tags, "changed": True}

    def import_note_stream(self, relative_path: str, stream) -> str:
        path = self.resolve_upload_path(relative_path)
        if path.suffix.lower() != ".md":
            raise RepositoryError(f"Apenas arquivos .md sao aceitos: {relative_path}")
        return self.import_file_stream(relative_path, stream)

    def import_file_stream(self, relative_path: str, stream) -> str:
        path = self.resolve_upload_path(relative_path)
        data = stream.read()

        if path.suffix.lower() == ".md":
            if isinstance(data, str):
                content = data
            else:
                try:
                    content = data.decode("utf-8-sig")
                except UnicodeDecodeError as error:
                    raise RepositoryError(f"{relative_path} nao esta em UTF-8.") from error

            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            return self.to_relative(path)

        if isinstance(data, str):
            data = data.encode("utf-8")

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return self.to_relative(path)

    def resolve_asset_path(self, relative_path: str) -> Path:
        path = self.resolve_upload_path(relative_path)
        if path.suffix.lower() not in ALLOWED_ATTACHMENT_EXTENSIONS:
            raise RepositoryError("Arquivo nao suportado como imagem.")
        if not path.exists() or not path.is_file():
            raise RepositoryError("Imagem nao encontrada.")
        return path

    def find_attachment(self, target: str, current_note_path: str = "") -> str | None:
        normalized = target.strip().replace("\\", "/")
        if not normalized:
            return None

        candidates = []
        if current_note_path:
            note_folder = Path(current_note_path).parent.as_posix()
            if note_folder and note_folder != ".":
                candidates.append(f"{note_folder}/{normalized}")
        candidates.append(normalized)

        for candidate in candidates:
            try:
                path = self.resolve_asset_path(candidate)
            except RepositoryError:
                continue
            return self.to_relative(path)

        filename = Path(normalized).name.lower()
        matches = [
            path
            for path in self.root.rglob("*")
            if path.is_file()
            and path.suffix.lower() in ALLOWED_ATTACHMENT_EXTENSIONS
            and path.name.lower() == filename
        ]
        if len(matches) == 1:
            return self.to_relative(matches[0])
        return None

    def resolve_upload_path(self, relative_path: str) -> Path:
        normalized = relative_path.strip().replace("\\", "/")
        if not normalized:
            raise RepositoryError("Arquivo sem nome.")

        path_parts = Path(normalized).parts
        if normalized.startswith("/") or Path(normalized).drive or ".." in path_parts:
            raise RepositoryError(f"Caminho invalido no upload: {relative_path}")
        if Path(normalized).suffix.lower() not in ALLOWED_UPLOAD_EXTENSIONS:
            raise RepositoryError(f"Arquivo nao suportado: {relative_path}")

        path = (self.root / normalized).resolve()
        if self.root != path and self.root not in path.parents:
            raise RepositoryError("Caminho fora do repositorio de notas.")
        return path

    def read_note(self, relative_path: str) -> dict[str, str]:
        path = self.resolve_note_path(relative_path)
        if not path.exists() or path.suffix.lower() != ".md":
            raise RepositoryError("Nota nao encontrada.")
        return {
            "path": self.to_relative(path),
            "title": path.stem,
            "content": path.read_text(encoding="utf-8"),
        }

    def iter_notes(self) -> list[Path]:
        self.ensure_root()
        return sorted(path for path in self.root.rglob("*.md") if path.is_file())

    def to_relative(self, path: Path) -> str:
        return path.resolve().relative_to(self.root).as_posix()

    def tree(self) -> dict:
        self.ensure_root()
        return self._folder_node(self.root)

    def _folder_node(self, folder: Path) -> dict:
        children = []
        for child in sorted(folder.iterdir(), key=lambda item: (item.is_file(), item.name.lower())):
            if child.is_dir():
                children.append(self._folder_node(child))
            elif child.suffix.lower() == ".md":
                children.append(
                    {
                        "type": "file",
                        "name": child.name,
                        "path": self.to_relative(child),
                    }
                )

        return {
            "type": "folder",
            "name": folder.name if folder != self.root else self.root.name,
            "path": "" if folder == self.root else self.to_relative(folder),
            "children": children,
        }


def append_approved_connection_section(content: str, link: str) -> str:
    section_pattern = re.compile(r"^## Conex(?:o|õ)es aprovadas\s*$", re.IGNORECASE | re.MULTILINE)
    if section_pattern.search(content):
        return f"{content.rstrip()}\n- {link}\n"

    separator = "\n\n" if content.strip() else ""
    return f"{content.rstrip()}{separator}## Conexoes aprovadas\n\n- {link}\n"


def next_copy_path(source: Path) -> Path:
    stem = source.stem
    suffix = source.suffix
    candidate = source.with_name(f"{stem} - copia{suffix}")
    counter = 2
    while candidate.exists():
        candidate = source.with_name(f"{stem} - copia {counter}{suffix}")
        counter += 1
    return candidate


def replace_wiki_link_targets(content: str, replacements: dict[str, str]) -> str:
    def replace(match: re.Match) -> str:
        raw_target = match.group(1)
        target, separator, alias = raw_target.partition("|")
        stripped = target.strip()
        replacement = replacements.get(stripped)
        if not replacement:
            return match.group(0)
        if separator:
            return f"[[{replacement}|{alias}]]"
        return f"[[{replacement}]]"

    return re.sub(r"\[\[([^\]]+)\]\]", replace, content)


def normalize_tags(tags: list[str]) -> list[str]:
    normalized = []
    seen = set()
    for tag in tags:
        clean = str(tag).strip().lstrip("#").lower()
        clean = re.sub(r"[^a-z0-9_\-/]+", "-", clean).strip("-")
        if clean and clean not in seen:
            seen.add(clean)
            normalized.append(clean)
    return normalized


def extract_inline_tags(content: str) -> set[str]:
    return {match.group(1).lower() for match in re.finditer(r"(?<!\w)#([A-Za-z0-9_\-/]+)", content)}


def append_tags_to_content(content: str, tags: list[str]) -> str:
    normalized = [tag for tag in normalize_tags(tags) if tag not in extract_inline_tags(content)]
    if not normalized:
        return content
    tag_line = " ".join(f"#{tag}" for tag in normalized)
    separator = "\n\n" if content.strip() else ""
    return f"{content.rstrip()}{separator}{tag_line}\n"
