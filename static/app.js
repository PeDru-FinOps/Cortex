const tabs = document.querySelectorAll(".tab");
const views = document.querySelectorAll(".view");
const appShell = document.querySelector(".app-shell");

setupSidebar();
setupTreeDragAndDrop();
setupConfirmForms();
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
  const collapsed = localStorage.getItem("cortex.sidebarCollapsed") === "1";

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
  const markdownFiles = files.filter((file) => file.name.toLowerCase().endsWith(".md"));
  if (!markdownFiles.length) return;

  const formData = new FormData();
  markdownFiles.forEach((file) => {
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
  const width = Math.max(520, rect.width || 720);
  const height = 320;
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
    context.fillStyle = "#1f1f1f";
    context.fillRect(0, 0, width, height);
    if (status) status.textContent = "Sem conexoes diretas";
    context.fillStyle = "rgba(255, 255, 255, 0.62)";
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
  context.fillStyle = "#1f1f1f";
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
    context.fillStyle = isFocus ? "#ffffff" : graphNodeColor(node, highlighted);
    context.arc(node.x, node.y, radius, 0, Math.PI * 2);
    context.fill();

    if (node.group === "tag" || isFocus || node === hoveredNode) {
      context.fillStyle = node === hoveredNode || isFocus ? "rgba(255,255,255,0.92)" : "rgba(74,222,128,0.72)";
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
    const screenWidth = Math.max(640, rect.width);
    const screenHeight = Math.max(680, rect.height);
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
  context.fillStyle = "#1f1f1f";
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
        ? "rgba(255, 255, 255, 0.92)"
        : node.group === "tag" ? "rgba(74, 222, 128, 0.30)" : "rgba(209, 213, 219, 0.16)";
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
    return edge.type === "linked" ? "rgba(255, 255, 255, 0.82)" : "rgba(74, 222, 128, 0.88)";
  }
  if (hasHover) {
    return edge.type === "linked" ? "rgba(210, 210, 210, 0.06)" : "rgba(74, 222, 128, 0.05)";
  }
  return edge.type === "linked" ? "rgba(210, 210, 210, 0.30)" : "rgba(74, 222, 128, 0.22)";
}

function graphNodeColor(node, highlighted) {
  if (highlighted) {
    return node.group === "tag" ? "#4ade80" : "#d1d5db";
  }
  return node.group === "tag" ? "rgba(74, 222, 128, 0.22)" : "rgba(209, 213, 219, 0.22)";
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
