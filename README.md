# CHRIZ__3656 AI — Master Operational Assistant 🌌

**CHRIZ__3656 AI** is a professional-grade, tool-first AI operations platform designed to manage Minecraft Bedrock servers, Discord communities, and automated infrastructure workflows. 

It is powered by a **Four-Mode Master Orchestrator** that intelligently switches between natural social interaction, factual grounding, secure action execution, and multi-step workflow automation.

---

## 🚀 Current Status: **STABILIZED & UNIFIED**
The platform is now **Production-Hardened** and fully unified with the **SkyRealm Official Community Bot**. It serves as the central operational brain for the entire ecosystem.

| Component | Status | Description |
|---|---|---|
| **Master Router** | ✅ Stable | LLM-based intent classification (Workflow/Action/Fact/Social). |
| **Official Bridge**| ✅ Active | Secure API connection to the live VPS Official Bot. |
| **Action Engine** | ✅ Active | Secure Discord/Minecraft command execution with RBAC. |
| **Workflow Mgr** | ✅ Active | Multi-step task planning (e.g. Maintenance/Restarts). |
| **Pterodactyl** | ✅ Integrated| Direct power control and metrics via Panel Client API. |
| **Social Layer** | ✅ Natural | Conversations in Manglish with zero technical leakage. |
| **MC RCON** | ✅ Stable | Robust async connection management for server control. |

---

## 🧠 Master Orchestration Architecture

The system uses a **Priority-Based Routing** model:

1.  **WORKFLOW MODE:** For complex, multi-step requests (e.g., "announce and restart").
2.  **ACTION MODE:** For single executable commands (e.g., "mute @user", "review whitelist").
3.  **FACTUAL MODE:** For server data retrieval (e.g., player counts, rules).
4.  **SOCIAL MODE:** For casual chatting and community banter.

---

## 🛠️ Key Features

### 1. Unified Community Ecosystem
- **Official Bot Integration:** Bridged with the live VPS bot (`skybot.skyrealm.fun`) to fetch whitelist applications and community analytics.
- **Secure Handshake:** Uses a private `INTERNAL_API_KEY` to bypass Discord OAuth for administrative AI tasks.
- **Pterodactyl Integration:** Replaces generic commands with official Panel API calls for server restarts and health monitoring.

### 2. Social Personality & Humanizer
- **Manglish Naturalization:** Speaks casual gamer-style Manglish (70% English / 30% Slang).
- **Zero Terminology Leakage:** A post-processing layer strips technical jargon (e.g., "REAL-TIME CONTEXT") and translates it into natural social language.
- **Rolling Memory:** Remembers channel context across 20+ messages for deep immersion.

### 3. Infrastructure & Moderation
- **Task Planning:** Automatically breaks complex requests into logical execution steps.
- **RBAC Security:** AI actions are strictly validated against real Discord roles (Admin/Moderator).
- **Live Monitor:** Real-time Dashboard tracking Players, Tickets, and AI Token usage.

---

## 📁 Project Structure
```text
/CHRIZ3656
├── ai/                # Master Router, Action Engine, Workflow Mgr, Humanizer
├── api/               # FastAPI routers (Live Metrics, Dashboard API)
├── bot/               # discord.py Cogs and Social Trigger system
├── core/              # Config, DB Repositories, & Workflow runners
├── frontend/          # Vanilla JS dashboard (Real-time monitoring)
├── mcp_server/        # MCP Tools (Official Bot bridge, Server inspection)
├── utils/             # Pterodactyl API, RCON, Logging, & Supabase
├── worker/            # Playwright background automation worker
└── launch.sh          # Unified one-command startup script
```

---

## ⚙️ Quick Start

1. **Setup:** `pip install -r requirements.txt` and `playwright install chromium`.
2. **Configure:** Fill in `.env` with your Discord, Supabase, and Pterodactyl keys.
3. **Internal Key:** Ensure `INTERNAL_API_KEY` matches on both the AI and VPS Bot.
4. **Launch:** `./launch.sh`

---

## 🌟 Credits
- **Owner:** chriz3656 (CHRIZ)
- **AI Engine:** Groq (Llama 3.3), OpenAI (GPT-4), Gemini (1.5 Flash), AWS Bedrock.

**SkyRealms SMP Season 2**  
*Build. Compete. Survive. Evolve.*
