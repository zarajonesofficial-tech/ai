# CHRIZ__3656 AI — Master Operational Assistant 🌌

**CHRIZ__3656 AI** is a professional-grade, tool-first AI operations platform designed to manage Minecraft Bedrock servers, Discord communities, and automated infrastructure workflows. 

It is powered by a **Four-Mode Master Orchestrator** that intelligently switches between natural social interaction, factual grounding, secure action execution, and multi-step workflow automation.

---

## 🚀 Current Status: **PRODUCTION-HARDENED & STABILIZED**
The platform has completed all 15 implementation phases. It is now fully verified for social naturalization, factual accuracy, and secure command execution.

| Mode | Status | Description |
|---|---|---|
| **SOCIAL** | ✅ Natural | Casual Manglish conversations with context memory. |
| **FACTUAL** | ✅ Grounded | 100% factual answers via Knowledge Base & RCON. |
| **ACTION** | ✅ Secure | Single-step Discord/MC commands with RBAC security. |
| **WORKFLOW** | ✅ Automated | Multi-step task planning (e.g. Maintenance/Restarts). |

---

## 🧠 Core Architecture: The "Master Brain"

The AI uses a **Priority-Based Orchestration Engine**:

1.  **Intent Classification:** Every message is analyzed by an LLM-based Master Router to determine if it's a Chat, a Fact, an Action, or a Workflow.
2.  **Context Building:** Before the AI generates a response, it retrieves **real-world data**:
    *   **Minecraft:** Live RCON player list and console status.
    *   **Discord:** Member lists, roles, and channel history.
    *   **Knowledge Base:** Semantic search across all server documentation.
3.  **Permission Validation:** Destructive actions (muting, restarting) are blocked unless the user has the required Discord role defined in `capability_registry.json`.
4.  **Response Humanization:** A post-processing layer strips technical jargon (e.g., "retrieved context") and translates it into natural Discord-style Manglish.

---

## 🛠️ Key Features

### 1. Social Personality (70% English / 30% Manglish)
- **Natural Conversation:** Sounds like a real community member, not a robot.
- **Cultural Awareness:** Understands and speaks in Manglish filler words ("bro", "scene", "set").
- **Rolling Memory:** Remembers the last 20 messages in every channel.

### 2. Infrastructure & Automation
- **Task Planning:** Break complex requests ("announce then restart") into logical steps.
- **Moderation:** AI-assisted `/warn`, `/mute`, and `/ban` with persistent logs.
- **Live Monitor:** Real-time Dashboard with status tracking for Players, Tickets, and AI Tokens.

### 3. Safety & Performance
- **Zero Hallucination:** Instructions strictly forbid inventing server information.
- **Rate-Limit Hardening:** Built-in cooldowns and throttling protection.
- **Clean Logging:** Color-coded module logging (`[CORE]`, `[BOT]`, `[AI]`, `[WORKER]`).

---

## 📁 Project Structure
```text
/CHRIZ3656
├── ai/                # Master Router, Action Engine, Workflow Mgr, Humanizer
├── api/               # FastAPI routers (Live Metrics, Dashboard API)
├── bot/               # discord.py Cogs and Event Listeners
├── core/              # Config, Repositories, & Workflow Logic
├── frontend/          # Vanilla JS/CSS/HTML dashboard
├── mcp_server/        # MCP Tools for server & member inspection
├── utils/             # RCON, Logging, & Supabase Clients
├── worker/            # Playwright background automation worker
└── launch.sh          # Unified one-command startup & cleanup
```

---

## ⚙️ Quick Start

1. **Setup:** `pip install -r requirements.txt` and `playwright install chromium`.
2. **Configure:** Fill in `.env` with your API keys.
3. **Database:** Run `database_schema.sql` in Supabase (Enable `pgvector` first).
4. **Launch:** `./launch.sh`

---

## 🌟 Credits
- **Owner:** chriz3656 (CHRIZ)
- **AI Engine:** Groq (Llama 3.3), OpenAI (GPT-4), Gemini (1.5 Flash), AWS Bedrock.

**SkyRealms SMP Season 2**  
*Build. Compete. Survive. Evolve.*
