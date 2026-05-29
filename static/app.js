const tabs = document.querySelectorAll(".tab");
const views = document.querySelectorAll(".view");
const appShell = document.querySelector(".app-shell");

setupSidebar();
setupTreeContextMenu();
setupTreeDragAndDrop();
setupConfirmForms();
setupVectorStoreSync();
setupAgent();
setupIntelligence();
loadLocalGraph();

tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    tabs.forEach((item) => item.classList.remove("active"));
    views.forEach((view) => view.classList.remove("active"));
    tab.classList.add("active");
    document.getElementById(tab.dataset.view).classList.add("active");
    appShell?.classList.toggle("graph-focused", tab.dataset.view === "graph");
    if (tab.dataset.view === "graph") {
      loadGraph();
    }
  });
});

function setupSidebar() {
  const toggles = document.querySelectorAll(".sidebar-toggle");
  const resizer = document.querySelector(".sidebar-resizer");
  const storedWidth = localStorage.getItem("cortex.sidebarWidth");
  const storedCollapsed = localStorage.getItem("cortex.sidebarCollapsed");
  const mobile = window.matchMedia("(max-width: 760px)").matches;
  const collapsed = storedCollapsed === null ? mobile : storedCollapsed === "1";

  if (storedWidth) {
    setSidebarWidth(Number(storedWidth));
  }
  appShell?.classList.toggle("sidebar-collapsed", collapsed);

  toggles.forEach((toggle) => {
    toggle.addEventListener("click", () => {
      const nextCollapsed = !appShell.classList.contains("sidebar-collapsed");
      appShell.classList.toggle("sidebar-collapsed", nextCollapsed);
      localStorage.setItem("cortex.sidebarCollapsed", nextCollapsed ? "1" : "0");
      setTimeout(() => currentGraphRender?.(), 80);
    });
  });

  document.querySelectorAll(".note-link").forEach((link) => {
    link.addEventListener("click", () => {
      if (!window.matchMedia("(max-width: 760px)").matches) return;
      appShell.classList.add("sidebar-collapsed");
      localStorage.setItem("cortex.sidebarCollapsed", "1");
    });
  });

  if (!resizer) return;

  resizer.addEventListener("mousedown", (event) => {
    event.preventDefault();
    document.body.classList.add("resizing-sidebar");

    const onMouseMove = (moveEvent) => {
      const width = setSidebarWidth(moveEvent.clientX);
      localStorage.setItem("cortex.sidebarWidth", String(width));
      currentGraphRender?.();
    };

    const onMouseUp = () => {
      document.body.classList.remove("resizing-sidebar");
      window.removeEventListener("mousemove", onMouseMove);
      window.removeEventListener("mouseup", onMouseUp);
    };

    window.addEventListener("mousemove", onMouseMove);
    window.addEventListener("mouseup", onMouseUp);
  });
}

function setupAgent() {
  const pane = document.getElementById("agent");
  const button = document.getElementById("agent-run");
  const input = document.getElementById("agent-query-input");
  const result = document.getElementById("agent-result");
  if (!pane || !button || !input || !result) return;

  button.addEventListener("click", async () => {
    const message = input.value.trim();
    button.disabled = true;
    button.textContent = "Pensando...";
    result.innerHTML = '<p class="agent-muted">Recuperando contexto, cruzando notas e consultando a LLM quando configurada...</p>';

    try {
      const response = await fetch("/api/agent/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message,
          path: pane.dataset.notePath || "",
        }),
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || "Nao foi possivel gerar insights.");
      }
      result.innerHTML = renderAgentResult(data);
    } catch (error) {
      result.innerHTML = `<p class="error">${escapeHtml(error.message)}</p>`;
    } finally {
      button.disabled = false;
      button.textContent = "Enviar";
    }
  });
}

function setupVectorStoreSync() {
  const button = document.getElementById("sync-vector-store");
  const status = document.getElementById("sync-status");
  if (!button || !status) return;

  button.addEventListener("click", async () => {
    button.disabled = true;
    button.textContent = "Sync...";
    status.hidden = false;
    status.classList.remove("error", "success");
    status.textContent = "Sincronizando notas com o OpenAI Vector Store.";

    try {
      const response = await fetch(button.dataset.syncUrl, { method: "POST" });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || "Nao foi possivel sincronizar.");
      }
      status.classList.add(data.failed?.length ? "error" : "success");
      status.textContent = syncSummaryText(data);
    } catch (error) {
      status.classList.add("error");
      status.textContent = error.message;
    } finally {
      button.disabled = false;
      button.textContent = "Sync";
    }
  });
}

function setupTreeContextMenu() {
  const menu = document.getElementById("tree-context-menu");
  const folderInput = document.querySelector(".folder-form input[name='path']");
  const folderForm = document.querySelector(".folder-form");
  const quickFolder = document.getElementById("quick-create-folder");
  let target = null;
  if (!menu) return;

  quickFolder?.addEventListener("click", () => {
    const path = prompt("Nome da nova pasta", "nova-pasta");
    if (!path || !folderInput || !folderForm) return;
    folderInput.value = path;
    folderForm.submit();
  });

  document.querySelectorAll(".tree-item").forEach((item) => {
    item.addEventListener("contextmenu", (event) => {
      event.preventDefault();
      target = treeTargetFromElement(item);
      showTreeMenu(menu, target, event.clientX, event.clientY);
    });
  });

  document.addEventListener("click", (event) => {
    if (!menu.contains(event.target)) {
      menu.hidden = true;
    }
  });

  menu.addEventListener("click", async (event) => {
    const button = event.target.closest("[data-tree-action]");
    if (!button || !target) return;
    menu.hidden = true;
    const action = button.dataset.treeAction;
    const folderPath = target.type === "folder" ? target.path : parentFolder(target.path);

    if (action === "new-note") {
      const path = prompt("Nome da nova nota", folderPath ? `${folderPath}/nova-nota.md` : "nova-nota.md");
      if (path) window.location.href = `/?mode=new&path=${encodeURIComponent(path)}`;
      return;
    }

    if (action === "new-folder") {
      const path = prompt("Nome da nova pasta", folderPath ? `${folderPath}/nova-pasta` : "nova-pasta");
      if (!path) return;
      if (folderInput && folderForm) {
        folderInput.value = path;
        folderForm.submit();
      }
      return;
    }

    if (action === "copy-note") {
      await postTreeAction("/notes/copy", { path: target.path }, (data) => {
        window.location.href = `/?path=${encodeURIComponent(data.path)}&mode=read`;
      });
      return;
    }

    if (action === "delete-note") {
      if (!window.confirm(`Apagar nota ${target.path}?`)) return;
      await postTreeAction("/notes/delete", { path: target.path }, () => {
        window.location.href = "/";
      }, true);
      return;
    }

    if (action === "delete-folder") {
      if (!window.confirm(`Apagar pasta ${target.path} e todo seu conteudo?`)) return;
      await postTreeAction("/folders/delete", { path: target.path }, (data) => {
        window.location.href = data.path ? `/?path=${encodeURIComponent(data.path)}&mode=read` : "/";
      });
    }
  });
}

function treeTargetFromElement(item) {
  if (item.dataset.treeType === "folder") {
    return { type: "folder", path: item.dataset.folderPath || "" };
  }
  return { type: "note", path: item.dataset.notePath || "" };
}

function showTreeMenu(menu, target, x, y) {
  menu.querySelector('[data-tree-action="copy-note"]').hidden = target.type !== "note";
  menu.querySelector('[data-tree-action="delete-note"]').hidden = target.type !== "note";
  menu.querySelector('[data-tree-action="delete-folder"]').hidden = target.type !== "folder" || !target.path;
  menu.style.left = `${Math.min(x, window.innerWidth - 210)}px`;
  menu.style.top = `${Math.min(y, window.innerHeight - 220)}px`;
  menu.hidden = false;
}

async function postTreeAction(url, payload, onSuccess, formEncoded = false) {
  const response = await fetch(url, formEncoded ? {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams(payload),
  } : {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (response.redirected) {
    window.location.href = response.url;
    return;
  }
  const data = await response.json().catch(() => ({ ok: response.ok }));
  if (!response.ok || data.ok === false) {
    window.alert(data.error || "Nao foi possivel executar a acao.");
    return;
  }
  onSuccess?.(data);
}

function parentFolder(path) {
  const parts = String(path || "").split("/");
  parts.pop();
  return parts.join("/");
}

function setupIntelligence() {
  const pane = document.getElementById("intelligence");
  const writingPane = document.getElementById("writing");
  if (!pane && !writingPane) return;

  const loadButton = document.getElementById("load-recommendations");
  const recommendationBox = document.getElementById("connection-recommendations");
  const writingTheme = document.getElementById("writing-theme");
  const writingResult = document.getElementById("writing-result");
  const readVectorButton = document.getElementById("read-vector-store");
  const vectorProgress = document.getElementById("vector-read-progress");
  const cacheStatus = document.getElementById("vector-cache-status");

  refreshVectorCacheStatus(cacheStatus);

  readVectorButton?.addEventListener("click", async () => {
    readVectorButton.disabled = true;
    vectorProgress.hidden = false;
    vectorProgress.innerHTML = renderVectorReadProgress({
      phase: "starting",
      message: "Iniciando leitura do Vector Store.",
      percent: 0,
      completed: 0,
      total: 0,
    });
    try {
      const response = await fetch("/api/vector-store/read", { method: "POST" });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Nao foi possivel iniciar a leitura do Vector Store.");
      await watchVectorReadJob(data.job_id, vectorProgress, cacheStatus);
    } catch (error) {
      vectorProgress.innerHTML = `<p class="error">${escapeHtml(error.message)}</p>`;
    } finally {
      readVectorButton.disabled = false;
    }
  });

  loadButton?.addEventListener("click", async () => {
    loadButton.disabled = true;
    loadButton.textContent = "Analisando...";
    recommendationBox.innerHTML = '<p class="agent-muted">Cruzando notas e detectando relações implícitas...</p>';
    try {
      const notePath = encodeURIComponent(pane?.dataset.notePath || "");
      const response = await fetch(`/api/intelligence/recommendations?path=${notePath}`);
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Nao foi possivel carregar recomendacoes.");
      recommendationBox.innerHTML = `
        ${renderTagRecommendations(data.tag_recommendations || [], pane?.dataset.notePath || "")}
        ${renderConnectionRecommendations(data.recommendations || [])}
      `;
    } catch (error) {
      recommendationBox.innerHTML = `<p class="error">${escapeHtml(error.message)}</p>`;
    } finally {
      loadButton.disabled = false;
      loadButton.textContent = "Atualizar";
    }
  });

  recommendationBox?.addEventListener("click", async (event) => {
    const approveButton = event.target.closest("[data-approve-connection]");
    if (approveButton) {
      await handleConnectionDecision(approveButton, "/api/intelligence/recommendations/approve", "Aprovando...", "Aprovar");
      return;
    }

    const tagButton = event.target.closest("[data-approve-tag]");
    if (tagButton) {
      await handleTagApproval(tagButton);
      return;
    }

    const button = event.target.closest("[data-reject-connection]");
    if (!button) return;

    await handleConnectionDecision(button, "/api/intelligence/recommendations/reject", "Rejeitando...", "Rejeitar", {
      reason: "Rejeitada pela interface",
    });
  });

  document.querySelectorAll("[data-write-kind]").forEach((button) => {
    button.addEventListener("click", async () => {
      const kind = button.dataset.writeKind;
      button.disabled = true;
      writingResult.innerHTML = renderWritingProgress({
        phase: "starting",
        message: "Enviando pedido para o servidor.",
        elapsed_seconds: 0,
      });
      try {
        const response = await fetch("/api/intelligence/write", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            kind,
            theme: writingTheme?.value || "",
            path: writingPane?.dataset.notePath || "",
          }),
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || "Nao foi possivel gerar o texto.");
        await watchWritingJob(data.job_id, writingResult);
      } catch (error) {
        writingResult.innerHTML = `<p class="error">${escapeHtml(error.message)}</p>`;
      } finally {
        button.disabled = false;
      }
    });
  });

  writingResult?.addEventListener("click", async (event) => {
    const copyButton = event.target.closest("[data-copy-writing]");
    if (copyButton) {
      try {
        await navigator.clipboard.writeText(readWritingMainText(writingResult));
        temporarilyRenameButton(copyButton, "Copiado");
      } catch {
        window.alert("Nao foi possivel copiar automaticamente.");
      }
      return;
    }

    const editButton = event.target.closest("[data-edit-writing]");
    if (editButton) {
      toggleWritingEditor(writingResult, editButton);
      return;
    }

    const approveButton = event.target.closest("[data-approve-writing]");
    if (approveButton) {
      await approveWritingSuggestion(writingResult, approveButton);
      return;
    }

    const addTagButton = event.target.closest("[data-add-writing-tag]");
    if (addTagButton) {
      addWritingTag(writingResult, addTagButton.dataset.addWritingTag || "");
    }
  });
}

async function refreshVectorCacheStatus(container) {
  if (!container) return;
  try {
    const response = await fetch("/api/vector-store/cache");
    const data = await response.json();
    if (!data.available) {
      container.textContent = "Sem cache lido. A escrita usara fallback local.";
      return;
    }
    const date = data.created_at ? new Date(data.created_at * 1000).toLocaleString() : "data desconhecida";
    const usable = Number(data.documents_with_text || 0);
    const errors = Number(data.documents_with_errors || 0);
    if (!data.usable) {
      container.textContent = `${data.document_count} arquivo(s) registrados, mas 0 com texto utilizavel. Releia o Vector Store. Atualizado em ${date}.`;
      return;
    }
    const errorText = errors ? ` ${errors} sem trecho recuperado.` : "";
    container.textContent = `${usable}/${data.document_count} arquivo(s) com trechos em cache. Atualizado em ${date}.${errorText}`;
  } catch {
    container.textContent = "Nao foi possivel verificar o cache.";
  }
}

async function watchVectorReadJob(jobId, container, cacheStatus) {
  if (!jobId) throw new Error("Servidor nao retornou o identificador da leitura.");

  while (true) {
    const response = await fetch(`/api/vector-store/read/${encodeURIComponent(jobId)}`);
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Nao foi possivel consultar a leitura do Vector Store.");

    if (data.status === "done") {
      container.innerHTML = renderVectorReadProgress(data);
      await refreshVectorCacheStatus(cacheStatus);
      return;
    }

    if (data.status === "error") {
      container.innerHTML = `
        ${renderVectorReadProgress(data)}
        <p class="error">${escapeHtml(data.error || "A leitura falhou.")}</p>
      `;
      return;
    }

    container.innerHTML = renderVectorReadProgress(data);
    await sleep(1800);
  }
}

function renderVectorReadProgress(job) {
  const percent = Number(job.percent || 0);
  return `
    <section class="vector-progress-card">
      <div class="vector-progress-header">
        <strong>${escapeHtml(vectorReadPhaseLabel(job.phase))}</strong>
        <span>${escapeHtml(job.message || "Lendo Vector Store.")}</span>
      </div>
      <div class="progress-track">
        <div class="progress-bar" style="width: ${Math.max(0, Math.min(100, percent))}%"></div>
      </div>
      <small>${escapeHtml(String(job.completed || 0))}/${escapeHtml(String(job.total || 0))} arquivos · ${escapeHtml(String(percent))}% · ${escapeHtml(String(job.elapsed_seconds || 0))}s decorridos</small>
    </section>
  `;
}

function vectorReadPhaseLabel(phase) {
  const labels = {
    queued: "Na fila",
    starting: "Inicializando",
    listing: "Listando arquivos",
    metadata: "Mapeando arquivos",
    reading: "Lendo arquivos",
    searching: "Consultando RAG",
    cached: "Cache reutilizado",
    done: "Cache atualizado",
    error: "Erro",
  };
  return labels[phase] || "Lendo Vector Store";
}

async function watchWritingJob(jobId, container) {
  if (!jobId) throw new Error("Servidor nao retornou o identificador da geracao.");

  while (true) {
    const response = await fetch(`/api/intelligence/write/${encodeURIComponent(jobId)}`);
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Nao foi possivel consultar o status da geracao.");

    if (data.status === "done") {
      container.innerHTML = renderWritingResultV2(data.result);
      return;
    }

    if (data.status === "error") {
      container.innerHTML = `
        ${renderWritingProgress(data)}
        <p class="error">${escapeHtml(data.error || "A geracao falhou.")}</p>
      `;
      return;
    }

    container.innerHTML = renderWritingProgress(data);
    await sleep(1800);
  }
}

function renderWritingProgress(job) {
  return `
    <section class="writing-progress">
      <div class="progress-spinner" aria-hidden="true"></div>
      <div>
        <strong>${escapeHtml(progressPhaseLabel(job.phase))}</strong>
        <span>${escapeHtml(job.message || "Processando.")}</span>
        <small>${escapeHtml(String(job.elapsed_seconds || 0))}s decorridos · ${escapeHtml(String(job.seconds_since_update || 0))}s sem nova etapa</small>
      </div>
    </section>
  `;
}

function progressPhaseLabel(phase) {
  const labels = {
    queued: "Na fila",
    starting: "Inicializando",
    retrieving: "Recuperando contexto",
    skill: "Carregando skill",
    reading_cache: "Lendo cache",
    llm: "Escrevendo com IA",
    fallback: "Fallback local",
    done: "Concluido",
    error: "Erro",
  };
  return labels[phase] || "Processando";
}

function sleep(milliseconds) {
  return new Promise((resolve) => window.setTimeout(resolve, milliseconds));
}

async function handleConnectionDecision(button, url, loadingText, fallbackText, extraPayload = {}) {
  const recommendationBox = document.getElementById("connection-recommendations");
  button.disabled = true;
  button.textContent = loadingText;
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        source: button.dataset.source,
        target: button.dataset.target,
        ...extraPayload,
      }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Nao foi possivel processar a conexao.");
    button.closest(".connection-card")?.remove();
    const status = document.createElement("p");
    status.className = "success";
    status.textContent = url.includes("approve")
      ? "Conexao aprovada e adicionada nas duas notas."
      : "Conexao rejeitada.";
    recommendationBox.prepend(status);
    if (!recommendationBox.querySelector(".connection-card")) {
      recommendationBox.insertAdjacentHTML("beforeend", '<p class="agent-muted">Nenhuma conexao pendente neste contexto.</p>');
    }
  } catch (error) {
    window.alert(error.message);
    button.disabled = false;
    button.textContent = fallbackText;
  }
}

function renderConnectionRecommendations(items) {
  if (!items.length) {
    return '<p class="agent-muted">Nenhuma conexao nova encontrada para este contexto.</p>';
  }
  return items.map((item) => {
    const analysis = item.analysis ? `<span>${escapeHtml(item.analysis)}</span>` : "";
    const connectionType = item.connection_type ? `<span>Tipo: ${escapeHtml(item.connection_type)}</span>` : "";
    return `
      <article class="connection-card">
        <strong>${escapeHtml(item.source)} -> ${escapeHtml(item.target)}</strong>
        <span>${escapeHtml(item.reason)}</span>
        ${analysis}
        <div class="connection-meta">
          <span>Confianca: ${escapeHtml(item.metadata?.confidence || "baixa")}</span>
          <span>Score: ${escapeHtml(String(item.score))}</span>
          ${connectionType}
          <span>${escapeHtml(item.metadata?.recommended_link || "")}</span>
        </div>
        <div class="connection-actions">
          <button type="button" data-approve-connection data-source="${escapeHtml(item.source)}" data-target="${escapeHtml(item.target)}">Aprovar</button>
          <button class="secondary-button" type="button" data-reject-connection data-source="${escapeHtml(item.source)}" data-target="${escapeHtml(item.target)}">Rejeitar</button>
        </div>
      </article>
    `;
  }).join("");
}

function renderTagRecommendations(items, notePath) {
  if (!items.length) return "";
  return `
    <section class="tag-suggestion-panel">
      <h3>Tags sugeridas</h3>
      <div class="tag-suggestion-list">
        ${items.map((item) => `
          <article class="tag-suggestion-card">
            <strong>#${escapeHtml(item.tag)}</strong>
            <span>${escapeHtml(item.reason || "Tag relevante para enriquecer o grafo.")}</span>
            <button type="button" data-approve-tag data-note-path="${escapeHtml(notePath)}" data-tag="${escapeHtml(item.tag)}">Aprovar tag</button>
          </article>
        `).join("")}
      </div>
    </section>
  `;
}

async function handleTagApproval(button) {
  button.disabled = true;
  button.textContent = "Aprovando...";
  try {
    const response = await fetch("/api/intelligence/tags/approve", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        path: button.dataset.notePath,
        tags: [button.dataset.tag],
      }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Nao foi possivel aprovar a tag.");
    button.closest(".tag-suggestion-card")?.remove();
  } catch (error) {
    window.alert(error.message);
    button.disabled = false;
    button.textContent = "Aprovar tag";
  }
}

function renderWritingResult(data) {
  return `
    <section class="agent-answer writing-output">
      <div class="agent-provider">${escapeHtml(providerLabel(data.llm))} · ${escapeHtml(data.skill || "skill local")}</div>
      <p>${formatMultiline(data.content || "")}</p>
    </section>
    ${renderAgentCards("Base usada", data.context, (item) => `
      <strong>${escapeHtml(item.path)}</strong>
      <span>${escapeHtml(item.excerpt)}</span>
    `)}
  `;
}

function renderWritingResultV2(data) {
  const parsed = parseWritingContent(data.content || "", data.kind || "");
  const mainText = parsed.main?.content || data.content || "";
  const supportSections = parsed.sections.filter((section) => section !== parsed.main && !isBaseUsedSection(section.title));
  return `
    <section class="writing-package" data-writing-kind="${escapeHtml(data.kind || "")}" data-writing-theme="${escapeHtml(data.theme || "")}" data-original-writing="${escapeHtml(encodeURIComponent(mainText))}">
      <div class="writing-package-header">
        <div>
          <span class="agent-provider">${escapeHtml(providerLabel(data.llm))} - ${escapeHtml(data.skill || "skill local")}</span>
          <h2>${escapeHtml(writingMainLabel(data.kind))}</h2>
        </div>
        <div class="writing-package-actions">
          <button type="button" data-copy-writing>Copiar</button>
          <button class="secondary-button" type="button" data-edit-writing>Editar</button>
          <button type="button" data-approve-writing>Aprovar e salvar</button>
        </div>
      </div>
      <article class="writing-main">
        <div class="writing-main-text" data-markdown-source="${escapeHtml(encodeURIComponent(mainText))}">${renderMarkdownLite(mainText)}</div>
        <textarea class="writing-editor" hidden>${escapeHtml(mainText)}</textarea>
      </article>
      ${renderWritingTagEditor(data.suggested_tags || [])}
    </section>
    ${renderWritingSupportSections(supportSections)}
    ${renderAgentCards("Base usada", data.context, (item) => `
      <strong>${escapeHtml(item.path)}</strong>
      <span>${escapeHtml(item.excerpt)}</span>
    `)}
  `;
}

function renderWritingTagEditor(items) {
  const tags = items.map((item) => `#${item.tag}`).join(" ");
  return `
    <section class="writing-tags">
      <label for="writing-tags-input">Tags aprovadas</label>
      <input id="writing-tags-input" list="writing-tag-options" value="${escapeHtml(tags)}" placeholder="#finops #azure">
      <datalist id="writing-tag-options">
        ${items.map((item) => `<option value="#${escapeHtml(item.tag)}"></option>`).join("")}
      </datalist>
      ${items.length ? `
        <div class="suggested-tag-list">
          ${items.map((item) => `<button class="secondary-button" type="button" data-add-writing-tag="${escapeHtml(item.tag)}">#${escapeHtml(item.tag)}</button>`).join("")}
        </div>
      ` : ""}
    </section>
  `;
}

function parseWritingContent(content, kind = "") {
  const sections = [];
  const headingPattern = /^##\s+(?:\d+\.\s+)?(.+)$/gm;
  const matches = [...content.matchAll(headingPattern)];
  const explicitMainPattern = /^##\s+(?:\d+\.\s+)?(postagem completa|artigo completo|texto completo)\s*$/gim;
  const hasExplicitMain = explicitMainPattern.test(content);
  if (kind !== "linkedin" && !hasExplicitMain) {
    return {
      main: { title: writingMainLabel(kind), content },
      sections: [{ title: writingMainLabel(kind), content }],
    };
  }
  if (!matches.length) {
    return {
      main: { title: writingMainLabel(kind), content },
      sections: [{ title: writingMainLabel(kind), content }],
    };
  }

  matches.forEach((match, index) => {
    const start = match.index + match[0].length;
    const end = matches[index + 1]?.index ?? content.length;
    sections.push({
      title: match[1].trim(),
      content: content.slice(start, end).replace(/^[-\s]+/, "").trim(),
    });
  });

  const main = sections.find((section) => normalizeSectionTitle(section.title).includes("postagem completa"))
    || sections.find((section) => normalizeSectionTitle(section.title).includes("artigo completo"))
    || sections.find((section) => normalizeSectionTitle(section.title).includes("texto completo"))
    || sections[0];

  return { main, sections };
}

function renderWritingSupportSections(sections) {
  if (!sections.length) return "";
  const primaryTitles = new Set([
    "objetivo da postagem",
    "percepcao desejada",
    "publico-alvo",
    "tema principal",
    "hook alternativo",
    "cta sugerido",
  ]);
  const primary = sections.filter((section) => primaryTitles.has(normalizeSectionTitle(section.title)));
  const secondary = sections.filter((section) => !primaryTitles.has(normalizeSectionTitle(section.title)));
  return `
    ${primary.length ? `
      <section class="writing-support-grid">
        ${primary.map(renderWritingSupportCard).join("")}
      </section>
    ` : ""}
    ${secondary.length ? `
      <section class="writing-support-list">
        ${secondary.map(renderWritingSupportCard).join("")}
      </section>
    ` : ""}
  `;
}

function renderWritingSupportCard(section) {
  return `
    <article class="writing-support-card">
      <h3>${escapeHtml(section.title)}</h3>
      <div>${renderMarkdownLite(section.content)}</div>
    </article>
  `;
}

function normalizeSectionTitle(title) {
  return title
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim();
}

function isBaseUsedSection(title) {
  return normalizeSectionTitle(title).includes("base usada");
}

function writingMainLabel(kind) {
  if (kind === "article") return "Artigo pronto";
  if (kind === "requested") return "Texto pronto";
  return "Postagem pronta";
}

function readWritingMainText(container) {
  const editor = container.querySelector(".writing-editor");
  if (editor && !editor.hidden) return editor.value.trim();
  const text = container.querySelector(".writing-main-text");
  return text?.dataset.markdownSource ? decodeURIComponent(text.dataset.markdownSource).trim() : text?.textContent.trim() || "";
}

function toggleWritingEditor(container, button) {
  const editor = container.querySelector(".writing-editor");
  const text = container.querySelector(".writing-main-text");
  if (!editor || !text) return;
  const editing = editor.hidden;
  if (editing) {
    editor.value = readWritingMainText(container);
    editor.hidden = false;
    text.hidden = true;
    button.textContent = "Concluir edicao";
    editor.focus();
    return;
  }
  const value = editor.value.trim();
  text.dataset.markdownSource = encodeURIComponent(value);
  text.innerHTML = renderMarkdownLite(value);
  text.hidden = false;
  editor.hidden = true;
  button.textContent = "Editar";
}

async function approveWritingSuggestion(container, button) {
  const packageElement = container.querySelector(".writing-package");
  const content = readWritingMainText(container);
  if (!content) {
    window.alert("Nao ha texto para salvar.");
    return;
  }

  button.disabled = true;
  const previousText = button.textContent;
  button.textContent = "Salvando...";
  try {
    const response = await fetch("/api/intelligence/write/approve", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        content,
        original_content: packageElement?.dataset.originalWriting ? decodeURIComponent(packageElement.dataset.originalWriting) : "",
        kind: packageElement?.dataset.writingKind || "",
        title: packageElement?.dataset.writingTheme || titleFromText(content),
        tags: readWritingTags(container),
      }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Nao foi possivel salvar o texto.");
    button.textContent = "Salvo";
    const status = document.createElement("p");
    status.className = "success";
    const learningText = data.learning?.recorded ? " Aprendizado de escrita registrado." : "";
    status.innerHTML = `Texto salvo em <a href="${escapeHtml(data.url)}">${escapeHtml(data.path)}</a>.${escapeHtml(learningText)}`;
    packageElement.insertAdjacentElement("afterend", status);
  } catch (error) {
    window.alert(error.message);
    button.disabled = false;
    button.textContent = previousText;
  }
}

function readWritingTags(container) {
  const input = container.querySelector("#writing-tags-input");
  if (!input) return [];
  return input.value.split(/[\s,]+/).map((tag) => tag.trim()).filter(Boolean);
}

function addWritingTag(container, tag) {
  const input = container.querySelector("#writing-tags-input");
  if (!input || !tag) return;
  const current = new Set(readWritingTags(container).map((item) => item.replace(/^#/, "").toLowerCase()));
  current.add(tag.replace(/^#/, "").toLowerCase());
  input.value = [...current].map((item) => `#${item}`).join(" ");
}

function titleFromText(content) {
  const firstLine = content.split("\n").map((line) => line.trim().replace(/^#+\s*/, "")).find(Boolean);
  return firstLine || "Texto gerado";
}

function temporarilyRenameButton(button, label) {
  const previousText = button.textContent;
  button.textContent = label;
  window.setTimeout(() => {
    button.textContent = previousText;
  }, 1400);
}

function renderMarkdownLite(markdown) {
  const lines = String(markdown || "").split("\n");
  let html = "";
  let paragraph = [];
  let listOpen = false;

  const flushParagraph = () => {
    if (!paragraph.length) return;
    html += `<p>${renderInlineMarkdown(paragraph.join(" "))}</p>`;
    paragraph = [];
  };
  const closeList = () => {
    if (!listOpen) return;
    html += "</ul>";
    listOpen = false;
  };

  lines.forEach((line) => {
    const trimmed = line.trim();
    if (!trimmed) {
      flushParagraph();
      closeList();
      return;
    }
    const heading = trimmed.match(/^(#{1,6})\s+(.+)$/);
    if (heading) {
      flushParagraph();
      closeList();
      const level = Math.min(6, heading[1].length + 1);
      html += `<h${level}>${renderInlineMarkdown(heading[2])}</h${level}>`;
      return;
    }
    const listItem = trimmed.match(/^[-*]\s+(.+)$/);
    if (listItem) {
      flushParagraph();
      if (!listOpen) {
        html += "<ul>";
        listOpen = true;
      }
      html += `<li>${renderInlineMarkdown(listItem[1])}</li>`;
      return;
    }
    paragraph.push(trimmed);
  });

  flushParagraph();
  closeList();
  return html;
}

function renderInlineMarkdown(value) {
  let html = escapeHtml(value);
  html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  html = html.replace(/\*([^*]+)\*/g, "<em>$1</em>");
  html = html.replace(/`([^`]+)`/g, "<code>$1</code>");
  return html;
}

function syncSummaryText(data) {
  const parts = [
    `${data.uploaded?.length || 0} novos`,
    `${data.updated?.length || 0} atualizados`,
    `${data.deleted?.length || 0} removidos`,
    `${data.skipped?.length || 0} sem mudancas`,
  ];
  if (data.failed?.length) {
    parts.push(`${data.failed.length} falhas`);
  }
  return `Sync concluido: ${parts.join(", ")}.`;
}

function renderAgentResult(data) {
  return `
    <section class="agent-answer">
      <div class="agent-provider">${escapeHtml(providerLabel(data.llm))}</div>
      <p>${formatMultiline(data.answer || data.synthesis || "")}</p>
    </section>
    <section class="agent-section">
      <h2>Síntese local</h2>
      <p>${escapeHtml(data.synthesis || "")}</p>
    </section>
    ${renderAgentCards("Padrões", data.patterns, (item) => `<strong>${escapeHtml(item.title)}</strong><span>${escapeHtml(item.detail)}</span>`)}
    ${renderAgentCards("Relações implícitas", data.implicit_relations, (item) => `
      <strong>${escapeHtml(item.source)} -> ${escapeHtml(item.target)}</strong>
      <span>${escapeHtml(item.reason)} Afinidade ${escapeHtml(String(item.score))}.</span>
    `)}
    ${renderAgentList("Hipóteses", data.hypotheses)}
    ${renderAgentList("Próximas perguntas", data.next_questions)}
    ${renderAgentCards("Contexto recuperado", data.context, (item) => `
      <strong>${escapeHtml(item.path)}</strong>
      <span>${escapeHtml(item.source || "local")} · score ${escapeHtml(String(item.score))}</span>
      <span>${escapeHtml(item.excerpt)}</span>
    `)}
  `;
}

function providerLabel(llm) {
  if (!llm) return "Modo local";
  if (llm.enabled && llm.vector_store) return `OpenAI · ${llm.model} · Vector Store ${llm.vector_store}`;
  if (llm.enabled) return `OpenAI · ${llm.model}`;
  return `Fallback local · ${llm.reason || llm.model || "sem LLM"}`;
}

function formatMultiline(value) {
  return escapeHtml(value).replaceAll("\n", "<br>");
}

function renderAgentCards(title, items, renderItem) {
  if (!items || !items.length) return "";
  return `
    <section class="agent-section">
      <h2>${escapeHtml(title)}</h2>
      <div class="agent-card-grid">
        ${items.map((item) => `<article class="agent-card">${renderItem(item)}</article>`).join("")}
      </div>
    </section>
  `;
}

function renderAgentList(title, items) {
  if (!items || !items.length) return "";
  return `
    <section class="agent-section">
      <h2>${escapeHtml(title)}</h2>
      <ul class="agent-list">
        ${items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
      </ul>
    </section>
  `;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function setupConfirmForms() {
  document.querySelectorAll("form[data-confirm]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!window.confirm(form.dataset.confirm)) {
        event.preventDefault();
      }
    });
  });
}

function setupTreeDragAndDrop() {
  document.querySelectorAll(".note-link[draggable='true']").forEach((link) => {
    link.addEventListener("dragstart", (event) => {
      event.dataTransfer.effectAllowed = "move";
      event.dataTransfer.setData("text/plain", link.dataset.notePath);
      event.dataTransfer.setData("application/x-cortex-note", link.dataset.notePath);
      link.classList.add("dragging-note");
    });

    link.addEventListener("dragend", () => {
      link.classList.remove("dragging-note");
      clearFolderDropState();
    });
  });

  document.querySelectorAll(".folder-drop-target").forEach((target) => {
    target.addEventListener("dragover", (event) => {
      const dragTypes = Array.from(event.dataTransfer.types);
      if (!dragTypes.includes("application/x-cortex-note") && !dragTypes.includes("text/plain")) {
        return;
      }
      event.preventDefault();
      event.dataTransfer.dropEffect = "move";
      target.classList.add("folder-drop-hover");
    });

    target.addEventListener("dragleave", () => {
      target.classList.remove("folder-drop-hover");
    });

    target.addEventListener("drop", async (event) => {
      event.preventDefault();
      const sourcePath = event.dataTransfer.getData("application/x-cortex-note") || event.dataTransfer.getData("text/plain");
      const targetFolder = target.dataset.folderPath || "";
      clearFolderDropState();
      if (!sourcePath) return;

      const response = await fetch("/notes/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          source_path: sourcePath,
          target_folder: targetFolder,
        }),
      });
      const result = await response.json();
      if (!result.ok) {
        window.alert(result.error || "Nao foi possivel mover a nota.");
        return;
      }
      window.location.href = `/?path=${encodeURIComponent(result.path)}&mode=read`;
    });
  });
}

function clearFolderDropState() {
  document.querySelectorAll(".folder-drop-hover").forEach((item) => {
    item.classList.remove("folder-drop-hover");
  });
}

function setSidebarWidth(rawWidth) {
  const maxWidth = Math.floor(window.innerWidth * 0.5);
  const width = Math.max(240, Math.min(maxWidth, Number(rawWidth) || 320));
  document.documentElement.style.setProperty("--sidebar-width", `${width}px`);
  return width;
}

const dropzone = document.querySelector(".dropzone");
const fileInput = document.getElementById("upload-files");
const folderInput = document.getElementById("upload-folder");

if (dropzone && fileInput && folderInput) {
  dropzone.querySelector('[data-upload-picker="files"]').addEventListener("click", () => {
    fileInput.click();
  });

  dropzone.querySelector('[data-upload-picker="folder"]').addEventListener("click", () => {
    folderInput.click();
  });

  fileInput.addEventListener("change", () => uploadFiles([...fileInput.files]));
  folderInput.addEventListener("change", () => uploadFiles([...folderInput.files]));

  ["dragenter", "dragover"].forEach((eventName) => {
    dropzone.addEventListener(eventName, (event) => {
      event.preventDefault();
      dropzone.classList.add("dragging");
    });
  });

  ["dragleave", "drop"].forEach((eventName) => {
    dropzone.addEventListener(eventName, () => {
      dropzone.classList.remove("dragging");
    });
  });

  dropzone.addEventListener("drop", async (event) => {
    event.preventDefault();
    const files = await collectDroppedFiles(event.dataTransfer);
    uploadFiles(files);
  });
}

async function uploadFiles(files) {
  const supportedFiles = files.filter((file) => isSupportedUpload(file.name));
  if (!supportedFiles.length) return;

  const formData = new FormData();
  supportedFiles.forEach((file) => {
    const relativePath = file.relativePath || file.webkitRelativePath || file.name;
    formData.append("files", file, relativePath);
  });

  const response = await fetch(dropzone.dataset.uploadUrl, {
    method: "POST",
    body: formData,
  });

  if (response.redirected) {
    window.location.href = response.url;
    return;
  }

  window.location.reload();
}

function isSupportedUpload(name) {
  return /\.(md|png|jpe?g|gif|webp|svg)$/i.test(name);
}

async function collectDroppedFiles(dataTransfer) {
  const items = [...(dataTransfer.items || [])];
  if (!items.length) return [...dataTransfer.files];

  const entries = items
    .map((item) => (item.webkitGetAsEntry ? item.webkitGetAsEntry() : null))
    .filter(Boolean);

  if (!entries.length) return [...dataTransfer.files];

  const files = [];
  for (const entry of entries) {
    files.push(...(await readEntry(entry, "")));
  }
  return files;
}

async function readEntry(entry, basePath) {
  if (entry.isFile) {
    return [
      await new Promise((resolve) => {
        entry.file((file) => {
          file.relativePath = `${basePath}${file.name}`;
          resolve(file);
        });
      }),
    ];
  }

  if (!entry.isDirectory) return [];

  const reader = entry.createReader();
  const entries = await readAllEntries(reader);
  const files = [];
  for (const child of entries) {
    files.push(...(await readEntry(child, `${basePath}${entry.name}/`)));
  }
  return files;
}

async function readAllEntries(reader) {
  const entries = [];
  let batch = [];
  do {
    batch = await new Promise((resolve) => reader.readEntries(resolve));
    entries.push(...batch);
  } while (batch.length);
  return entries;
}

async function loadGraph() {
  const response = await fetch("/api/graph");
  const graph = await response.json();
  renderGraph(graph);
}

async function loadLocalGraph() {
  const canvas = document.getElementById("local-graph-canvas");
  if (!canvas) return;

  const notePath = canvas.dataset.notePath;
  const response = await fetch(`/api/graph/local?path=${encodeURIComponent(notePath)}`);
  const graph = await response.json();
  renderLocalGraph(canvas, graph);
}

function renderLocalGraph(canvas, graph) {
  const container = canvas.closest(".local-graph");
  const status = container?.querySelector(".local-graph-status");
  const context = canvas.getContext("2d");
  const rect = canvas.getBoundingClientRect();
  const ratio = window.devicePixelRatio || 1;
  const minCanvasWidth = window.matchMedia("(max-width: 760px)").matches ? 280 : 520;
  const width = Math.max(minCanvasWidth, rect.width || 720);
  const height = window.matchMedia("(max-width: 760px)").matches ? 260 : 320;
  canvas.width = width * ratio;
  canvas.height = height * ratio;
  canvas.style.width = `${width}px`;
  canvas.style.height = `${height}px`;
  context.setTransform(ratio, 0, 0, ratio, 0, 0);

  const nodes = graph.nodes || [];
  const edges = graph.edges || [];
  const focusId = graph.focus;
  const focusNode = nodes.find((node) => node.id === focusId);

  if (!focusNode || nodes.length <= 1) {
    context.fillStyle = "#050a13";
    context.fillRect(0, 0, width, height);
    if (status) status.textContent = "Sem conexoes diretas";
    context.fillStyle = "rgba(248, 250, 252, 0.72)";
    context.font = "14px Segoe UI, sans-serif";
    context.fillText("Esta nota ainda nao possui tags ou links diretos.", 24, 170);
    return;
  }

  if (status) status.textContent = `${nodes.length - 1} conexao(oes)`;

  const localNodes = nodes.map((node) => ({
    ...node,
    degree: edges.filter((edge) => edge.source === node.id || edge.target === node.id).length,
    radius: node.id === focusId ? 10 : node.group === "tag" ? 7 : 5,
  }));
  const nodeById = new Map(localNodes.map((node) => [node.id, node]));
  const localEdges = edges
    .map((edge) => ({
      ...edge,
      sourceNode: nodeById.get(edge.source),
      targetNode: nodeById.get(edge.target),
    }))
    .filter((edge) => edge.sourceNode && edge.targetNode);

  const worldWidth = Math.max(760, width * 1.45, nodes.length * 70);
  const worldHeight = Math.max(460, height * 1.35, nodes.length * 32);
  const worldCenter = { x: worldWidth / 2, y: worldHeight / 2 };
  const neighbors = localNodes.filter((node) => node.id !== focusId);
  const radius = Math.min(worldWidth, worldHeight) * 0.34;

  neighbors.forEach((node, index) => {
    const angle = (Math.PI * 2 * index) / Math.max(1, neighbors.length) - Math.PI / 2;
    const tagOffset = node.group === "tag" ? 0.88 : 1.04;
    node.x = worldCenter.x + Math.cos(angle) * radius * tagOffset;
    node.y = worldCenter.y + Math.sin(angle) * radius * tagOffset;
  });
  nodeById.get(focusId).x = worldCenter.x;
  nodeById.get(focusId).y = worldCenter.y;

  localGraphState = {
    canvas,
    context,
    nodes: localNodes,
    edges: localEdges,
    focusId,
    hoveredNode: null,
    dragging: false,
    lastX: 0,
    lastY: 0,
    screenWidth: width,
    screenHeight: height,
    worldWidth,
    worldHeight,
    viewport: { scale: 1, offsetX: 0, offsetY: 0 },
  };
  fitLocalGraphToScreen();
  bindLocalGraphControls();
  drawLocalGraph();
}

function bindLocalGraphControls() {
  const state = localGraphState;
  if (!state) return;

  document.querySelectorAll("[data-local-graph-zoom]").forEach((button) => {
    button.onclick = () => {
      const action = button.dataset.localGraphZoom;
      if (action === "in") zoomLocalGraph(1.18);
      if (action === "out") zoomLocalGraph(1 / 1.18);
      if (action === "reset") fitLocalGraphToScreen();
      drawLocalGraph();
    };
  });

  state.canvas.onwheel = (event) => {
    event.preventDefault();
    zoomLocalGraph(event.deltaY < 0 ? 1.08 : 1 / 1.08);
    drawLocalGraph();
  };

  state.canvas.onmousedown = (event) => {
    state.dragging = true;
    state.lastX = event.clientX;
    state.lastY = event.clientY;
    state.canvas.classList.add("panning");
  };

  state.canvas.onmousemove = (event) => {
    if (state.dragging) {
      state.viewport.offsetX += event.clientX - state.lastX;
      state.viewport.offsetY += event.clientY - state.lastY;
      state.lastX = event.clientX;
      state.lastY = event.clientY;
      drawLocalGraph();
      return;
    }

    const point = localScreenToWorld(event.offsetX, event.offsetY);
    const hoveredNode = findLocalNodeAtPoint(point.x, point.y);
    if (hoveredNode !== state.hoveredNode) {
      state.hoveredNode = hoveredNode;
      state.canvas.classList.toggle("hovering-node", Boolean(hoveredNode));
      drawLocalGraph();
    }
  };

  window.addEventListener("mouseup", () => {
    if (!localGraphState) return;
    localGraphState.dragging = false;
    localGraphState.canvas.classList.remove("panning");
  });

  state.canvas.onmouseleave = () => {
    state.hoveredNode = null;
    state.dragging = false;
    state.canvas.classList.remove("hovering-node", "panning");
    drawLocalGraph();
  };
}

function zoomLocalGraph(factor) {
  const state = localGraphState;
  const previousScale = state.viewport.scale;
  const nextScale = Math.max(0.14, Math.min(3.2, previousScale * factor));
  const centerX = state.screenWidth / 2;
  const centerY = state.screenHeight / 2;
  const worldCenterX = (centerX - state.viewport.offsetX) / previousScale;
  const worldCenterY = (centerY - state.viewport.offsetY) / previousScale;
  state.viewport.scale = nextScale;
  state.viewport.offsetX = centerX - worldCenterX * nextScale;
  state.viewport.offsetY = centerY - worldCenterY * nextScale;
}

function fitLocalGraphToScreen() {
  const state = localGraphState;
  const scale = Math.min(state.screenWidth / state.worldWidth, state.screenHeight / state.worldHeight) * 0.96;
  state.viewport.scale = scale;
  state.viewport.offsetX = (state.screenWidth - state.worldWidth * scale) / 2;
  state.viewport.offsetY = (state.screenHeight - state.worldHeight * scale) / 2;
}

function localScreenToWorld(x, y) {
  const state = localGraphState;
  return {
    x: (x - state.viewport.offsetX) / state.viewport.scale,
    y: (y - state.viewport.offsetY) / state.viewport.scale,
  };
}

function findLocalNodeAtPoint(x, y) {
  const state = localGraphState;
  for (let index = state.nodes.length - 1; index >= 0; index -= 1) {
    const node = state.nodes[index];
    const radius = renderedNodeRadius(node) + 6 / state.viewport.scale;
    const dx = x - node.x;
    const dy = y - node.y;
    if (dx * dx + dy * dy <= radius * radius) return node;
  }
  return null;
}

function drawLocalGraph() {
  const state = localGraphState;
  const { context, viewport } = state;
  context.clearRect(0, 0, state.screenWidth, state.screenHeight);
  context.fillStyle = "#050a13";
  context.fillRect(0, 0, state.screenWidth, state.screenHeight);
  context.save();
  context.translate(viewport.offsetX, viewport.offsetY);
  context.scale(viewport.scale, viewport.scale);

  const hoveredNode = state.hoveredNode;
  const highlightedIds = highlightedNodeIds(state, hoveredNode);
  context.lineWidth = hoveredNode ? 1.6 : 1.2;
  state.edges.forEach((edge) => {
    const highlighted = hoveredNode && (edge.sourceNode.id === hoveredNode.id || edge.targetNode.id === hoveredNode.id);
    context.beginPath();
    context.strokeStyle = graphEdgeColor(edge, highlighted, Boolean(hoveredNode));
    context.moveTo(edge.sourceNode.x, edge.sourceNode.y);
    context.lineTo(edge.targetNode.x, edge.targetNode.y);
    context.stroke();
  });

  state.nodes.forEach((node) => {
    const highlighted = !hoveredNode || highlightedIds.has(node.id);
    const isFocus = node.id === state.focusId;
    const radius = renderedNodeRadius(node) + (node === hoveredNode ? 4 : 0) + (isFocus ? 3 : 0);
    context.beginPath();
    context.fillStyle = isFocus ? "#22d3ee" : graphNodeColor(node, highlighted);
    context.arc(node.x, node.y, radius, 0, Math.PI * 2);
    context.fill();

    if (node.group === "tag" || isFocus || node === hoveredNode) {
      context.fillStyle = node === hoveredNode || isFocus ? "rgba(248,250,252,0.94)" : "rgba(34,211,238,0.78)";
      context.font = isFocus ? "700 13px Segoe UI, sans-serif" : "12px Segoe UI, sans-serif";
      context.fillText(node === hoveredNode ? node.label : truncateLabel(node.label, 34), node.x + radius + 6, node.y + 4);
    }
  });

  context.restore();
}

let graphAnimationFrame = null;
let graphViewport = {
  scale: 1,
  offsetX: 0,
  offsetY: 0,
};
let currentGraphRender = null;
let graphInteraction = {
  dragging: false,
  lastX: 0,
  lastY: 0,
  hoveredNode: null,
};
let localGraphState = null;

function renderGraph(graph) {
  const canvas = document.getElementById("graph-canvas");
  const context = canvas.getContext("2d");
  const status = document.querySelector(".graph-status");
  const nodes = graph.nodes || [];
  const edges = graph.edges || [];

  if (graphAnimationFrame) {
    cancelAnimationFrame(graphAnimationFrame);
  }

  if (!nodes.length) {
    context.clearRect(0, 0, canvas.width, canvas.height);
    if (status) status.textContent = "Nenhum item encontrado para montar o grafo.";
    return;
  }

  if (status) {
    const notes = nodes.filter((node) => node.group === "note").length;
    const tags = nodes.filter((node) => node.group === "tag").length;
    status.textContent = `${notes} artigos, ${tags} tags, ${edges.length} conexoes`;
  }

  const graphBox = document.getElementById("graph");
  const simulation = createForceLayout(nodes, edges);

  function resizeCanvas() {
    const rect = graphBox.getBoundingClientRect();
    const ratio = window.devicePixelRatio || 1;
    const mobile = window.matchMedia("(max-width: 760px)").matches;
    const screenWidth = Math.max(mobile ? 300 : 640, rect.width);
    const screenHeight = Math.max(mobile ? 520 : 680, rect.height);
    canvas.width = screenWidth * ratio;
    canvas.height = screenHeight * ratio;
    canvas.style.width = `${screenWidth}px`;
    canvas.style.height = `${screenHeight}px`;
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
    simulation.screenWidth = screenWidth;
    simulation.screenHeight = screenHeight;
    simulation.worldWidth = Math.max(screenWidth, 620 + nodes.length * 6.2);
    simulation.worldHeight = Math.max(screenHeight, 520 + nodes.length * 3.8);
    simulation.layout();
    fitGraphToScreen(simulation);
  }

  resizeCanvas();
  window.addEventListener("resize", resizeCanvas, { once: true });
  currentGraphRender = () => drawForceGraph(context, simulation, graphViewport);
  bindGraphControls(canvas, simulation);
  drawForceGraph(context, simulation, graphViewport);
}

function bindGraphControls(canvas, simulation) {
  document.querySelectorAll("[data-graph-zoom]").forEach((button) => {
    button.onclick = () => {
      const action = button.dataset.graphZoom;
      if (action === "in") zoomGraph(simulation, 1.18);
      if (action === "out") zoomGraph(simulation, 1 / 1.18);
      if (action === "reset") fitGraphToScreen(simulation);
      currentGraphRender?.();
    };
  });

  canvas.onwheel = (event) => {
    event.preventDefault();
    const direction = event.deltaY < 0 ? 1.08 : 1 / 1.08;
    zoomGraph(simulation, direction);
    currentGraphRender?.();
  };

  canvas.onmousedown = (event) => {
    graphInteraction.dragging = true;
    graphInteraction.lastX = event.clientX;
    graphInteraction.lastY = event.clientY;
    canvas.classList.add("panning");
  };

  window.onmouseup = () => {
    graphInteraction.dragging = false;
    canvas.classList.remove("panning");
  };

  canvas.onmousemove = (event) => {
    if (graphInteraction.dragging) {
      graphViewport.offsetX += event.clientX - graphInteraction.lastX;
      graphViewport.offsetY += event.clientY - graphInteraction.lastY;
      graphInteraction.lastX = event.clientX;
      graphInteraction.lastY = event.clientY;
      currentGraphRender?.();
      return;
    }

    const point = screenToWorld(event.offsetX, event.offsetY);
    const hoveredNode = findNodeAtPoint(simulation, point.x, point.y);
    if (hoveredNode !== graphInteraction.hoveredNode) {
      graphInteraction.hoveredNode = hoveredNode;
      canvas.classList.toggle("hovering-node", Boolean(hoveredNode));
      currentGraphRender?.();
    }
  };

  canvas.onmouseleave = () => {
    graphInteraction.hoveredNode = null;
    graphInteraction.dragging = false;
    canvas.classList.remove("hovering-node", "panning");
    currentGraphRender?.();
  };
}

function zoomGraph(simulation, factor) {
  const previousScale = graphViewport.scale;
  const nextScale = Math.max(0.08, Math.min(2.8, previousScale * factor));
  if (!previousScale) {
    fitGraphToScreen(simulation);
    return;
  }
  const centerX = simulation.screenWidth / 2;
  const centerY = simulation.screenHeight / 2;
  const worldCenterX = (centerX - graphViewport.offsetX) / previousScale;
  const worldCenterY = (centerY - graphViewport.offsetY) / previousScale;
  graphViewport.scale = nextScale;
  graphViewport.offsetX = centerX - worldCenterX * nextScale;
  graphViewport.offsetY = centerY - worldCenterY * nextScale;
}

function fitGraphToScreen(simulation) {
  const scale = Math.min(
    simulation.screenWidth / simulation.worldWidth,
    simulation.screenHeight / simulation.worldHeight,
  ) * 0.96;
  graphViewport.scale = scale;
  graphViewport.offsetX = (simulation.screenWidth - simulation.worldWidth * scale) / 2;
  graphViewport.offsetY = (simulation.screenHeight - simulation.worldHeight * scale) / 2;
}

function screenToWorld(x, y) {
  return {
    x: (x - graphViewport.offsetX) / graphViewport.scale,
    y: (y - graphViewport.offsetY) / graphViewport.scale,
  };
}

function findNodeAtPoint(simulation, x, y) {
  for (let index = simulation.nodes.length - 1; index >= 0; index -= 1) {
    const node = simulation.nodes[index];
    const radius = renderedNodeRadius(node) + 5 / graphViewport.scale;
    const dx = x - node.x;
    const dy = y - node.y;
    if (dx * dx + dy * dy <= radius * radius) {
      return node;
    }
  }
  return null;
}

function truncateLabel(label, maxLength) {
  if (label.length <= maxLength) return label;
  return `${label.slice(0, maxLength - 3)}...`;
}

function createForceLayout(nodes, edges) {
  const simulationNodes = nodes.map((node, index) => {
    const seed = hashString(node.id);
    const angle = (index * Math.PI * (3 - Math.sqrt(5))) + (seed % 100) * 0.01;
    const radius = 120 + Math.sqrt(index + 1) * 26;
    return {
      ...node,
      x: 900 + Math.cos(angle) * radius,
      y: 550 + Math.sin(angle) * radius,
      vx: 0,
      vy: 0,
      degree: 0,
      radius: node.group === "tag" ? 5.5 : 3.4,
    };
  });
  const nodeById = new Map(simulationNodes.map((node) => [node.id, node]));
  const simulationEdges = edges
    .map((edge) => ({
      ...edge,
      sourceNode: nodeById.get(edge.source),
      targetNode: nodeById.get(edge.target),
    }))
    .filter((edge) => edge.sourceNode && edge.targetNode);
  simulationEdges.forEach((edge) => {
    edge.sourceNode.degree += 1;
    edge.targetNode.degree += 1;
  });

  return {
    nodes: simulationNodes,
    edges: simulationEdges,
    screenWidth: 900,
    screenHeight: 680,
    worldWidth: 1800,
    worldHeight: 1100,
    layout() {
      const centerX = this.worldWidth / 2;
      const centerY = this.worldHeight / 2;
      const iterations = 760;

      for (let step = 0; step < iterations; step += 1) {
        const cooling = 1 - step / iterations;
        const repulsion = 9000 * cooling + 900;
        const spring = 0.012 * cooling + 0.0028;

        for (let i = 0; i < this.nodes.length; i += 1) {
          const a = this.nodes[i];
          for (let j = i + 1; j < this.nodes.length; j += 1) {
            const b = this.nodes[j];
            const dx = b.x - a.x || 0.01;
            const dy = b.y - a.y || 0.01;
            const distanceSq = Math.max(36, dx * dx + dy * dy);
            const distance = Math.sqrt(distanceSq);
            const force = repulsion / distanceSq;
            const fx = (dx / distance) * force;
            const fy = (dy / distance) * force;
            a.vx -= fx;
            a.vy -= fy;
            b.vx += fx;
            b.vy += fy;
          }
        }

        this.edges.forEach((edge) => {
          const source = edge.sourceNode;
          const target = edge.targetNode;
          const dx = target.x - source.x;
          const dy = target.y - source.y;
          const distance = Math.sqrt(dx * dx + dy * dy) || 1;
          const desired = edge.type === "linked" ? 86 : 112;
          const force = (distance - desired) * spring;
          const fx = (dx / distance) * force;
          const fy = (dy / distance) * force;
          source.vx += fx;
          source.vy += fy;
          target.vx -= fx;
          target.vy -= fy;
        });

        this.nodes.forEach((node) => {
          const centerForce = node.degree ? 0.0018 : 0.0008;
          node.vx += (centerX - node.x) * centerForce;
          node.vy += (centerY - node.y) * centerForce;
          node.vx *= 0.72;
          node.vy *= 0.72;
          node.x += Math.max(-18, Math.min(18, node.vx));
          node.y += Math.max(-18, Math.min(18, node.vy));
        });
      }

      fitLayoutToWorld(this);
    },
  };
}

function drawForceGraph(context, simulation, viewport) {
  context.clearRect(0, 0, simulation.screenWidth, simulation.screenHeight);
  context.fillStyle = "#050a13";
  context.fillRect(0, 0, simulation.screenWidth, simulation.screenHeight);
  context.save();
  context.translate(viewport.offsetX, viewport.offsetY);
  context.scale(viewport.scale, viewport.scale);

  const hoveredNode = graphInteraction.hoveredNode;
  const highlightedIds = highlightedNodeIds(simulation, hoveredNode);

  context.lineWidth = hoveredNode ? 1.5 : 1;
  simulation.edges.forEach((edge) => {
    const highlighted = hoveredNode && (edge.sourceNode.id === hoveredNode.id || edge.targetNode.id === hoveredNode.id);
    context.beginPath();
    context.strokeStyle = graphEdgeColor(edge, highlighted, Boolean(hoveredNode));
    context.moveTo(edge.sourceNode.x, edge.sourceNode.y);
    context.lineTo(edge.targetNode.x, edge.targetNode.y);
    context.stroke();
  });

  context.font = "12px Segoe UI, sans-serif";
  simulation.nodes.forEach((node) => {
    const highlighted = !hoveredNode || highlightedIds.has(node.id);
    const radius = renderedNodeRadius(node) + (node === hoveredNode ? 4 : 0);
    context.beginPath();
    context.fillStyle = graphNodeColor(node, highlighted);
    context.arc(node.x, node.y, radius, 0, Math.PI * 2);
    context.fill();

    if (node.group === "tag" || node.degree > 8 || node === hoveredNode) {
      context.fillStyle = node === hoveredNode
        ? "rgba(248, 250, 252, 0.94)"
        : node.group === "tag" ? "rgba(217, 70, 239, 0.46)" : "rgba(34, 211, 238, 0.22)";
      context.fillText(node === hoveredNode ? node.label : truncateLabel(node.label, 30), node.x + radius + 5, node.y + 4);
    }
  });
  context.restore();
}

function renderedNodeRadius(node) {
  return node.radius + Math.min(6, Math.sqrt(node.degree) * 0.85);
}

function highlightedNodeIds(simulation, hoveredNode) {
  if (!hoveredNode) return new Set();
  const ids = new Set([hoveredNode.id]);
  simulation.edges.forEach((edge) => {
    if (edge.sourceNode.id === hoveredNode.id) ids.add(edge.targetNode.id);
    if (edge.targetNode.id === hoveredNode.id) ids.add(edge.sourceNode.id);
  });
  return ids;
}

function graphEdgeColor(edge, highlighted, hasHover) {
  if (highlighted) {
    return edge.type === "linked" ? "rgba(34, 211, 238, 0.88)" : "rgba(217, 70, 239, 0.90)";
  }
  if (hasHover) {
    return edge.type === "linked" ? "rgba(34, 211, 238, 0.08)" : "rgba(217, 70, 239, 0.08)";
  }
  return edge.type === "linked" ? "rgba(34, 211, 238, 0.28)" : "rgba(217, 70, 239, 0.24)";
}

function graphNodeColor(node, highlighted) {
  if (highlighted) {
    return node.group === "tag" ? "#d946ef" : "#5b6cff";
  }
  return node.group === "tag" ? "rgba(217, 70, 239, 0.26)" : "rgba(91, 108, 255, 0.30)";
}

function fitLayoutToWorld(simulation) {
  const padding = 90;
  const minX = Math.min(...simulation.nodes.map((node) => node.x));
  const maxX = Math.max(...simulation.nodes.map((node) => node.x));
  const minY = Math.min(...simulation.nodes.map((node) => node.y));
  const maxY = Math.max(...simulation.nodes.map((node) => node.y));
  const layoutWidth = Math.max(1, maxX - minX);
  const layoutHeight = Math.max(1, maxY - minY);
  const scale = Math.min(
    (simulation.worldWidth - padding * 2) / layoutWidth,
    (simulation.worldHeight - padding * 2) / layoutHeight,
    1.18,
  );
  const offsetX = (simulation.worldWidth - layoutWidth * scale) / 2 - minX * scale;
  const offsetY = (simulation.worldHeight - layoutHeight * scale) / 2 - minY * scale;

  simulation.nodes.forEach((node) => {
    node.x = node.x * scale + offsetX;
    node.y = node.y * scale + offsetY;
  });
}

function hashString(value) {
  let hash = 0;
  for (let index = 0; index < value.length; index += 1) {
    hash = (hash << 5) - hash + value.charCodeAt(index);
    hash |= 0;
  }
  return Math.abs(hash);
}
