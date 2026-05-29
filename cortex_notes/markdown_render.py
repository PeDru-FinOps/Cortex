from __future__ import annotations

import html
import re
from pathlib import Path
from urllib.parse import quote

import markdown

from cortex_notes.graph import TAG_PATTERN, WIKI_LINK_PATTERN, resolve_wiki_link


IMAGE_WIKI_LINK_PATTERN = re.compile(r"!\[\[([^\]]+)\]\]")


def render_markdown(
    content: str,
    note_lookup: dict[str, str],
    image_resolver=None,
) -> str:
    prepared = replace_wiki_images(content, image_resolver)
    prepared = replace_wiki_links(prepared, note_lookup)
    prepared = replace_tags(prepared)
    return markdown.markdown(prepared, extensions=["fenced_code", "tables", "toc"])


def replace_wiki_images(content: str, image_resolver=None) -> str:
    def replacement(match: re.Match) -> str:
        raw = match.group(1)
        target_name, label = split_wiki_link(raw)
        safe_label = html.escape(label)
        asset_path = image_resolver(target_name) if image_resolver else None
        if not asset_path:
            return f'<span class="image-missing">{safe_label}</span>'

        src = f"/assets?path={quote(asset_path)}"
        return f'<img class="note-image" src="{src}" alt="{safe_label}">'

    return IMAGE_WIKI_LINK_PATTERN.sub(replacement, content)


def replace_wiki_links(content: str, note_lookup: dict[str, str]) -> str:
    def replacement(match: re.Match) -> str:
        raw = match.group(1)
        target_name, label = split_wiki_link(raw)
        target_path = resolve_wiki_link(target_name, note_lookup)
        safe_label = html.escape(label)
        if not target_path:
            return f'<span class="wiki-link missing">{safe_label}</span>'

        href = f"/?path={quote(target_path)}&mode=read"
        return f'<a class="wiki-link" href="{href}">{safe_label}</a>'

    return WIKI_LINK_PATTERN.sub(replacement, content)


def replace_tags(content: str) -> str:
    def replacement(match: re.Match) -> str:
        tag = match.group(1)
        safe_tag = html.escape(tag)
        return f'<span class="tag-label">#{safe_tag}</span>'

    return TAG_PATTERN.sub(replacement, content)


def split_wiki_link(raw: str) -> tuple[str, str]:
    target, _, alias = raw.partition("|")
    target = target.strip()
    label = alias.strip() or Path(target).stem or target
    return target, label
