from __future__ import annotations

import os
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, session, url_for

from cortex_notes.graph import build_graph, build_local_graph, build_note_lookup
from cortex_notes.markdown_render import render_markdown
from cortex_notes.repository import NoteRepository, RepositoryError


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-change-me")

repository = NoteRepository(os.getenv("NOTES_ROOT", "notes"))


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
            preview_html = render_markdown(selected_note["content"], note_lookup)
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
                upload_error="Selecione pelo menos um arquivo .md.",
            ),
            400,
        )

    imported_paths = []
    try:
        for uploaded_file in files:
            imported_paths.append(
                repository.import_note_stream(uploaded_file.filename, uploaded_file.stream)
            )
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
            path=imported_paths[-1],
            mode="read",
            uploaded=len(imported_paths),
        )
    )


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


if __name__ == "__main__":
    repository.ensure_root()
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")
