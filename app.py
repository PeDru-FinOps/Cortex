from __future__ import annotations

import os
import re
import time
import uuid
from functools import wraps
from threading import Lock, Thread

from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, send_file, session, url_for

from cortex_notes.agent import chat_with_agent, recommend_connections, run_agent, write_with_agent
from cortex_notes.connection_rejections import load_rejections, reject_connection
from cortex_notes.graph import build_graph, build_local_graph, build_note_lookup
from cortex_notes.markdown_render import render_markdown
from cortex_notes.openai_sync import SyncError, sync_notes_to_openai
from cortex_notes.repository import NoteRepository, RepositoryError
from cortex_notes.vector_cache import (
    VectorCacheError,
    cache_summary,
    load_vector_cache,
    read_openai_vector_store_to_cache,
)


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-change-me")

repository = NoteRepository(os.getenv("NOTES_ROOT", "notes"))
writing_jobs = {}
writing_jobs_lock = Lock()
vector_read_jobs = {}
vector_read_jobs_lock = Lock()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("authenticated"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


@app.get("/login")
def login():
    if session.get("authenticated"):
        return redirect(url_for("index"))
    return render_template("login.html", error=None)


@app.post("/login")
def login_post():
    load_dotenv(override=True)
    configured_user = os.getenv("APP_USER", "admin")
    configured_password = os.getenv("APP_PASSWORD", "admin")

    if (
        request.form.get("username") == configured_user
        and request.form.get("password") == configured_password
    ):
        session["authenticated"] = True
        return redirect(url_for("index"))

    return render_template("login.html", error="Usuario ou senha invalidos."), 401


@app.post("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.get("/")
@login_required
def index():
    tree = repository.tree()
    selected_path = request.args.get("path") or ""
    mode = request.args.get("mode") or ("read" if selected_path else "new")
    if mode not in {"read", "edit", "new"}:
        mode = "read"
    selected_note = None
    preview_html = ""

    if selected_path:
        try:
            selected_note = repository.read_note(selected_path)
            note_lookup = build_note_lookup(repository, repository.iter_notes())
            preview_html = render_markdown(
                selected_note["content"],
                note_lookup,
                image_resolver=lambda target: repository.find_attachment(target, selected_note["path"]),
            )
        except RepositoryError:
            selected_note = None

    return render_template(
        "index.html",
        tree=tree,
        selected_path=selected_path,
        selected_note=selected_note,
        preview_html=preview_html,
        mode=mode,
        uploaded=request.args.get("uploaded"),
    )


@app.post("/notes")
@login_required
def save_note():
    path = request.form.get("path", "").strip()
    content = request.form.get("content", "")

    try:
        saved_path = repository.write_note(path, content)
    except RepositoryError as error:
        tree = repository.tree()
        return (
            render_template(
                "index.html",
                tree=tree,
                selected_path=path,
                selected_note={"path": path, "content": content},
                preview_html="",
                mode="edit",
                error=str(error),
            ),
            400,
        )

    return redirect(url_for("index", path=saved_path, mode="read"))


@app.post("/notes/delete")
@login_required
def delete_note():
    path = request.form.get("path", "").strip()

    try:
        repository.delete_note(path)
    except RepositoryError:
        return redirect(url_for("index", path=path, mode="read"))

    return redirect(url_for("index"))


@app.post("/notes/move")
@login_required
def move_note():
    payload = request.get_json(silent=True) or {}
    source_path = str(payload.get("source_path", "")).strip()
    target_folder = str(payload.get("target_folder", "")).strip()

    try:
        moved_path = repository.move_note(source_path, target_folder)
    except RepositoryError as error:
        return jsonify({"ok": False, "error": str(error)}), 400

    return jsonify({"ok": True, "path": moved_path})


@app.post("/folders")
@login_required
def create_folder():
    path = request.form.get("path", "").strip()

    try:
        repository.create_folder(path)
    except RepositoryError as error:
        tree = repository.tree()
        return (
            render_template(
                "index.html",
                tree=tree,
                selected_path="",
                selected_note=None,
                preview_html="",
                mode="new",
                error=str(error),
                folder_error=str(error),
            ),
            400,
        )

    return redirect(url_for("index"))


@app.post("/uploads")
@login_required
def upload_notes():
    files = [file for file in request.files.getlist("files") if file.filename]

    if not files:
        tree = repository.tree()
        return (
            render_template(
                "index.html",
                tree=tree,
                selected_path="",
                selected_note=None,
                preview_html="",
                mode="new",
                upload_error="Selecione pelo menos um arquivo Markdown ou imagem.",
            ),
            400,
        )

    imported_paths = []
    imported_note_paths = []
    try:
        for uploaded_file in files:
            imported_path = repository.import_file_stream(uploaded_file.filename, uploaded_file.stream)
            imported_paths.append(imported_path)
            if imported_path.lower().endswith(".md"):
                imported_note_paths.append(imported_path)
    except RepositoryError as error:
        tree = repository.tree()
        return (
            render_template(
                "index.html",
                tree=tree,
                selected_path="",
                selected_note=None,
                preview_html="",
                mode="new",
                upload_error=str(error),
            ),
            400,
        )

    return redirect(
        url_for(
            "index",
            path=(imported_note_paths[-1] if imported_note_paths else ""),
            mode="read",
            uploaded=len(imported_paths),
        )
    )


@app.get("/assets")
@login_required
def assets():
    path = request.args.get("path", "").strip()
    try:
        return send_file(repository.resolve_asset_path(path))
    except RepositoryError:
        return "", 404


@app.get("/api/tree")
@login_required
def api_tree():
    return jsonify(repository.tree())


@app.get("/api/graph")
@login_required
def api_graph():
    return jsonify(build_graph(repository))


@app.get("/api/graph/local")
@login_required
def api_local_graph():
    path = request.args.get("path", "").strip()
    try:
        return jsonify(build_local_graph(repository, path))
    except RepositoryError as error:
        return jsonify({"nodes": [], "edges": [], "error": str(error)}), 404


@app.post("/api/agent/insights")
@login_required
def api_agent_insights():
    payload = request.get_json(silent=True) or {}
    query = str(payload.get("query", "")).strip()
    focus_path = str(payload.get("path", "")).strip()

    try:
        return jsonify(run_agent(repository, query=query, focus_path=focus_path))
    except RepositoryError as error:
        return jsonify({"error": str(error)}), 400


@app.post("/api/agent/chat")
@login_required
def api_agent_chat():
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    focus_path = str(payload.get("path", "")).strip()

    try:
        return jsonify(chat_with_agent(repository, message=message, focus_path=focus_path))
    except RepositoryError as error:
        return jsonify({"error": str(error)}), 400


@app.post("/api/vector-store/sync")
@login_required
def api_vector_store_sync():
    try:
        return jsonify(sync_notes_to_openai(repository))
    except SyncError as error:
        return jsonify({"error": str(error)}), 400


@app.get("/api/vector-store/cache")
@login_required
def api_vector_store_cache():
    return jsonify(cache_summary(load_vector_cache(repository.root)))


@app.post("/api/vector-store/read")
@login_required
def api_vector_store_read():
    payload = request.get_json(silent=True) or {}
    force = request.args.get("force") == "1" or bool(payload.get("force"))
    job_id = uuid.uuid4().hex
    now = time.time()
    with vector_read_jobs_lock:
        vector_read_jobs[job_id] = {
            "id": job_id,
            "status": "queued",
            "phase": "queued",
            "message": "Leitura do Vector Store colocada na fila.",
            "completed": 0,
            "total": 0,
            "started_at": now,
            "updated_at": now,
            "finished_at": None,
            "result": None,
            "error": None,
        }

    Thread(target=run_vector_read_job, args=(job_id, force), daemon=True).start()
    return jsonify({"job_id": job_id, "status": "queued"}), 202


@app.get("/api/vector-store/read/<job_id>")
@login_required
def api_vector_store_read_status(job_id):
    with vector_read_jobs_lock:
        job = vector_read_jobs.get(job_id)
        if not job:
            return jsonify({"error": "Job nao encontrado."}), 404
        payload = dict(job)

    now = time.time()
    payload["elapsed_seconds"] = round((payload.get("finished_at") or now) - payload["started_at"], 1)
    payload["seconds_since_update"] = round(now - payload.get("updated_at", payload["started_at"]), 1)
    total = payload.get("total") or 0
    payload["percent"] = round((payload.get("completed", 0) / total) * 100, 1) if total else 0
    return jsonify(payload)


@app.get("/api/intelligence/recommendations")
@login_required
def api_intelligence_recommendations():
    focus_path = request.args.get("path", "").strip()
    rejections = load_rejections(repository.root)
    rejected_pairs = {
        tuple(sorted([item["source"], item["target"]]))
        for item in rejections.get("rejected", {}).values()
        if item.get("source") and item.get("target")
    }
    try:
        return jsonify(
            recommend_connections(
                repository,
                focus_path=focus_path,
                rejected_pairs=rejected_pairs,
            )
        )
    except RepositoryError as error:
        return jsonify({"error": str(error)}), 400


@app.post("/api/intelligence/recommendations/reject")
@login_required
def api_intelligence_recommendation_reject():
    payload = request.get_json(silent=True) or {}
    source = str(payload.get("source", "")).strip()
    target = str(payload.get("target", "")).strip()
    reason = str(payload.get("reason", "")).strip()
    if not source or not target:
        return jsonify({"error": "Informe origem e destino da conexao."}), 400

    rejected = reject_connection(repository.root, source, target, reason)
    return jsonify({"ok": True, "rejected": rejected})


@app.post("/api/intelligence/recommendations/approve")
@login_required
def api_intelligence_recommendation_approve():
    payload = request.get_json(silent=True) or {}
    source = str(payload.get("source", "")).strip()
    target = str(payload.get("target", "")).strip()
    if not source or not target:
        return jsonify({"error": "Informe origem e destino da conexao."}), 400

    try:
        result = repository.approve_connection(source, target)
    except RepositoryError as error:
        return jsonify({"error": str(error)}), 400

    return jsonify({"ok": True, **result})


@app.post("/api/intelligence/write")
@login_required
def api_intelligence_write():
    payload = request.get_json(silent=True) or {}
    kind = str(payload.get("kind", "")).strip()
    theme = str(payload.get("theme", "")).strip()
    focus_path = str(payload.get("path", "")).strip()

    job_id = uuid.uuid4().hex
    with writing_jobs_lock:
        writing_jobs[job_id] = {
            "id": job_id,
            "status": "queued",
            "phase": "queued",
            "message": "Escrita colocada na fila.",
            "started_at": time.time(),
            "updated_at": time.time(),
            "finished_at": None,
            "result": None,
            "error": None,
        }

    Thread(
        target=run_writing_job,
        args=(job_id, kind, theme, focus_path),
        daemon=True,
    ).start()
    return jsonify({"job_id": job_id, "status": "queued"}), 202


@app.get("/api/intelligence/write/<job_id>")
@login_required
def api_intelligence_write_status(job_id):
    with writing_jobs_lock:
        job = writing_jobs.get(job_id)
        if not job:
            return jsonify({"error": "Job nao encontrado."}), 404
        payload = dict(job)

    now = time.time()
    payload["elapsed_seconds"] = round((payload.get("finished_at") or now) - payload["started_at"], 1)
    payload["seconds_since_update"] = round(now - payload.get("updated_at", payload["started_at"]), 1)
    return jsonify(payload)


@app.post("/api/intelligence/write/approve")
@login_required
def api_intelligence_write_approve():
    payload = request.get_json(silent=True) or {}
    content = str(payload.get("content", "")).strip()
    title = str(payload.get("title", "")).strip()
    kind = str(payload.get("kind", "")).strip()

    if not content:
        return jsonify({"error": "Nao ha texto para salvar."}), 400

    try:
        repository.create_folder("Artigos")
        path = next_article_path(repository, title or title_from_content(content), kind)
        saved_path = repository.write_note(path, approved_article_content(content))
    except RepositoryError as error:
        return jsonify({"error": str(error)}), 400

    return jsonify(
        {
            "ok": True,
            "path": saved_path,
            "url": url_for("index", path=saved_path, mode="read"),
        }
    )


def update_writing_job(job_id: str, **changes) -> None:
    with writing_jobs_lock:
        if job_id in writing_jobs:
            changes.setdefault("updated_at", time.time())
            writing_jobs[job_id].update(changes)


def next_article_path(repository: NoteRepository, title: str, kind: str = "") -> str:
    slug = slugify_title(title) or "texto-gerado"
    if kind:
        prefix = slugify_title(kind)
        slug = f"{prefix}-{slug}" if prefix else slug

    candidate = f"Artigos/{slug}.md"
    counter = 2
    while True:
        try:
            repository.read_note(candidate)
        except RepositoryError:
            return candidate
        candidate = f"Artigos/{slug}-{counter}.md"
        counter += 1


def title_from_content(content: str) -> str:
    for line in content.splitlines():
        clean = line.strip().lstrip("#").strip()
        if clean:
            return clean[:80]
    return "Texto gerado"


def slugify_title(value: str) -> str:
    normalized = remove_accents(value).lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    return normalized.strip("-")[:80]


def remove_accents(value: str) -> str:
    replacements = str.maketrans(
        "áàãâäéèêëíìîïóòõôöúùûüçÁÀÃÂÄÉÈÊËÍÌÎÏÓÒÕÔÖÚÙÛÜÇ",
        "aaaaaeeeeiiiiooooouuuucAAAAAEEEEIIIIOOOOOUUUUC",
    )
    return value.translate(replacements)


def approved_article_content(content: str) -> str:
    return f"{content.strip()}\n"


def update_vector_read_job(job_id: str, **changes) -> None:
    with vector_read_jobs_lock:
        if job_id in vector_read_jobs:
            changes.setdefault("updated_at", time.time())
            vector_read_jobs[job_id].update(changes)


def run_vector_read_job(job_id: str, force: bool = False) -> None:
    def progress(phase: str, message: str, completed: int, total: int) -> None:
        update_vector_read_job(
            job_id,
            status="running",
            phase=phase,
            message=message,
            completed=completed,
            total=total,
        )

    update_vector_read_job(job_id, status="running", phase="starting", message="Inicializando leitura do Vector Store.")
    try:
        result = read_openai_vector_store_to_cache(repository.root, progress=progress, force=force)
    except (VectorCacheError, Exception) as error:  # noqa: BLE001 - surfaced to UI
        update_vector_read_job(
            job_id,
            status="error",
            phase="error",
            message="A leitura do Vector Store falhou.",
            error=str(error),
            finished_at=time.time(),
        )
        return

    update_vector_read_job(
        job_id,
        status="done",
        phase="done",
        message=(
            "Cache existente reutilizado; nenhuma leitura remota foi feita."
            if result.get("reused")
            else "Vector Store lido e cache atualizado."
        ),
        completed=result.get("document_count", 0),
        total=result.get("document_count", 0),
        result=result,
        finished_at=time.time(),
    )


def run_writing_job(job_id: str, kind: str, theme: str, focus_path: str) -> None:
    def progress(phase: str, message: str) -> None:
        update_writing_job(
            job_id,
            status="running",
            phase=phase,
            message=message,
        )

    update_writing_job(job_id, status="running", phase="starting", message="Inicializando agente de escrita.")
    try:
        result = write_with_agent(
            repository,
            kind=kind,
            theme=theme,
            focus_path=focus_path,
            progress=progress,
        )
    except Exception as error:  # noqa: BLE001 - background job must surface errors to UI
        update_writing_job(
            job_id,
            status="error",
            phase="error",
            message="A geracao falhou.",
            error=str(error),
            finished_at=time.time(),
        )
        return

    update_writing_job(
        job_id,
        status="done",
        phase="done",
        message="Geracao concluida.",
        result=result,
        finished_at=time.time(),
    )


if __name__ == "__main__":
    repository.ensure_root()
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")
