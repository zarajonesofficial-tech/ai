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
2. **Configure:** Copy `.env.example` to `.env`, then fill in your Discord, Supabase, and Pterodactyl keys.
3. **Internal Key:** Ensure `INTERNAL_API_KEY` matches on both the AI and VPS Bot.
4. **Launch:** `./launch.sh`

---

## 🚂 Railway Deployment

This repo deploys cleanly to Railway as two services:

1. **Web service:** FastAPI API + Discord bot using `Dockerfile`
2. **Worker service:** Playwright automation worker using `worker.Dockerfile`

Recommended setup:

1. Create two Railway services from the same repository.
2. For the **web** service, set the config file path to `/railway.web.json`.
3. For the **worker** service, set the config file path to `/railway.worker.json`.
4. Copy variables from `.env.example` into Railway service variables.
5. Use the same shared secrets on both services, especially `DISCORD_TOKEN`, `SUPABASE_URL`, `SUPABASE_KEY`, and `INTERNAL_API_KEY`.

Notes:

- The web container now listens on Railway's `PORT` automatically.
- The worker uses `requirements-worker.txt` and a matching `mcr.microsoft.com/playwright/python:v1.59.0-noble` base image to avoid runtime browser/dependency mismatches.
- The Railway config files explicitly override the start command, so Railway should not run `launch.sh` for these services.
- Railway uses the health check path `/health` for the web service.
- If you prefer service settings instead of config-as-code, set `RAILWAY_DOCKERFILE_PATH=Dockerfile` for the web service and `RAILWAY_DOCKERFILE_PATH=worker.Dockerfile` for the worker service.
- Do not use `launch.sh` on Railway; let each service run its own container command.

Relevant Railway docs:

- Monorepo/root-directory guidance: https://docs.railway.com/guides/monorepo
- Public port handling: https://docs.railway.com/deploy/exposing-your-app
- Config as code and custom Dockerfile path: https://docs.railway.com/reference/config-as-code
- Dockerfile behavior: https://docs.railway.com/builds/dockerfiles

---

## 🌟 Credits
- **Owner:** chriz3656 (CHRIZ)
- **AI Engine:** Groq (Llama 3.3), OpenAI (GPT-4), Gemini (1.5 Flash), AWS Bedrock.

**SkyRealms SMP Season 2**  
*Build. Compete. Survive. Evolve.*
