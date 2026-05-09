const API_BASE = `${window.location.origin}/api`;
const DASHBOARD_KEY_STORAGE = "chriz_dashboard_internal_key";

let currentUser = { username: "Admin", role: "admin" };
let cachedChannels = [];

const routes = {
    "#overview": renderOverview,
    "#moderation": renderModeration,
    "#tickets": renderTickets,
    "#minecraft": renderMinecraft,
    "#broadcast": renderBroadcast,
    "#ai": renderAI,
    "#settings": renderSettings,
};

window.addEventListener("hashchange", handleRouting);
window.addEventListener("load", async () => {
    if (!window.location.hash) window.location.hash = "#overview";
    handleRouting();
    updateSystemTime();
    setInterval(updateSystemTime, 1000);
});

function handleRouting() {
    const hash = window.location.hash || "#overview";
    const renderFunc = routes[hash];

    document.querySelectorAll("nav a").forEach((link) => {
        link.classList.remove("active");
        if (link.getAttribute("href") === hash) link.classList.add("active");
    });

    const title = hash.replace("#", "");
    document.getElementById("page-title").innerText = title.charAt(0).toUpperCase() + title.slice(1);

    if (renderFunc) renderFunc();
}

function getDashboardKey() {
    return localStorage.getItem(DASHBOARD_KEY_STORAGE) || "";
}

function setDashboardKey(value) {
    localStorage.setItem(DASHBOARD_KEY_STORAGE, value);
}

function buildHeaders(includeJson = false) {
    const headers = {};
    const key = getDashboardKey();
    if (key) headers["X-Internal-API-Key"] = key;
    if (includeJson) headers["Content-Type"] = "application/json";
    return headers;
}

async function fetchJson(path, options = {}) {
    const response = await fetch(`${API_BASE}${path}`, options);
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
        throw new Error(data.detail || "Request failed");
    }
    return data;
}

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
            <h3>Dashboard Access</h3>
            <p class="muted">This dashboard is now served directly by FastAPI. Use the Broadcast tab for bot-sent announcements.</p>
        </div>
    `;

    try {
        const data = await fetchJson("/state");
        const statusEl = document.getElementById("status-val");
        statusEl.innerText = (data.status || "unknown").toUpperCase();
        statusEl.style.color = data.status === "online" ? "var(--success)" : "var(--danger)";

        document.getElementById("players-val").innerText = data.live_players || 0;
        document.getElementById("tickets-val").innerText = data.active_tickets || 0;

        const tokens = data.total_tokens || 0;
        document.getElementById("tokens-val").innerText = tokens > 1000 ? `${(tokens / 1000).toFixed(1)}k` : tokens;
    } catch (error) {
        document.getElementById("status-val").innerText = "ERROR";
        console.error(error);
    }
}

function renderModeration() {
    document.getElementById("main-view").innerHTML = `<h3>Moderation Logs</h3><p class="muted">Coming soon: interactive log viewer and search.</p>`;
}

function renderTickets() {
    document.getElementById("main-view").innerHTML = `<h3>Active Support Tickets</h3><p class="muted">Coming soon: AI ticket summarization and chat view.</p>`;
}

function renderMinecraft() {
    document.getElementById("main-view").innerHTML = `
        <div class="card">
            <h3>Minecraft Controls</h3>
            <p class="muted">Operational quick actions can be added next once the dashboard message flow is stable.</p>
        </div>
    `;
}

async function renderBroadcast() {
    const mainView = document.getElementById("main-view");
    mainView.innerHTML = `
        <div class="card">
            <h3>Bot Broadcast</h3>
            <p class="muted">Send a message through the Discord bot, optionally mention everyone or here, and pin it.</p>
            <div class="form-grid">
                <label>
                    <span>Internal API Key</span>
                    <input type="password" id="internal-key" placeholder="Paste INTERNAL_API_KEY">
                </label>
                <label>
                    <span>Channel</span>
                    <select id="channel-select">
                        <option value="">Loading channels...</option>
                    </select>
                </label>
            </div>
            <label class="full-width">
                <span>Message</span>
                <textarea id="broadcast-content" rows="6" placeholder="Type the announcement or pinned message here"></textarea>
            </label>
            <div class="checkbox-row">
                <label><input type="checkbox" id="mention-everyone"> Mention @everyone</label>
                <label><input type="checkbox" id="mention-here"> Mention @here</label>
                <label><input type="checkbox" id="pin-message"> Pin message</label>
            </div>
            <div class="action-row">
                <button id="save-key-btn" class="secondary-btn">Save Key</button>
                <button id="refresh-channels-btn" class="secondary-btn">Refresh Channels</button>
                <button id="send-broadcast-btn">Send Through Bot</button>
            </div>
            <div id="broadcast-status" class="status-box"></div>
        </div>
    `;

    const keyInput = document.getElementById("internal-key");
    keyInput.value = getDashboardKey();

    document.getElementById("save-key-btn").addEventListener("click", () => {
        setDashboardKey(keyInput.value.trim());
        setStatus("broadcast-status", "API key saved locally in this browser.", "success");
    });

    document.getElementById("refresh-channels-btn").addEventListener("click", async () => {
        setDashboardKey(keyInput.value.trim());
        await loadChannels();
    });

    document.getElementById("send-broadcast-btn").addEventListener("click", async () => {
        setDashboardKey(keyInput.value.trim());
        await sendBroadcast();
    });

    await loadChannels();
}

function renderAI() {
    document.getElementById("main-view").innerHTML = `<h3>AI Console</h3><p class="muted">Coming soon: direct chat interface with context visualizer.</p>`;
}

function renderSettings() {
    document.getElementById("main-view").innerHTML = `
        <div class="card">
            <h3>Settings</h3>
            <p class="muted">Current dashboard API base: <code>${API_BASE}</code></p>
        </div>
    `;
}

async function loadChannels() {
    const select = document.getElementById("channel-select");
    if (!select) return;

    select.innerHTML = `<option value="">Loading channels...</option>`;

    try {
        const data = await fetchJson("/dashboard/channels", {
            headers: buildHeaders(),
        });
        cachedChannels = data.channels || [];

        if (!cachedChannels.length) {
            select.innerHTML = `<option value="">No sendable text channels found</option>`;
            return;
        }

        select.innerHTML = cachedChannels
            .map((channel) => `<option value="${channel.id}">#${channel.name}</option>`)
            .join("");
        setStatus("broadcast-status", `Loaded ${cachedChannels.length} channels.`, "success");
    } catch (error) {
        select.innerHTML = `<option value="">Unable to load channels</option>`;
        setStatus("broadcast-status", error.message, "error");
    }
}

async function sendBroadcast() {
    const channelId = document.getElementById("channel-select")?.value;
    const content = document.getElementById("broadcast-content")?.value.trim();
    const mentionEveryone = document.getElementById("mention-everyone")?.checked;
    const mentionHere = document.getElementById("mention-here")?.checked;
    const pinMessage = document.getElementById("pin-message")?.checked;

    if (!channelId) {
        setStatus("broadcast-status", "Choose a channel first.", "error");
        return;
    }

    if (!content) {
        setStatus("broadcast-status", "Message content is required.", "error");
        return;
    }

    try {
        const data = await fetchJson("/dashboard/message", {
            method: "POST",
            headers: buildHeaders(true),
            body: JSON.stringify({
                channel_id: Number(channelId),
                content,
                mention_everyone: Boolean(mentionEveryone),
                mention_here: Boolean(mentionHere),
                pin_message: Boolean(pinMessage),
            }),
        });

        setStatus(
            "broadcast-status",
            `Message sent successfully. Open: ${data.jump_url}`,
            "success"
        );
    } catch (error) {
        setStatus("broadcast-status", error.message, "error");
    }
}

function setStatus(id, text, kind) {
    const element = document.getElementById(id);
    if (!element) return;
    element.textContent = text;
    element.className = `status-box ${kind}`;
}

function updateSystemTime() {
    const now = new Date();
    document.getElementById("system-time").innerText = now.toLocaleString();
}
