const API = "http://localhost:8000";
const markers = {};
let map;

// Init map centered on NYC/NJ area
window.addEventListener("DOMContentLoaded", () => {
  map = L.map("map").setView([40.73, -74.02], 10);
  L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
    attribution: "© CartoDB",
    maxZoom: 19,
  }).addTo(map);
  loadAll();
});

const severityColor = { high: "#ef4444", medium: "#f59e0b", low: "#10b981" };

function makeIcon(severity, duplicate) {
  const color = duplicate ? "#6b7280" : severityColor[severity] || "#60a5fa";
  return L.divIcon({
    className: "",
    html: `<div style="width:14px;height:14px;border-radius:50%;background:${color};border:2px solid #fff;box-shadow:0 0 6px ${color}88"></div>`,
    iconSize: [14, 14],
    iconAnchor: [7, 7],
  });
}

async function submitReport() {
  const text = document.getElementById("report-input").value.trim();
  if (!text) return;
  const btn = document.getElementById("submit-btn");
  btn.textContent = "Processing…";
  btn.disabled = true;
  showResult("", false);

  try {
    const res = await fetch(`${API}/process`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Error");

    showResult(
      `✓ Extracted: ${data.incident_type} @ ${data.formatted_address}\nSeverity: ${data.severity} | ${data.duplicate ? "⚠ Merged with existing" : "New unique incident"}`,
      false
    );
    addMarker(data);
    addCard(data);
    await refreshStats();
    document.getElementById("report-input").value = "";
  } catch (e) {
    showResult(`✗ ${e.message}`, true);
  } finally {
    btn.textContent = "⚡ Process report";
    btn.disabled = false;
  }
}

async function clearAll() {
  await fetch(`${API}/incidents`, { method: "DELETE" });
  Object.values(markers).forEach(m => map.removeLayer(m));
  Object.keys(markers).forEach(k => delete markers[k]);
  document.getElementById("incident-list").innerHTML = "";
  await refreshStats();
  showResult("", false);
}

async function loadAll() {
  const res = await fetch(`${API}/incidents`);
  const list = await res.json();
  list.forEach(i => { addMarker(i); addCard(i); });
  await refreshStats();
}

function addMarker(incident) {
  if (markers[incident.id]) return;
  const m = L.marker([incident.lat, incident.lng], { icon: makeIcon(incident.severity, incident.duplicate) })
    .addTo(map)
    .bindPopup(`
      <b>${incident.incident_type.replace("_", " ").toUpperCase()}</b><br>
      ${incident.formatted_address}<br>
      Severity: ${incident.severity}<br>
      ${incident.summary}<br>
      <small>ID: ${incident.id} ${incident.duplicate ? "· merged" : ""}</small>
    `);
  markers[incident.id] = m;
}

function addCard(incident) {
  const list = document.getElementById("incident-list");
  const card = document.createElement("div");
  card.className = `incident-card${incident.duplicate ? " dup" : ""}`;
  card.style.borderLeftColor = incident.duplicate ? "#374151" : severityColor[incident.severity] || "#60a5fa";
  card.innerHTML = `<div class="ic-type">${incident.incident_type.replace("_", " ")} ${incident.duplicate ? "· duplicate" : ""}</div>
    <div class="ic-loc">${incident.formatted_address}</div>`;
  card.onclick = () => { map.setView([incident.lat, incident.lng], 14); markers[incident.id]?.openPopup(); };
  list.prepend(card);
}

async function refreshStats() {
  const res = await fetch(`${API}/stats`);
  const s = await res.json();
  document.getElementById("stat-total").textContent = s.total;
  document.getElementById("stat-unique").textContent = s.unique;
  document.getElementById("stat-merged").textContent = s.duplicates_merged;
  const total = s.total || 1;
  document.getElementById("bar-high").style.width = ((s.by_severity.high / total) * 100) + "%";
  document.getElementById("bar-medium").style.width = ((s.by_severity.medium / total) * 100) + "%";
  document.getElementById("bar-low").style.width = ((s.by_severity.low / total) * 100) + "%";
}

function showResult(msg, isError) {
  const box = document.getElementById("result-box");
  if (!msg) { box.classList.add("hidden"); return; }
  box.textContent = msg;
  box.className = `result-box${isError ? " error" : ""}`;
}