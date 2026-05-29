from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cortex_notes.repository import NoteRepository


class SyncError(RuntimeError):
    pass


@dataclass(frozen=True)
class LocalNoteFile:
    path: str
    absolute_path: Path
    sha256: str
    size: int


def sync_notes_to_openai(repository: NoteRepository, client=None) -> dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    vector_store_id = os.getenv("OPENAI_VECTOR_STORE_ID", "").strip()
    if not api_key:
        raise SyncError("Configure OPENAI_API_KEY no .env antes de sincronizar.")
    if not vector_store_id:
        raise SyncError("Configure OPENAI_VECTOR_STORE_ID no .env antes de sincronizar.")

    if client is None:
        try:
            from openai import OpenAI
        except ImportError as error:
            raise SyncError("Instale o SDK openai com pip install -r requirements.txt.") from error
        client = OpenAI(api_key=api_key)
    manifest = load_manifest(repository.root, vector_store_id)
    local_files = collect_local_note_files(repository)
    local_by_path = {item.path: item for item in local_files}

    summary = {
        "vector_store_id": vector_store_id,
        "uploaded": [],
        "updated": [],
        "deleted": [],
        "skipped": [],
        "failed": [],
        "total_local": len(local_files),
    }

    for note in local_files:
        previous = manifest["files"].get(note.path)
        if previous and previous.get("sha256") == note.sha256:
            summary["skipped"].append(note.path)
            continue

        if previous:
            delete_remote_file(client, vector_store_id, previous.get("file_id"))

        try:
            uploaded = upload_note(client, vector_store_id, note)
        except Exception as error:  # noqa: BLE001 - returned to UI as per-file sync failure
            summary["failed"].append({"path": note.path, "error": str(error)})
            continue

        manifest["files"][note.path] = {
            "file_id": uploaded["file_id"],
            "vector_store_file_id": uploaded["vector_store_file_id"],
            "sha256": note.sha256,
            "size": note.size,
        }
        if previous:
            summary["updated"].append(note.path)
        else:
            summary["uploaded"].append(note.path)

    for path, remote in list(manifest["files"].items()):
        if path in local_by_path:
            continue
        delete_remote_file(client, vector_store_id, remote.get("file_id"))
        del manifest["files"][path]
        summary["deleted"].append(path)

    save_manifest(repository.root, vector_store_id, manifest)
    return summary


def collect_local_note_files(repository: NoteRepository) -> list[LocalNoteFile]:
    files = []
    for path in repository.iter_notes():
        data = path.read_bytes()
        files.append(
            LocalNoteFile(
                path=repository.to_relative(path),
                absolute_path=path,
                sha256=hashlib.sha256(data).hexdigest(),
                size=len(data),
            )
        )
    return files


def upload_note(client, vector_store_id: str, note: LocalNoteFile) -> dict[str, str]:
    with note.absolute_path.open("rb") as file:
        uploaded_file = client.files.create(
            file=file,
            purpose=os.getenv("OPENAI_FILE_PURPOSE", "assistants"),
        )

    vector_store_file = client.vector_stores.files.create(
        vector_store_id=vector_store_id,
        file_id=uploaded_file.id,
        attributes={
            "cortex_path": note.path[:512],
            "sha256": note.sha256,
            "source": "cortex",
        },
    )
    return {
        "file_id": uploaded_file.id,
        "vector_store_file_id": vector_store_file.id,
    }


def delete_remote_file(client, vector_store_id: str, file_id: str | None) -> None:
    if not file_id:
        return
    try:
        client.vector_stores.files.delete(vector_store_id=vector_store_id, file_id=file_id)
    except Exception:
        pass
    try:
        client.files.delete(file_id)
    except Exception:
        pass


def manifest_path(root: Path, vector_store_id: str) -> Path:
    safe_id = "".join(char if char.isalnum() or char in {"_", "-"} else "_" for char in vector_store_id)
    base = Path(os.getenv("CORTEX_SYNC_ROOT", root.parent / ".cortex_sync"))
    return base / f"openai_vector_store_{safe_id}.json"


def load_manifest(root: Path, vector_store_id: str) -> dict[str, Any]:
    path = manifest_path(root, vector_store_id)
    if not path.exists():
        return {"vector_store_id": vector_store_id, "files": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"vector_store_id": vector_store_id, "files": {}}
    if data.get("vector_store_id") != vector_store_id or not isinstance(data.get("files"), dict):
        return {"vector_store_id": vector_store_id, "files": {}}
    return data


def save_manifest(root: Path, vector_store_id: str, manifest: dict[str, Any]) -> None:
    path = manifest_path(root, vector_store_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, ensure_ascii=True, indent=2), encoding="utf-8")
