# CHRIZ__3656 AI — Operational Assistant 🌌

**CHRIZ__3656 AI** is a modular, tool-first AI operations platform designed to manage Minecraft Bedrock servers, Discord communities, and automated workflows. It transforms a standard AI chatbot into a factual system assistant by grounding every response in real-time server data, while maintaining a naturally conversational social personality.

---

## 🚀 Current Development Stage: **PRODUCTION-READY**
The platform features a **Dual-Layer Brain** that seamlessly switches between factual infrastructure management and natural community engagement.

| Component | Status | Description |
|---|---|---|
| **Core API** | ✅ Stable | FastAPI backend with unified color-coded logging. |
| **Discord Bot** | ✅ Functional | 8+ commands, Social Personality, & Ticket systems. |
| **AI Orchestrator**| ✅ Reliable | Tool-first logic with deterministic fact injection. |
| **Social Layer** | ✅ Natural | Conversational Manglish (English/Malayalam/Slang). |
| **Knowledge Base** | ✅ Optimized| Multi-keyword search with title prioritization. |
| **MC RCON** | ✅ Stable | Robust async connection management (aiorcon). |
| **Automation** | ✅ Graceful | Playwright worker for non-API panel interactions. |
| **Dashboard** | ✅ Real-time| Live metrics (Players, Tickets, Tokens) on Localhost. |

---

## 🧠 Dual-Layer AI Architecture

### 1. Operational Mode (Factual)
When factual data is required (server IP, player counts, rules, moderation), the bot uses a **Tool-First pipeline**:
`Intent Detection` → `Real Data Retrieval` → `Fact Injection` → `LLM Generation`.
This ensures **Zero Hallucinations** for critical server data.

### 2. Social Mode (Conversational)
When users chat naturally, mention the bot, or reply to it, the **Social Naturalization Layer** activates:
- **Language:** Speaks natural **Manglish** (70% English / 30% Malayalam Slang).
- **Personality:** Intelligent, chill, slightly playful, and culturally aware.
- **Memory:** Remembers the last 20 messages in the channel to hold natural discussions.

---

## 🛠️ Core Features

### 1. Factual AI Assistant
- **Social Naturalization:** Uses example-driven generation to avoid robotic "translator" phrasing.
- **Context Memory:** Maintains a rolling history window per channel.
- **Zero-Hallucination:** Strictly follows factual context for server infrastructure data.

### 2. Knowledge Base (RAG)
- **SkyRealms Docs:** Pre-ingested with server rules, ranks, skills, and onboarding info.
- **Robust Search:** Uses multi-keyword "OR" logic to find facts accurately without complex embeddings.

### 3. Minecraft Bedrock & Discord
- **Real-time Sync:** Discord `/status` and `/players` commands pull live data from RCON.
- **Modular Moderation:** `/warn`, `/mute`, and `/ban` with persistent audit logs in Supabase.
- **Operational Awareness:** AI understands maintenance modes and active server events.

### 4. Stability & Monitoring
- **Clean Logging:** Color-coded terminal output categorized by `[CORE]`, `[BOT]`, `[AI]`, `[WORKER]`.
- **Unified Launcher:** `launch.sh` handles startup and graceful cleanup of all services.

---

## 📁 Project Structure
```text
/CHRIZ3656
├── ai/                # Orchestrator, Social Mode, & Knowledge Base
├── api/               # FastAPI routers (Live State, RBAC, Auth)
├── bot/               # discord.py Cogs (Moderation, Minecraft, AI, Tickets)
├── core/              # Pydantic Config, DB Repositories, & Workflows
├── frontend/          # Vanilla JS/CSS/HTML dashboard (Live metrics)
├── mcp_server/        # MCP Tools (Direct server & member inspection)
├── utils/             # RCON, Logger, & Supabase Client
├── worker/            # Playwright background worker
├── launch.sh          # Unified one-command startup script
└── README.md          # Project documentation
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
# Fill in your Discord, Supabase, and AI Provider (Groq/Gemini/AWS) keys

# Initialize Database
# Run database_schema.sql in your Supabase SQL Editor (Enable 'pgvector' first)
```

### 2. Launch
```bash
# Start the entire ecosystem
./launch.sh
```
View the live monitor at: `http://localhost:8080`

---

## 🌟 Credits & Providers
- **Owner:** chriz3656 (CHRIZ)
- **AI Engine:** Primary: **Groq (Llama 3.3)** | Fallbacks: **OpenAI**, **Gemini**, **AWS Bedrock**.

---
**SkyRealms SMP Season 2**  
*Build. Compete. Survive. Evolve.*
