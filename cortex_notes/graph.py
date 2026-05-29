from __future__ import annotations

import re
from pathlib import Path

from cortex_notes.repository import NoteRepository


TAG_PATTERN = re.compile(r"(?<!\w)#([A-Za-z0-9_\-/]+)")
WIKI_LINK_PATTERN = re.compile(r"\[\[([^\]]+)\]\]")


def extract_tags(content: str) -> set[str]:
    return {match.group(1).lower() for match in TAG_PATTERN.finditer(content)}


def extract_wiki_links(content: str) -> set[str]:
    links = set()
    for match in WIKI_LINK_PATTERN.finditer(content):
        target = match.group(1).split("|", 1)[0].strip()
        if target:
            links.add(target)
    return links


def build_graph(repository: NoteRepository) -> dict[str, list[dict]]:
    nodes: dict[str, dict] = {}
    edges: list[dict] = []

    def add_node(node_id: str, label: str, group: str) -> None:
        nodes.setdefault(node_id, {"id": node_id, "label": label, "group": group})

    notes = repository.iter_notes()
    note_lookup = build_note_lookup(repository, notes)

    for note_path in notes:
        relative = repository.to_relative(note_path)
        note_id = f"note:{relative}"
        content = note_path.read_text(encoding="utf-8")
        add_node(note_id, Path(relative).stem, "note")

        tags = extract_tags(content)
        for tag in sorted(tags):
            tag_id = f"tag:{tag}"
            add_node(tag_id, f"#{tag}", "tag")
            edges.append({"source": note_id, "target": tag_id, "type": "tagged"})

        for link in sorted(extract_wiki_links(content)):
            target = resolve_wiki_link(link, note_lookup)
            if target:
                edges.append(
                    {
                        "source": note_id,
                        "target": f"note:{target}",
                        "type": "linked",
                    }
                )

    return {"nodes": list(nodes.values()), "edges": dedupe_edges(edges)}


def build_local_graph(repository: NoteRepository, relative_path: str) -> dict[str, list[dict]]:
    graph = build_graph(repository)
    note_id = f"note:{repository.read_note(relative_path)['path']}"
    local_edges = [
        edge
        for edge in graph["edges"]
        if edge["source"] == note_id or edge["target"] == note_id
    ]
    local_node_ids = {note_id}
    for edge in local_edges:
        local_node_ids.add(edge["source"])
        local_node_ids.add(edge["target"])

    local_nodes = [node for node in graph["nodes"] if node["id"] in local_node_ids]
    return {"nodes": local_nodes, "edges": local_edges, "focus": note_id}


def build_note_lookup(repository: NoteRepository, notes: list[Path]) -> dict[str, str]:
    lookup = {}
    for note_path in notes:
        relative = repository.to_relative(note_path)
        path_without_suffix = str(Path(relative).with_suffix("")).replace("\\", "/")
        stem = Path(relative).stem
        lookup[relative.lower()] = relative
        lookup[path_without_suffix.lower()] = relative
        lookup[stem.lower()] = relative
    return lookup


def resolve_wiki_link(link: str, lookup: dict[str, str]) -> str | None:
    normalized = link.strip().replace("\\", "/")
    candidates = [normalized]
    if not normalized.lower().endswith(".md"):
        candidates.append(f"{normalized}.md")
    return next((lookup.get(candidate.lower()) for candidate in candidates), None)


def dedupe_edges(edges: list[dict]) -> list[dict]:
    seen = set()
    unique = []
    for edge in edges:
        key = (edge["source"], edge["target"], edge["type"])
        if key not in seen:
            seen.add(key)
            unique.append(edge)
    return unique
