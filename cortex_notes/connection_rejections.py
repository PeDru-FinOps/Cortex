from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def reject_connection(root: Path, source: str, target: str, reason: str = "") -> dict[str, Any]:
    data = load_rejections(root)
    key = connection_key(source, target)
    data["rejected"][key] = {
        "source": source,
        "target": target,
        "reason": reason,
    }
    save_rejections(root, data)
    return data["rejected"][key]


def is_rejected(rejections: dict[str, Any], source: str, target: str) -> bool:
    return connection_key(source, target) in rejections.get("rejected", {})


def load_rejections(root: Path) -> dict[str, Any]:
    path = rejections_path(root)
    if not path.exists():
        return {"rejected": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"rejected": {}}
    if not isinstance(data.get("rejected"), dict):
        return {"rejected": {}}
    return data


def save_rejections(root: Path, data: dict[str, Any]) -> None:
    path = rejections_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2), encoding="utf-8")


def rejections_path(root: Path) -> Path:
    return root.parent / ".cortex_intelligence" / "rejected_connections.json"


def connection_key(source: str, target: str) -> str:
    left, right = sorted([source, target])
    return f"{left}|||{right}"
