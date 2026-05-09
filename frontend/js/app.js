// app.js - CHRIZ__3656 AI Dashboard Logic

const API_BASE = "http://localhost:8001/api";
let currentUser = { username: "Admin", role: "admin" };

// --- Routing ---
const routes = {
    "#overview": renderOverview,
    "#moderation": renderModeration,
    "#tickets": renderTickets,
    "#minecraft": renderMinecraft,
    "#ai": renderAI,
    "#settings": renderSettings
};

window.addEventListener("hashchange", handleRouting);
window.addEventListener("load", () => {
    if (!window.location.hash) window.location.hash = "#overview";
    handleRouting();
    updateSystemTime();
    setInterval(updateSystemTime, 1000);
});

function handleRouting() {
    const hash = window.location.hash || "#overview";
    const renderFunc = routes[hash];
    
    // Update active nav link
    document.querySelectorAll("nav a").forEach(link => {
        link.classList.remove("active");
        if (link.getAttribute("href") === hash) link.classList.add("active");
    });

    // Update page title
    const title = hash.replace("#", "").charAt(0).toUpperCase() + hash.slice(2);
    document.getElementById("page-title").innerText = title;

    if (renderFunc) renderFunc();
}

// --- Renderers ---

async function renderOverview() {
    const mainView = document.getElementById("main-view");
    mainView.innerHTML = `
        <div class="card-grid">
            <div class="card"><h3>Server Status</h3><div class="value" id="status-val">...</div></div>
            <div class="card"><h3>Online Players</h3><div class="value" id="players-val">0</div></div>
            <div class="card"><h3>Active Tickets</h3><div class="value" id="tickets-val">0</div></div>
            <div class="card"><h3>AI Usage (Tokens)</h3><div class="value" id="tokens-val">0</div></div>
        </div>
        <div class="recent-activity card">
            <h3>Recent System Logs</h3>
            <div id="logs-container">
                <p>Fetching logs...</p>
            </div>
        </div>
    `;
    
    // Fetch live data from API
    try {
        const resp = await fetch(`${API_BASE}/state`);
        const data = await resp.json();
        
        // Update Status Card
        const statusEl = document.getElementById("status-val");
        statusEl.innerText = data.status.toUpperCase();
        statusEl.style.color = data.status === "online" ? "var(--success)" : "var(--danger)";
        
        // Update Metrics
        document.getElementById("players-val").innerText = data.live_players || 0;
        document.getElementById("tickets-val").innerText = data.active_tickets || 0;
        
        // Format token count (e.g. 1500 -> 1.5k)
        const tokens = data.total_tokens || 0;
        document.getElementById("tokens-val").innerText = tokens > 1000 ? (tokens/1000).toFixed(1) + "k" : tokens;

    } catch (e) { 
        console.error("Failed to fetch state", e);
        document.getElementById("status-val").innerText = "ERROR";
    }
}

function renderModeration() {
    document.getElementById("main-view").innerHTML = `<h3>Moderation Logs</h3><p>Coming soon: Interactive log viewer and search.</p>`;
}

function renderTickets() {
    document.getElementById("main-view").innerHTML = `<h3>Active Support Tickets</h3><p>Coming soon: AI ticket summarization and chat view.</p>`;
}

function renderMinecraft() {
    document.getElementById("main-view").innerHTML = `
        <div class="card-grid">
            <div class="card"><h3>TPS</h3><div class="value">19.95</div></div>
            <div class="card"><h3>RAM</h3><div class="value">2.4 GB</div></div>
        </div>
        <div class="card">
            <h3>Quick Actions</h3>
            <div style="margin-top: 1rem; display: flex; gap: 1rem;">
                <button>Restart Server</button>
                <button>Backup World</button>
                <button style="border-color: var(--danger); color: var(--danger);">Stop Server</button>
            </div>
        </div>
    `;
}

function renderAI() {
    document.getElementById("main-view").innerHTML = `<h3>AI Console</h3><p>Coming soon: Direct chat interface with context visualizer.</p>`;
}

function renderSettings() {
    document.getElementById("main-view").innerHTML = `<h3>System Settings</h3><p>Manage providers, API keys, and server preferences.</p>`;
}

// --- Helpers ---

function updateSystemTime() {
    const now = new Date();
    document.getElementById("system-time").innerText = now.toLocaleString();
}
