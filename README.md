# CHRIZ__3656 AI — Operational Assistant 🌌

**CHRIZ__3656 AI** is a modular, tool-first AI operations platform designed to manage Minecraft Bedrock servers, Discord communities, and automated workflows. It transforms a standard AI chatbot into a factual system assistant by grounding every response in real-time server data, while maintaining a naturally conversational social personality and secure action execution.

---

## 🚀 Current Development Stage: **PRODUCTION-HARDENED**
The platform features a **Four-Mode Master Orchestrator** that intelligently routes and executes requests with absolute precision.

| Component | Status | Description |
|---|---|---|
| **Master Router** | ✅ Stable | LLM-based intent classification (Workflow/Action/Fact/Social). |
| **Action Engine** | ✅ Active | Secure Discord/Minecraft command execution with RBAC. |
| **Workflow Mgr** | ✅ Active | Multi-step task planning (e.g., Maintenance Cycles). |
| **Permission Sys**| ✅ Secure | Role-based capability validation for all AI actions. |
| **Social Layer** | ✅ Natural | Conversations in Manglish with zero technical leakage. |
| **MC RCON** | ✅ Stable | Robust async connection management for server control. |
| **Dashboard** | ✅ Live | Live metrics and task monitoring on Localhost. |

---

## 🧠 Master Orchestration Architecture

The system uses a **Priority-Based Routing** model:

1. **WORKFLOW MODE:** For complex, multi-step requests (e.g., "announce and restart").
2. **ACTION MODE:** For single executable commands (e.g., "mention everyone", "mute user").
3. **FACTUAL MODE:** For server data retrieval (e.g., player counts, rules).
4. **SOCIAL MODE:** For casual chatting and community banter.

### 🛡️ Security First
The AI CANNOT perform destructive actions without permission. The **Permission Validator** checks the user's real Discord roles against the `capability_registry.json` before any action is executed.

---

## 🛠️ Core Features

### 1. Social & Humanized AI
- **Manglish Naturalization:** Speaks casual gamer-style Manglish (70% English / 30% Slang).
- **Humanizer Layer:** Post-processes all responses to strip technical jargon (e.g., "retrieved context").
- **Social Memory:** Remembers channel context across 20+ messages.

### 2. Infrastructure Automation
- **Action Executor:** Securely handles moderation (warn/mute), mentions, and Discord element creation.
- **Workflow Planner:** Breaks complex community requests into logical execution steps.
- **Minecraft Sync:** Direct RCON integration for live player stats and console command execution.

### 3. Knowledge Management
- **RAG Engine:** Searches the SkyRealms knowledge base for factual community information.
- **Title Prioritization:** Ensures the most relevant docs are used for AI grounding.

---

## 📁 Project Structure
```text
/CHRIZ3656
├── ai/                # Master Router, Action Executor, Workflow Mgr, Social Memory
├── api/               # FastAPI routers (Live State, Dashboard API)
├── bot/               # discord.py Cogs and Social Trigger system
├── core/              # Config, DB Repositories, & Workflow runners
├── frontend/          # Vanilla JS dashboard (Real-time monitoring)
├── mcp_server/        # MCP Tools for server & member inspection
├── utils/             # RCON, Logger, & Supabase Client
├── worker/            # Playwright background automation worker
└── launch.sh          # Unified one-command startup script
```

---

## ⚙️ Quick Start

### 1. Setup
```bash
# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Configuration
cp .env.example .env
# Fill in your Discord, Supabase, and AI Provider keys (Groq/Gemini/AWS)
```

### 2. Launch
```bash
# Start the full ecosystem
./launch.sh
```

---

## 🌟 Credits & Providers
- **Owner:** chriz3656 (CHRIZ)
- **AI Engine:** Primary: **Groq (Llama 3.3)** | Fallbacks: **OpenAI**, **Gemini**, **AWS Bedrock**.

---
**SkyRealms SMP Season 2**  
*Build. Compete. Survive. Evolve.*
