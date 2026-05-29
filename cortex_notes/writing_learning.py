from __future__ import annotations

import difflib
import os
import time
from pathlib import Path


PRIVATE_SKILL_NAME = "revisor_pedro"
PRIVATE_SKILL_FILENAME = "SKILL.md"
SECURITY_SKILL_NAMES = ("agente_security", "security_reviwer")


def record_writing_learning(
    original: str,
    edited: str,
    kind: str = "",
    title: str = "",
) -> dict:
    original = original.strip()
    edited = edited.strip()
    if not original or not edited or original == edited:
        return {"recorded": False, "reason": "sem edicoes relevantes"}

    path = private_reviewer_skill_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    current = path.read_text(encoding="utf-8") if path.exists() else initial_reviewer_skill()
    entry = build_learning_entry(original, edited, kind=kind, title=title)
    path.write_text(f"{current.rstrip()}\n\n{entry}\n", encoding="utf-8")
    return {"recorded": True, "path": str(path)}


def load_private_reviewer_skill() -> dict[str, str] | None:
    return load_private_skill(PRIVATE_SKILL_NAME)


def load_private_security_skills() -> list[dict[str, str]]:
    return [skill for name in SECURITY_SKILL_NAMES if (skill := load_private_skill(name))]


def load_private_writing_skills() -> list[dict[str, str]]:
    skills = load_private_security_skills()
    reviewer = load_private_reviewer_skill()
    if reviewer:
        skills.append(reviewer)
    return skills


def load_private_skill(name: str) -> dict[str, str] | None:
    path = private_skill_path(name)
    if not path.exists():
        return None
    return {"path": str(path), "content": path.read_text(encoding="utf-8")}


def private_reviewer_skill_path() -> Path:
    return private_skill_path(PRIVATE_SKILL_NAME)


def private_skill_path(name: str) -> Path:
    root = Path(os.getenv("CORTEX_PRIVATE_SKILLS_DIR", ".cortex_private_skills"))
    return root / name / PRIVATE_SKILL_FILENAME


def initial_reviewer_skill() -> str:
    return (
        "# Skill: revisor_pedro\n\n"
        "Use esta skill privada para aproximar a escrita do Cortex da voz do Pedro.\n\n"
        "Prioridade:\n\n"
        "- Aprender com edicoes aprovadas pelo usuario.\n"
        "- Aprender voz, estrutura, ritmo, nivel de detalhe e formulacoes preferidas.\n"
        "- Nao interpretar remocao de topicos como proibicao futura de falar sobre esses temas.\n"
        "- Tratar topicos removidos como escopo daquela publicacao, salvo quando houver recusa explicita.\n"
        "- Reforcar formulacoes, estruturas e escolhas adicionadas pelo usuario.\n"
        "- Preservar criterio tecnico, clareza e naturalidade humana.\n"
    )


def build_learning_entry(original: str, edited: str, kind: str = "", title: str = "") -> str:
    removed, added = diff_blocks(original, edited)
    original_profile = style_profile(original)
    edited_profile = style_profile(edited)
    return (
        f"## Aprendizado - {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"- Tipo: {kind or 'texto'}\n"
        f"- Tema/Titulo: {title or 'sem titulo informado'}\n"
        f"- Tamanho original: {original_profile['words']} palavras; aprovado: {edited_profile['words']} palavras\n"
        f"- Frase media original: {original_profile['avg_sentence_words']} palavras; "
        f"aprovado: {edited_profile['avg_sentence_words']} palavras\n\n"
        "### Trechos removidos ou alterados nesta edicao\n\n"
        "Observacao: remocao de topico pode indicar apenas ajuste de escopo deste texto, "
        "nao uma preferencia permanente contra o tema.\n\n"
        f"{format_blocks(removed) or '- Nada relevante removido.'}\n\n"
        "### Padroes preferidos pelo usuario\n\n"
        f"{format_blocks(added) or '- Nada relevante adicionado.'}\n\n"
        "### Diretriz inferida\n\n"
        f"{infer_guideline(removed, added, original_profile, edited_profile)}"
    )


def diff_blocks(original: str, edited: str) -> tuple[list[str], list[str]]:
    original_lines = meaningful_lines(original)
    edited_lines = meaningful_lines(edited)
    matcher = difflib.SequenceMatcher(a=original_lines, b=edited_lines)
    removed = []
    added = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag in {"replace", "delete"}:
            removed.extend(original_lines[i1:i2])
        if tag in {"replace", "insert"}:
            added.extend(edited_lines[j1:j2])
    return compact_blocks(removed), compact_blocks(added)


def meaningful_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip() and line.strip() != "---"]


def compact_blocks(lines: list[str], limit: int = 8) -> list[str]:
    compacted = []
    seen = set()
    for line in lines:
        normalized = " ".join(line.split())
        if normalized in seen:
            continue
        seen.add(normalized)
        compacted.append(normalized[:420])
        if len(compacted) >= limit:
            break
    return compacted


def format_blocks(blocks: list[str]) -> str:
    return "\n".join(f"- {block}" for block in blocks)


def style_profile(text: str) -> dict[str, float | int]:
    words = [word for word in text.replace("\n", " ").split(" ") if word.strip()]
    sentences = [part for part in text.replace("\n", " ").replace("?", ".").replace("!", ".").split(".") if part.strip()]
    return {
        "words": len(words),
        "avg_sentence_words": round(len(words) / max(1, len(sentences)), 1),
    }


def infer_guideline(
    removed: list[str],
    added: list[str],
    original_profile: dict[str, float | int],
    edited_profile: dict[str, float | int],
) -> str:
    guidelines = []
    if edited_profile["words"] < original_profile["words"]:
        guidelines.append("Preferir mais concisao quando o texto gerado vier excessivamente explicativo.")
    if edited_profile["avg_sentence_words"] < original_profile["avg_sentence_words"]:
        guidelines.append("Usar frases mais curtas e diretas.")
    if added:
        guidelines.append("Imitar as formulacoes adicionadas pelo usuario em proximas geracoes.")
    if removed:
        guidelines.append(
            "Usar remocoes para calibrar tom, concisao e escopo; nao transformar assuntos removidos em temas proibidos."
        )
    return " ".join(guidelines) or "Manter a versao aprovada como referencia de voz e estrutura."
