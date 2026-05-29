from __future__ import annotations

from pathlib import Path


class RepositoryError(ValueError):
    pass


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

    def delete_note(self, relative_path: str) -> None:
        path = self.resolve_note_path(relative_path)
        if not path.exists() or not path.is_file():
            raise RepositoryError("Nota nao encontrada.")
        path.unlink()

    def import_note_stream(self, relative_path: str, stream) -> str:
        path = self.resolve_upload_path(relative_path)
        data = stream.read()
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

    def resolve_upload_path(self, relative_path: str) -> Path:
        normalized = relative_path.strip().replace("\\", "/")
        if not normalized:
            raise RepositoryError("Arquivo sem nome.")

        path_parts = Path(normalized).parts
        if normalized.startswith("/") or Path(normalized).drive or ".." in path_parts:
            raise RepositoryError(f"Caminho invalido no upload: {relative_path}")
        if Path(normalized).suffix.lower() != ".md":
            raise RepositoryError(f"Apenas arquivos .md sao aceitos: {relative_path}")

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
