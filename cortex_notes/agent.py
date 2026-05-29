from __future__ import annotations

import math
import os
import re
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from cortex_notes.graph import build_note_lookup, extract_tags, extract_wiki_links, resolve_wiki_link
from cortex_notes.repository import NoteRepository, RepositoryError
from cortex_notes.vector_cache import cache_summary, load_vector_cache, search_vector_cache
from cortex_notes.writing_learning import load_private_security_skills, load_private_writing_skills


TOKEN_PATTERN = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9][A-Za-zÀ-ÖØ-öø-ÿ0-9_-]{2,}")
HEADING_PATTERN = re.compile(r"^#{1,6}\s+(.+)$", re.MULTILINE)
CHUNK_SIZE = 900
CHUNK_OVERLAP = 140

STOPWORDS = {
    "ainda",
    "algo",
    "aqui",
    "cada",
    "como",
    "com",
    "das",
    "dos",
    "de",
    "da",
    "do",
    "e",
    "ela",
    "ele",
    "eles",
    "em",
    "entre",
    "essa",
    "esse",
    "esta",
    "este",
    "isso",
    "mais",
    "mas",
    "mesmo",
    "muito",
    "nao",
    "nas",
    "nos",
    "para",
    "pela",
    "pelo",
    "por",
    "que",
    "quando",
    "sao",
    "sem",
    "ser",
    "seu",
    "sua",
    "tambem",
    "tem",
    "uma",
    "uns",
    "ver",
    "voce",
}


@dataclass(frozen=True)
class NoteDocument:
    path: str
    title: str
    content: str
    tags: set[str]
    links: set[str]
    terms: Counter


@dataclass(frozen=True)
class RagChunk:
    id: str
    path: str
    title: str
    text: str
    terms: Counter


class CortexAgent:
    def __init__(self, repository: NoteRepository):
        self.repository = repository
        self.documents = self._load_documents()
        self.chunks = self._build_chunks()
        self.idf = self._build_idf()
        self.document_vectors = {
            document.path: self._weighted_vector(document.terms)
            for document in self.documents
        }

    def run(self, query: str = "", focus_path: str = "", use_openai_search: bool = True) -> dict:
        focus = self._read_focus(focus_path) if focus_path else None
        retrieval_query = self._retrieval_query(query, focus)
        context = self.search(
            retrieval_query,
            focus_path=focus.path if focus else "",
            limit=8,
            use_openai_search=use_openai_search,
        )
        focus_documents = self._documents_for_context(context, focus)

        return {
            "query": query,
            "focus": self._focus_payload(focus),
            "context": context,
            "synthesis": self._synthesize(query, focus_documents, context),
            "patterns": self._patterns(focus_documents),
            "implicit_relations": self._implicit_relations(focus_documents, limit=6),
            "hypotheses": self._hypotheses(focus_documents),
            "next_questions": self._next_questions(query, focus_documents),
        }

    def chat(self, message: str, focus_path: str = "") -> dict:
        base = self.run(query=message, focus_path=focus_path)
        try:
            llm_answer = self._generate_llm_answer(message, base)
        except Exception as error:  # noqa: BLE001 - surfaced as graceful local fallback
            llm_answer = None
            base["llm_error"] = str(error)
        if llm_answer:
            base["answer"] = llm_answer["answer"]
            base["llm"] = llm_answer
            return base

        base["answer"] = self._fallback_answer(base)
        base["llm"] = {
            "enabled": False,
            "provider": "local",
            "model": "tf-idf",
            "reason": base.get("llm_error") or "OPENAI_API_KEY ausente ou SDK OpenAI indisponivel.",
        }
        return base

    def recommend_connections(
        self,
        focus_path: str = "",
        limit: int = 12,
        rejected_pairs: set[tuple[str, str]] | None = None,
    ) -> dict:
        focus = self._read_focus(focus_path) if focus_path else None
        if focus:
            context = self.search(self._retrieval_query("", focus), focus_path=focus.path, limit=10)
            documents = self._documents_for_context(context, focus)
        else:
            context = []
            documents = self.documents

        relations = self._implicit_relations(documents, limit=max(limit * 2, limit))
        rejected_pairs = rejected_pairs or set()
        relations = [
            relation
            for relation in relations
            if canonical_pair(relation["source"], relation["target"]) not in rejected_pairs
        ]
        relations = self._review_connection_candidates(relations[:limit], limit=limit)
        existing_links = {
            (left.path, target)
            for left in self.documents
            for target in left.links
        }
        enriched = []
        for relation in relations:
            enriched.append(
                {
                    **relation,
                    "metadata": {
                        "type": "implicit",
                        "confidence": confidence_label(relation["score"]),
                        "recommended_link": f"[[{Path(relation['target']).stem}]]",
                        "already_linked": (
                            (relation["source"], relation["target"]) in existing_links
                            or (relation["target"], relation["source"]) in existing_links
                        ),
                    },
                }
            )

        return {
            "focus": self._focus_payload(focus),
            "context": context,
            "recommendations": enriched,
        }

    def write_content(self, kind: str, theme: str = "", focus_path: str = "", progress=None) -> dict:
        kind = normalize_write_kind(kind)
        focus = self._read_focus(focus_path) if focus_path else None
        query = theme.strip() or (focus.title if focus else "")
        report_progress(progress, "reading_cache", "Buscando contexto no cache do Vector Store.")
        cached_context = search_vector_cache(self.repository.root, query, limit=10)
        if cached_context:
            report_progress(progress, "reading_cache", f"Cache utilizavel encontrado: {len(cached_context)} trechos recuperados.")
            base = {
                "query": query,
                "focus": self._focus_payload(focus),
                "context": cached_context,
                "synthesis": self._synthesize(query, [], cached_context),
                "patterns": [],
                "implicit_relations": [],
                "hypotheses": [],
                "next_questions": [],
            }
        else:
            summary = cache_summary(load_vector_cache(self.repository.root))
            if summary.get("available") and not summary.get("usable"):
                message = (
                    "Cache existe, mas nao contem texto utilizavel; "
                    "montando briefing local rapido a partir das notas."
                )
            elif summary.get("available"):
                message = (
                    "Cache existe, mas nao retornou trechos para este pedido; "
                    "montando briefing local rapido a partir das notas."
                )
            else:
                message = "Cache ausente; montando briefing local rapido a partir das notas."
            report_progress(progress, "retrieving", message)
            base = self.run(
                query=query,
                focus_path=focus.path if focus else "",
                use_openai_search=False,
            )
        report_progress(progress, "skill", "Carregando skill de escrita.")
        skill = self._writing_skill(kind)
        llm_error = ""
        try:
            report_progress(progress, "llm", "Enviando contexto lido/cacheado e instrucoes para a OpenAI.")
            llm_answer = self._generate_writing_answer(kind, theme, skill, base)
        except Exception as error:  # noqa: BLE001 - writing must not leave UI stuck
            llm_answer = None
            llm_error = str(error)
        if llm_answer:
            report_progress(progress, "done", "Texto gerado pela OpenAI.")
            return {
                "kind": kind,
                "theme": theme,
                "skill": skill["path"],
                "context": base["context"],
                "content": llm_answer["answer"],
                "llm": llm_answer,
            }

        report_progress(progress, "fallback", "Gerando fallback local porque a LLM nao respondeu.")
        return {
            "kind": kind,
            "theme": theme,
            "skill": skill["path"],
            "context": base["context"],
            "content": self._fallback_writing_content(kind, theme, base),
            "llm": {
                "enabled": False,
                "provider": "local",
                "model": "tf-idf",
                "reason": llm_error or "OPENAI_API_KEY ausente ou SDK OpenAI indisponivel.",
            },
        }

    def search(
        self,
        query: str,
        focus_path: str = "",
        limit: int = 8,
        use_openai_search: bool = True,
    ) -> list[dict]:
        if use_openai_search and self._uses_openai_vector_store():
            cached_results = search_vector_cache(self.repository.root, query, limit=limit)
            if cached_results:
                return cached_results
            if self._allows_live_vector_search():
                results = self._search_openai_vector_store(query, limit)
                if results:
                    return results

        return self._search_local(query, focus_path=focus_path, limit=limit)

    def _search_local(self, query: str, focus_path: str = "", limit: int = 8) -> list[dict]:
        query_terms = tokenize(query)
        if not query_terms and focus_path:
            focus = self._document_by_path(focus_path)
            query_terms = focus.terms if focus else Counter()
        if not query_terms:
            query_terms = Counter(
                term
                for document in self.documents
                for term, count in document.terms.items()
                for _ in range(min(count, 2))
            )

        query_vector = self._weighted_vector(query_terms)
        scored = []
        for chunk in self.chunks:
            score = cosine_similarity(query_vector, self._weighted_vector(chunk.terms))
            if focus_path and chunk.path == focus_path:
                score += 0.08
            if score > 0:
                scored.append((score, chunk))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [
            {
                "path": chunk.path,
                "title": chunk.title,
                "score": round(score, 4),
                "excerpt": excerpt(chunk.text, query_terms),
                "source": "local-tfidf",
            }
            for score, chunk in scored[:limit]
        ]

    def _uses_openai_vector_store(self) -> bool:
        backend = os.getenv("CORTEX_VECTOR_STORE", "tfidf").strip().lower()
        return backend == "openai" and bool(os.getenv("OPENAI_VECTOR_STORE_ID", "").strip())

    def _allows_live_vector_search(self) -> bool:
        return os.getenv("CORTEX_ALLOW_LIVE_VECTOR_SEARCH", "0").strip().lower() in {"1", "true", "yes", "sim"}

    def _search_openai_vector_store(self, query: str, limit: int) -> list[dict]:
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        vector_store_id = os.getenv("OPENAI_VECTOR_STORE_ID", "").strip()
        if not api_key or not vector_store_id:
            return []

        try:
            from openai import OpenAI
        except ImportError:
            return []

        client = OpenAI(api_key=api_key)
        response = client.vector_stores.search(
            vector_store_id=vector_store_id,
            query=query or "Analise o conteudo mais relevante do Cortex.",
            max_num_results=limit,
        )
        return [vector_store_result_to_context(item) for item in response.data]

    def _load_documents(self) -> list[NoteDocument]:
        notes = self.repository.iter_notes()
        lookup = build_note_lookup(self.repository, notes)
        documents = []
        for path in notes:
            relative = self.repository.to_relative(path)
            content = path.read_text(encoding="utf-8")
            links = {
                resolved
                for link in extract_wiki_links(content)
                if (resolved := resolve_wiki_link(link, lookup))
            }
            documents.append(
                NoteDocument(
                    path=relative,
                    title=Path(relative).stem,
                    content=content,
                    tags=extract_tags(content),
                    links=links,
                    terms=tokenize(f"{Path(relative).stem} {content}"),
                )
            )
        return documents

    def _build_chunks(self) -> list[RagChunk]:
        chunks = []
        for document in self.documents:
            for index, chunk_text in enumerate(split_markdown(document.content)):
                chunks.append(
                    RagChunk(
                        id=f"{document.path}#{index}",
                        path=document.path,
                        title=document.title,
                        text=chunk_text,
                        terms=tokenize(f"{document.title} {chunk_text}"),
                    )
                )
        return chunks

    def _build_idf(self) -> dict[str, float]:
        total = max(1, len(self.chunks))
        appearances = Counter()
        for chunk in self.chunks:
            appearances.update(chunk.terms.keys())
        return {
            term: math.log((1 + total) / (1 + count)) + 1
            for term, count in appearances.items()
        }

    def _weighted_vector(self, terms: Counter) -> dict[str, float]:
        if not terms:
            return {}
        max_frequency = max(terms.values())
        return {
            term: (count / max_frequency) * self.idf.get(term, 1.0)
            for term, count in terms.items()
        }

    def _read_focus(self, focus_path: str) -> NoteDocument:
        note = self.repository.read_note(focus_path)
        return self._document_by_path(note["path"]) or NoteDocument(
            path=note["path"],
            title=note["title"],
            content=note["content"],
            tags=extract_tags(note["content"]),
            links=set(),
            terms=tokenize(note["content"]),
        )

    def _document_by_path(self, path: str) -> NoteDocument | None:
        return next((document for document in self.documents if document.path == path), None)

    def _retrieval_query(self, query: str, focus: NoteDocument | None) -> str:
        if query.strip():
            return query
        if focus:
            headings = " ".join(HEADING_PATTERN.findall(focus.content))
            common_terms = " ".join(term for term, _ in focus.terms.most_common(18))
            return f"{focus.title} {headings} {common_terms}"
        return " ".join(term for document in self.documents for term, _ in document.terms.most_common(5))

    def _documents_for_context(self, context: list[dict], focus: NoteDocument | None) -> list[NoteDocument]:
        ordered_paths = []
        if focus:
            ordered_paths.append(focus.path)
        for item in context:
            if item["path"] not in ordered_paths:
                ordered_paths.append(item["path"])
        return [
            document
            for path in ordered_paths
            if (document := self._document_by_path(path))
        ]

    def _focus_payload(self, focus: NoteDocument | None) -> dict | None:
        if not focus:
            return None
        return {"path": focus.path, "title": focus.title, "tags": sorted(focus.tags)}

    def _synthesize(self, query: str, documents: list[NoteDocument], context: list[dict]) -> str:
        if not documents and context:
            titles = ", ".join(item["title"] for item in context[:4])
            signals = ", ".join(top_terms_from_context(context, 8))
            intent = query.strip() or "a nota atual"
            return (
                f"Para {intent}, o Vector Store retornou contexto em {titles}. "
                f"Os sinais mais fortes nos trechos recuperados sao: {signals}. "
                "Esta sintese e local: ela resume os resultados recuperados antes da resposta da LLM."
            )

        if not documents:
            return "Nao encontrei contexto suficiente no Cortex para gerar uma sintese."

        top_terms = top_terms_for(documents, 8)
        titles = ", ".join(document.title for document in documents[:4])
        intent = query.strip() or "a nota atual"
        return (
            f"Para {intent}, o Cortex aponta para um nucleo formado por {titles}. "
            f"Os sinais mais fortes sao: {', '.join(top_terms)}. "
            "A leitura combinada sugere procurar nao apenas respostas isoladas, mas dependencias "
            "entre conceitos, procedimentos e decisoes recorrentes."
        )

    def _patterns(self, documents: list[NoteDocument]) -> list[dict]:
        tag_counter = Counter(tag for document in documents for tag in document.tags)
        folder_counter = Counter(document.path.split("/", 1)[0] for document in documents)
        term_counter = aggregate_terms(documents)

        patterns = []
        if tag_counter:
            patterns.append(
                {
                    "title": "Tags recorrentes",
                    "detail": ", ".join(f"#{tag}" for tag, _ in tag_counter.most_common(6)),
                }
            )
        if folder_counter:
            patterns.append(
                {
                    "title": "Areas mais presentes",
                    "detail": ", ".join(area for area, _ in folder_counter.most_common(5)),
                }
            )
        if term_counter:
            patterns.append(
                {
                    "title": "Vocabulos dominantes",
                    "detail": ", ".join(term for term, _ in term_counter.most_common(10)),
                }
            )
        return patterns

    def _implicit_relations(self, documents: list[NoteDocument], limit: int) -> list[dict]:
        candidate_paths = {document.path for document in documents}
        if len(candidate_paths) < 2:
            candidate_paths = {document.path for document in self.documents}

        relations = []
        selected = [document for document in self.documents if document.path in candidate_paths]
        for index, left in enumerate(selected):
            for right in selected[index + 1 :]:
                if right.path in left.links or left.path in right.links:
                    continue
                shared_tags = left.tags & right.tags
                shared_terms = meaningful_shared_terms(left, right)
                similarity = cosine_similarity(
                    self.document_vectors.get(left.path, {}),
                    self.document_vectors.get(right.path, {}),
                )
                score = similarity * 0.78 + min(len(shared_terms), 12) * 0.022 + len(shared_tags) * 0.012
                if score >= 0.14:
                    relations.append(
                        {
                            "source": left.path,
                            "target": right.path,
                            "score": round(score, 4),
                            "reason": relation_reason(left, right, shared_tags, shared_terms, similarity),
                            "evidence": connection_evidence(left, right, shared_terms),
                        }
                    )

        relations.sort(key=lambda item: item["score"], reverse=True)
        return relations[:limit]

    def _review_connection_candidates(self, relations: list[dict], limit: int) -> list[dict]:
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key or not relations:
            return relations[:limit]

        try:
            from openai import OpenAI
        except ImportError:
            return relations[:limit]

        model = os.getenv("OPENAI_MODEL", "gpt-5.2").strip() or "gpt-5.2"
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=model,
            instructions=with_private_security_skills(
                "Voce avalia conexoes entre notas de um segundo cerebro. "
                "Nao aprove conexoes apenas por tags iguais. Priorize relacao conceitual, dependencia operacional, "
                "causa e efeito, continuidade de processo, contradicao ou oportunidade de sintese. "
                "Responda somente JSON valido."
            ),
            input=build_connection_review_prompt(relations),
            max_output_tokens=1400,
        )
        reviewed = parse_connection_review(response.output_text)
        if not reviewed:
            return relations[:limit]

        by_pair = {canonical_pair(item["source"], item["target"]): item for item in relations}
        approved = []
        for item in reviewed:
            source = item.get("source", "")
            target = item.get("target", "")
            original = by_pair.get(canonical_pair(source, target))
            if not original or item.get("keep") is False:
                continue
            score = item.get("score", original["score"])
            try:
                score = float(score)
            except (TypeError, ValueError):
                score = original["score"]
            approved.append(
                {
                    **original,
                    "score": round(score, 4),
                    "reason": str(item.get("reason") or original["reason"]),
                    "analysis": str(item.get("analysis") or ""),
                    "connection_type": str(item.get("connection_type") or "conceitual"),
                }
            )

        approved.sort(key=lambda item: item["score"], reverse=True)
        return approved[:limit] or relations[:limit]

    def _hypotheses(self, documents: list[NoteDocument]) -> list[str]:
        if not documents:
            return []

        folders = Counter(document.path.split("/", 1)[0] for document in documents)
        terms = top_terms_for(documents, 6)
        hypotheses = [
            (
                "Se estes conteudos forem estudados juntos, pode existir um modelo reutilizavel "
                f"em torno de {', '.join(terms[:3])}."
            )
        ]
        if len(folders) > 1:
            areas = ", ".join(area for area, _ in folders.most_common(3))
            hypotheses.append(
                f"Ha uma ponte potencial entre {areas}; talvez uma nota de sintese reduza conhecimento disperso."
            )
        if any(document.tags for document in documents):
            hypotheses.append(
                "As tags indicam trilhas tematicas que podem virar indices curados ou playbooks."
            )
        return hypotheses[:4]

    def _next_questions(self, query: str, documents: list[NoteDocument]) -> list[str]:
        terms = top_terms_for(documents, 5)
        if not terms:
            return ["Que pergunta central esta por tras desta busca?"]
        return [
            f"O que muda se {terms[0]} for tratado como criterio de decisao?",
            f"Quais notas contradizem ou limitam a leitura sobre {terms[1] if len(terms) > 1 else terms[0]}?",
            "Qual seria a menor nota de sintese capaz de conectar estes contextos?",
        ]

    def _generate_llm_answer(self, message: str, base: dict) -> dict | None:
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            return None

        try:
            from openai import OpenAI
        except ImportError:
            return None

        model = os.getenv("OPENAI_MODEL", "gpt-5.2").strip() or "gpt-5.2"
        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model=model,
            instructions=with_private_security_skills(
                "Voce e a agente de inteligencia do Cortex, um segundo cerebro em Markdown. "
                "Responda em portugues do Brasil. Use apenas o contexto recuperado como base factual. "
                "Raciocine conectando informacoes, identificando padroes, hipoteses, relacoes implicitas "
                "e proximos passos. Quando houver incerteza, diga que e uma hipotese."
            ),
            input=build_llm_prompt(message, base),
            max_output_tokens=int(os.getenv("OPENAI_MAX_OUTPUT_TOKENS", "1200")),
        )
        return {
            "enabled": True,
            "provider": "openai",
            "model": model,
            "vector_store": os.getenv("OPENAI_VECTOR_STORE_ID", "").strip() or None,
            "answer": response.output_text,
        }

    def _generate_writing_answer(self, kind: str, theme: str, skill: dict, base: dict) -> dict | None:
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            return None

        try:
            from openai import OpenAI
        except ImportError:
            return None

        model = os.getenv("OPENAI_MODEL", "gpt-5.2").strip() or "gpt-5.2"
        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model=model,
            instructions=with_private_security_skills(
                "Voce e a agente de escrita do Cortex. Use a skill fornecida como norma de estilo, "
                "estrutura e criterio de qualidade. Use o contexto recuperado do Cortex como base factual. "
                "Responda em portugues do Brasil. Nao invente fatos especificos que nao estejam no contexto; "
                "quando fizer inferencias, sinalize como inferencia ou hipotese."
            ),
            input=build_writing_prompt(kind, theme, skill, base),
            max_output_tokens=int(os.getenv("OPENAI_WRITING_MAX_OUTPUT_TOKENS", "2400")),
        )
        return {
            "enabled": True,
            "provider": "openai",
            "model": model,
            "vector_store": os.getenv("OPENAI_VECTOR_STORE_ID", "").strip() or None,
            "answer": response.output_text,
        }

    def _fallback_answer(self, base: dict) -> str:
        sections = [base.get("synthesis", "")]
        hypotheses = base.get("hypotheses") or []
        if hypotheses:
            sections.append("Hipoteses:\n" + "\n".join(f"- {item}" for item in hypotheses))
        next_questions = base.get("next_questions") or []
        if next_questions:
            sections.append("Proximas perguntas:\n" + "\n".join(f"- {item}" for item in next_questions))
        return "\n\n".join(section for section in sections if section)

    def _writing_skill(self, kind: str) -> dict:
        if kind == "linkedin":
            paths = ["IA/Skills/linkedin_posts_skill.md"]
        elif kind == "article":
            paths = ["IA/Skills/newsletter_skill.md", "IA/Skills/seo_skill.md"]
        else:
            paths = ["IA/Skills/newsletter_skill.md", "IA/Skills/seo_skill.md"]

        contents = []
        existing_paths = []
        for path in paths:
            try:
                note = self.repository.read_note(path)
            except RepositoryError:
                continue
            contents.append(note["content"])
            existing_paths.append(note["path"])
        for private_skill in load_private_writing_skills():
            contents.append(private_skill["content"])
            existing_paths.append(private_skill["path"])
        return {
            "path": ", ".join(existing_paths) if existing_paths else "fallback-local",
            "content": "\n\n---\n\n".join(contents),
        }

    def _fallback_writing_content(self, kind: str, theme: str, base: dict) -> str:
        title = theme.strip() or "Tema sugerido pelo Cortex"
        context = "\n".join(f"- {item['path']}: {item['excerpt']}" for item in base.get("context", [])[:5])
        if kind == "linkedin":
            return (
                f"Objetivo da postagem: autoridade tecnica\n\n"
                f"Postagem completa:\n\n{title}\n\n"
                "O Cortex encontrou sinais relevantes neste tema, mas a LLM nao esta configurada. "
                "Use os pontos abaixo como briefing para escrever a postagem:\n\n"
                f"{context}"
            )
        return (
            f"# {title}\n\n"
            "A LLM nao esta configurada. O Cortex preparou um briefing local com os trechos mais relevantes:\n\n"
            f"{context}"
        )


def tokenize(text: str) -> Counter:
    words = []
    for match in TOKEN_PATTERN.finditer(strip_markdown(text).lower()):
        word = remove_accents(match.group(0))
        if word not in STOPWORDS and not word.isdigit():
            words.append(word)
    return Counter(words)


def split_markdown(content: str) -> list[str]:
    blocks = [block.strip() for block in re.split(r"\n\s*\n", content) if block.strip()]
    chunks = []
    current = ""
    for block in blocks:
        if current and len(current) + len(block) + 2 > CHUNK_SIZE:
            chunks.append(current)
            current = current[-CHUNK_OVERLAP:] if len(current) > CHUNK_OVERLAP else ""
        current = f"{current}\n\n{block}".strip()
    if current:
        chunks.append(current)
    return chunks or [content[:CHUNK_SIZE]]


def strip_markdown(text: str) -> str:
    text = re.sub(r"`{1,3}[^`]*`{1,3}", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", r"\1", text)
    return re.sub(r"[#>*_\-]", " ", text)


def remove_accents(value: str) -> str:
    replacements = str.maketrans(
        "áàãâäéèêëíìîïóòõôöúùûüç",
        "aaaaaeeeeiiiiooooouuuuc",
    )
    return value.translate(replacements)


def cosine_similarity(left: dict[str, float], right: dict[str, float]) -> float:
    if not left or not right:
        return 0.0
    shared = set(left) & set(right)
    numerator = sum(left[term] * right[term] for term in shared)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)


def excerpt(text: str, query_terms: Counter, size: int = 280) -> str:
    clean = " ".join(text.split())
    if len(clean) <= size:
        return clean
    positions = [
        clean.lower().find(term)
        for term in query_terms
        if clean.lower().find(term) >= 0
    ]
    start = max(0, min(positions) - 80) if positions else 0
    return f"{'...' if start else ''}{clean[start:start + size].strip()}..."


def aggregate_terms(documents: list[NoteDocument]) -> Counter:
    counter = Counter()
    for document in documents:
        counter.update(document.terms)
    return counter


def top_terms_for(documents: list[NoteDocument], limit: int) -> list[str]:
    return [term for term, _ in aggregate_terms(documents).most_common(limit)]


def top_terms_from_context(context: list[dict], limit: int) -> list[str]:
    terms = Counter()
    for item in context:
        terms.update(tokenize(f"{item.get('title', '')} {item.get('excerpt', '')}"))
    return [term for term, _ in terms.most_common(limit)]


def canonical_pair(source: str, target: str) -> tuple[str, str]:
    return tuple(sorted([source, target]))


def meaningful_shared_terms(left: NoteDocument, right: NoteDocument) -> set[str]:
    shared = set(left.terms) & set(right.terms)
    generic = {"nota", "conteudo", "exemplo", "processo", "forma", "parte", "caso"}
    return {
        term
        for term in shared
        if term not in generic and left.terms[term] + right.terms[term] >= 2
    }


def confidence_label(score: float) -> str:
    if score >= 0.35:
        return "alta"
    if score >= 0.2:
        return "media"
    return "baixa"


def normalize_write_kind(kind: str) -> str:
    normalized = kind.strip().lower()
    if normalized in {"linkedin", "linkedin_post", "post"}:
        return "linkedin"
    if normalized in {"article", "artigo"}:
        return "article"
    return "requested"


def report_progress(callback, phase: str, message: str) -> None:
    if callback:
        callback(phase, message)


def relation_reason(
    left: NoteDocument,
    right: NoteDocument,
    shared_tags: set[str],
    shared_terms: set[str],
    similarity: float,
) -> str:
    concepts = ", ".join(sorted(shared_terms)[:7])
    if concepts and similarity >= 0.08:
        return (
            f"As notas parecem tratar de uma mesma area conceitual ou operacional: {concepts}. "
            "A recomendacao vem da proximidade do conteudo, nao apenas de tags."
        )
    if concepts:
        return f"Ha vocabulario tecnico recorrente entre as notas: {concepts}."
    if shared_tags:
        return (
            f"As tags ({', '.join('#' + tag for tag in sorted(shared_tags)[:4])}) sugerem uma relacao fraca; "
            "vale validar manualmente antes de criar o link."
        )
    return "Os vetores locais indicam proximidade de conteudo, mas a relacao precisa de validacao humana."


def connection_evidence(left: NoteDocument, right: NoteDocument, shared_terms: set[str]) -> dict:
    query_terms = Counter({term: 1 for term in shared_terms})
    return {
        "source_excerpt": excerpt(left.content, query_terms, size=220),
        "target_excerpt": excerpt(right.content, query_terms, size=220),
        "shared_concepts": sorted(shared_terms)[:10],
    }


def build_connection_review_prompt(relations: list[dict]) -> str:
    candidates = []
    for item in relations:
        candidates.append(
            {
                "source": item["source"],
                "target": item["target"],
                "score": item["score"],
                "local_reason": item["reason"],
                "evidence": item.get("evidence", {}),
            }
        )
    return (
        "Avalie estes candidatos de conexao entre notas. Retorne JSON no formato:\n"
        "[{\"source\":\"...\",\"target\":\"...\",\"keep\":true,\"score\":0.0,"
        "\"connection_type\":\"conceitual|processo|causa_efeito|contraste|sintese\","
        "\"reason\":\"motivo concreto em uma frase\",\"analysis\":\"explicacao curta\"}]\n\n"
        "Candidatos:\n"
        f"{json.dumps(candidates, ensure_ascii=False)}"
    )


def parse_connection_review(text: str) -> list[dict]:
    clean = text.strip()
    if clean.startswith("```"):
        clean = re.sub(r"^```(?:json)?", "", clean).strip()
        clean = re.sub(r"```$", "", clean).strip()
    match = re.search(r"\[.*\]", clean, flags=re.DOTALL)
    if match:
        clean = match.group(0)
    try:
        data = json.loads(clean)
    except json.JSONDecodeError:
        return []
    if not isinstance(data, list):
        return []
    return [item for item in data if isinstance(item, dict)]


def vector_store_result_to_context(item) -> dict:
    filename = getattr(item, "filename", "") or getattr(item, "file_id", "vector-store")
    content = getattr(item, "content", []) or []
    text_parts = []
    for part in content:
        text = getattr(part, "text", "")
        if text:
            text_parts.append(text)
    text = " ".join(text_parts).strip()
    return {
        "path": filename,
        "title": Path(filename).stem,
        "score": round(float(getattr(item, "score", 0) or 0), 4),
        "excerpt": excerpt(text, tokenize(text), size=360) if text else "",
        "source": "openai-vector-store",
        "file_id": getattr(item, "file_id", ""),
    }


def with_private_security_skills(instructions: str) -> str:
    skills = load_private_security_skills()
    if not skills:
        return instructions
    security_context = "\n\n".join(
        f"Skill privada obrigatoria ({skill['path']}):\n{skill['content']}"
        for skill in skills
    )
    return (
        f"{instructions}\n\n"
        "Skills privadas de seguranca obrigatorias:\n"
        f"{security_context}\n\n"
        "Aplique essas skills em toda resposta, revisao, raciocinio e escrita."
    )


def build_llm_prompt(message: str, base: dict) -> str:
    context = "\n\n".join(
        (
            f"Fonte: {item['path']}\n"
            f"Score: {item['score']}\n"
            f"Trecho: {item['excerpt']}"
        )
        for item in base.get("context", [])
    )
    relations = "\n".join(
        f"- {item['source']} -> {item['target']}: {item['reason']}"
        for item in base.get("implicit_relations", [])
    )
    patterns = "\n".join(
        f"- {item['title']}: {item['detail']}"
        for item in base.get("patterns", [])
    )
    focus = base.get("focus") or {}
    return (
        f"Pergunta do usuario:\n{message or 'Analise a nota atual.'}\n\n"
        f"Nota em foco:\n{focus.get('path', 'nenhuma')}\n\n"
        f"Contexto recuperado via RAG:\n{context or 'Nenhum contexto recuperado.'}\n\n"
        f"Padroes detectados localmente:\n{patterns or 'Nenhum padrao local detectado.'}\n\n"
        f"Relacoes implicitas candidatas:\n{relations or 'Nenhuma relacao implicita detectada.'}\n\n"
        "Produza uma resposta de chat com: resposta direta, conexoes relevantes, hipoteses e proximos passos."
    )


def build_writing_prompt(kind: str, theme: str, skill: dict, base: dict) -> str:
    context = "\n\n".join(
        (
            f"Fonte: {item['path']}\n"
            f"Score: {item['score']}\n"
            f"Trecho: {item['excerpt']}"
        )
        for item in base.get("context", [])
    )
    kind_label = {
        "linkedin": "LinkedIn post pronto para publicacao",
        "article": "artigo tecnico completo",
        "requested": "texto solicitado pelo usuario",
    }.get(kind, "texto solicitado pelo usuario")
    structure_instruction = {
        "linkedin": (
            "Para LinkedIn, se entregar material estrategico alem do post, coloque o texto publicavel "
            "em uma secao exatamente chamada '## Postagem completa'."
        ),
        "article": (
            "Para artigo, entregue o artigo completo como corpo principal em Markdown. "
            "Nao use secoes auxiliares numeradas antes do artigo. Use titulos internos normalmente."
        ),
        "requested": (
            "Para texto solicitado, entregue o texto final como corpo principal em Markdown. "
            "Nao separe em blocos estrategicos, a menos que o usuario tenha pedido isso."
        ),
    }.get(kind, "")
    return (
        f"Tipo de escrita: {kind_label}\n"
        f"Tema escolhido: {theme or 'inferir a partir da nota/contexto atual'}\n\n"
        f"Skill de escrita a seguir:\n{skill.get('content') or 'Sem skill encontrada.'}\n\n"
        f"Contexto recuperado do Cortex:\n{context or 'Nenhum contexto recuperado.'}\n\n"
        f"Regra de formato:\n{structure_instruction}\n\n"
        "Gere a saida final respeitando a estrutura obrigatoria da skill quando existir. "
        "Inclua fontes do Cortex usadas ao final em uma secao curta chamada 'Base usada'."
    )


def run_agent(repository: NoteRepository, query: str = "", focus_path: str = "") -> dict:
    try:
        return CortexAgent(repository).run(query=query, focus_path=focus_path)
    except RepositoryError:
        raise


def chat_with_agent(repository: NoteRepository, message: str = "", focus_path: str = "") -> dict:
    try:
        return CortexAgent(repository).chat(message=message, focus_path=focus_path)
    except RepositoryError:
        raise


def recommend_connections(
    repository: NoteRepository,
    focus_path: str = "",
    rejected_pairs: set[tuple[str, str]] | None = None,
) -> dict:
    try:
        return CortexAgent(repository).recommend_connections(
            focus_path=focus_path,
            rejected_pairs=rejected_pairs,
        )
    except RepositoryError:
        raise


def write_with_agent(
    repository: NoteRepository,
    kind: str,
    theme: str = "",
    focus_path: str = "",
    progress=None,
) -> dict:
    try:
        return CortexAgent(repository).write_content(
            kind=kind,
            theme=theme,
            focus_path=focus_path,
            progress=progress,
        )
    except RepositoryError:
        raise
