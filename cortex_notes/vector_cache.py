from __future__ import annotations

import json
import os
import re
import time
from collections import Counter
from pathlib import Path
from typing import Any


TOKEN_PATTERN = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9][A-Za-zÀ-ÖØ-öø-ÿ0-9_-]{2,}")


class VectorCacheError(RuntimeError):
    pass


def read_openai_vector_store_to_cache(root: Path, progress=None, client=None, force: bool = False) -> dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    vector_store_id = os.getenv("OPENAI_VECTOR_STORE_ID", "").strip()
    if not api_key:
        raise VectorCacheError("Configure OPENAI_API_KEY no .env antes de ler o Vector Store.")
    if not vector_store_id:
        raise VectorCacheError("Configure OPENAI_VECTOR_STORE_ID no .env antes de ler o Vector Store.")

    existing_summary = cache_summary(load_vector_cache(root))
    if existing_summary.get("usable") and not force:
        report(progress, "cached", "Cache utilizavel ja existe; leitura remota ignorada para economizar custo.", 0, 0)
        existing_summary["reused"] = True
        return existing_summary

    if client is None:
        try:
            from openai import OpenAI
        except ImportError as error:
            raise VectorCacheError("Instale o SDK openai com pip install -r requirements.txt.") from error
        client = OpenAI(api_key=api_key)

    report(progress, "listing", "Listando arquivos do Vector Store.", 0, 0)
    vector_files = list(client.vector_stores.files.list(vector_store_id=vector_store_id, limit=100))
    total = len(vector_files)
    max_chars = int(os.getenv("CORTEX_VECTOR_CACHE_FILE_CHARS", "12000"))

    documents = []
    for index, vector_file in enumerate(vector_files, start=1):
        file_id = vector_file_openai_file_id(vector_file)
        filename = file_id
        report(progress, "reading", f"Lendo conteudo indexado {index}/{total}: {file_id}", index - 1, total)
        try:
            file_object = client.files.retrieve(file_id)
            filename = getattr(file_object, "filename", file_id)
            content = client.vector_stores.files.content(
                file_id=file_id,
                vector_store_id=vector_store_id,
            )
            text = vector_file_content_to_text(content)
        except Exception as error:  # noqa: BLE001 - cache read should keep partial progress
            documents.append(
                {
                    "file_id": file_id,
                    "filename": filename,
                    "text": "",
                    "error": str(error),
                }
            )
            continue

        if not text:
            documents.append(
                {
                    "file_id": file_id,
                    "filename": filename,
                    "text": "",
                    "error": "Nenhum conteudo indexado retornado para este arquivo.",
                }
            )
            report(progress, "reading", f"Sem conteudo indexado {index}/{total}: {filename}", index, total)
            continue

        documents.append(
            {
                "file_id": file_id,
                "filename": filename,
                "text": text[:max_chars],
                "truncated": len(text) > max_chars,
                "cache_mode": "vector_file_content",
            }
        )
        report(progress, "reading", f"Conteudo cacheado {index}/{total}: {filename}", index, total)

    cache = {
        "vector_store_id": vector_store_id,
        "created_at": time.time(),
        "document_count": len(documents),
        "documents": documents,
        "cache_mode": "vector_file_content",
    }
    save_vector_cache(root, cache)
    usable = len([document for document in documents if document.get("text")])
    if usable:
        report(progress, "done", f"Vector Store lido: {usable}/{total} arquivos com trechos em cache.", total, total)
    else:
        report(progress, "done", "Cache criado, mas nenhum texto utilizavel foi recuperado do Vector Store.", total, total)
    return cache_summary(cache)


def load_vector_cache(root: Path) -> dict[str, Any] | None:
    path = vector_cache_path(root)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def save_vector_cache(root: Path, cache: dict[str, Any]) -> None:
    path = vector_cache_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cache, ensure_ascii=True), encoding="utf-8")


def vector_cache_path(root: Path) -> Path:
    base = root.parent if root.name == "notes" else root
    return base / ".cortex_vector_cache" / "openai_vector_store.json"


def cache_summary(cache: dict[str, Any] | None) -> dict[str, Any]:
    if not cache:
        return {"available": False}
    documents = cache.get("documents", [])
    documents_with_text = len([item for item in documents if item.get("text")])
    documents_with_errors = len([item for item in documents if item.get("error")])
    return {
        "available": True,
        "usable": documents_with_text > 0,
        "vector_store_id": cache.get("vector_store_id", ""),
        "created_at": cache.get("created_at"),
        "document_count": cache.get("document_count", 0),
        "documents_with_text": documents_with_text,
        "documents_with_errors": documents_with_errors,
        "cache_mode": cache.get("cache_mode", ""),
    }


def search_vector_cache(root: Path, query: str, limit: int = 8) -> list[dict]:
    cache = load_vector_cache(root)
    if not cache:
        return []

    query_terms = tokenize(query)
    scored = []
    for document in cache.get("documents", []):
        text = document.get("text", "")
        if not text:
            continue
        terms = tokenize(f"{document.get('filename', '')} {text}")
        score = overlap_score(query_terms, terms)
        if score > 0:
            scored.append((score, document))

    if not scored and cache.get("documents"):
        scored = [(0.01, document) for document in cache["documents"] if document.get("text")]

    scored.sort(key=lambda item: item[0], reverse=True)
    return [
        {
            "path": document.get("filename", document.get("file_id", "vector-cache")),
            "title": Path(document.get("filename", "vector-cache")).stem,
            "score": round(score, 4),
            "excerpt": excerpt(document.get("text", ""), query_terms),
            "source": "openai-vector-cache",
            "file_id": document.get("file_id", ""),
        }
        for score, document in scored[:limit]
    ]


def response_to_text(response) -> str:
    if hasattr(response, "text"):
        value = response.text
        return value() if callable(value) else str(value)
    if hasattr(response, "read"):
        data = response.read()
    elif hasattr(response, "content"):
        data = response.content
    else:
        data = bytes(response)
    if isinstance(data, str):
        return data
    return data.decode("utf-8", errors="replace")


def vector_file_content_to_text(content) -> str:
    pages = getattr(content, "data", content)
    parts = []
    for item in pages:
        text = getattr(item, "text", "")
        if text:
            parts.append(str(text))
    return "\n\n".join(parts).strip()


def vector_file_openai_file_id(vector_file) -> str:
    if hasattr(vector_file, "model_dump"):
        raw = vector_file.model_dump()
        file_id = raw.get("file_id") or raw.get("id")
        if file_id:
            return str(file_id)
    return str(getattr(vector_file, "file_id", "") or getattr(vector_file, "id", ""))


def build_file_cache_query(filename: str) -> str:
    stem = Path(filename).stem
    return (
        f"{filename}\n{stem}\n"
        "Recupere os trechos mais representativos deste arquivo: conceitos centrais, decisoes, exemplos, "
        "relacoes com outros temas, procedimentos e conclusoes."
    )


def matching_snippets(results: list[Any], file_ref: dict[str, str]) -> list[str]:
    matched = []
    fallback = []
    for item in results:
        text = vector_result_text(item)
        if not text:
            continue
        fallback.append(text)
        if vector_result_matches_file(item, file_ref):
            matched.append(text)
    return unique_snippets(matched or fallback[:1])


def vector_result_matches_file(item, file_ref: dict[str, str]) -> bool:
    result_file_id = str(getattr(item, "file_id", "") or "")
    result_filename = str(getattr(item, "filename", "") or "")
    expected_file_id = str(file_ref.get("file_id", ""))
    expected_filename = str(file_ref.get("filename", ""))
    return bool(
        result_file_id and result_file_id == expected_file_id
        or result_filename and result_filename == expected_filename
    )


def vector_result_text(item) -> str:
    content = getattr(item, "content", []) or []
    parts = []
    for part in content:
        text = getattr(part, "text", "")
        if text:
            parts.append(str(text))
    return "\n".join(parts).strip()


def unique_snippets(snippets: list[str]) -> list[str]:
    seen = set()
    unique = []
    for snippet in snippets:
        clean = " ".join(snippet.split())
        if not clean or clean in seen:
            continue
        seen.add(clean)
        unique.append(snippet)
    return unique


def tokenize(text: str) -> Counter:
    return Counter(match.group(0).lower() for match in TOKEN_PATTERN.finditer(text))


def overlap_score(query_terms: Counter, document_terms: Counter) -> float:
    if not query_terms or not document_terms:
        return 0.0
    shared = set(query_terms) & set(document_terms)
    return sum(min(query_terms[term], document_terms[term]) for term in shared) / max(1, sum(query_terms.values()))


def excerpt(text: str, query_terms: Counter, size: int = 700) -> str:
    clean = " ".join(text.split())
    if len(clean) <= size:
        return clean
    positions = [clean.lower().find(term) for term in query_terms if clean.lower().find(term) >= 0]
    start = max(0, min(positions) - 120) if positions else 0
    return f"{'...' if start else ''}{clean[start:start + size].strip()}..."


def report(callback, phase: str, message: str, completed: int, total: int) -> None:
    if callback:
        callback(phase, message, completed, total)
