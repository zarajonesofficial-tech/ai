import asyncio
import os
from utils.supabase_client import supabase
from utils.logger import setup_logging, core_logger
from core.config import settings

# Initialize logging for the script
setup_logging(debug=settings.DEBUG)

KB_CONTENT = """# SkyRealms SMP — Official Community Knowledge Base 🌌

> Welcome to the official knowledge base for **SkyRealms SMP Season 2** — the evolving Minecraft Bedrock survival ecosystem.

🌐 Website: https://skyrealm.fun

---

# 🌌 About SkyRealms SMP

**SkyRealms SMP** is a Minecraft Bedrock Edition survival multiplayer community focused on delivering a modern, technology-driven, and community-powered survival experience.

The server combines:

- Vanilla-style survival gameplay
- Economy progression
- Custom ranks & skills
- Community-driven gameplay
- Events and competitions
- PvP & clan wars
- Automated systems
- Discord integration
- AI-assisted moderation
- Protected survival systems
- Cross-platform Bedrock support

Season 2 introduces:

- Refreshed gameplay systems
- Improved balancing
- Enhanced progression
- Better world systems
- Competitive gameplay improvements
- Advanced automation systems
- Future AI-powered infrastructure plans

The goal is to create a long-term evolving Minecraft ecosystem powered by community, automation, and innovation.

---

# 🧬 Core Identity

## Server Name
**SkyRealms SMP**

## Short Description
A custom Minecraft Bedrock survival experience with progression systems, skills, economy, automation, community events, and competitive gameplay.

## Core Philosophy

SkyRealms SMP is designed to be more than a normal survival server.

It combines:
- Survival gameplay
- Competitive systems
- Automation
- AI integrations
- Community events
- Technical innovation
- Long-term progression

The vision is to build a technology-driven Minecraft community that continuously evolves over time.

---

# 📡 Server Information

| Category | Information |
|---|---|
| Server Name | SkyRealms SMP |
| Edition | Minecraft Bedrock Edition |
| Gameplay Style | Vanilla+ Survival SMP |
| Server Type | Economy + Community + Events |
| Cross Platform | Supported |
| Website | https://skyrealm.fun |
| Server IP | play.skyrealm.fun |
| Port | 25773 |

---

# 🌠 Season 2 — Purple Edition

Season 2 introduces the futuristic **Purple Edition** branding with:
- Neon-inspired aesthetics
- Enhanced server presentation
- Updated progression systems
- Expanded gameplay features
- Competitive event focus
- Improved community systems

---

# 🎮 Core Features

- Survival SMP
- Economy System
- Clan System
- Rank Progression
- Skill Unlock System
- PvP Battles
- Community Events
- Build Competitions
- Automated Moderation
- Discord Integration
- AI Systems
- Player Shops
- Teleport Systems
- Starter Kits
- Spawn Protection
- Anti-Grief Systems
- Custom NPC Systems
- Cross-platform Bedrock support

---

# 🌠 Rank & Skill System

## Purpose

The rank system rewards progression and unlocks powerful gameplay abilities.

### 💎 Diamond Rank
- Heal
- Feed
- Miner (Haste I)
- 2 Homes
- Chat Color

### 🛡️ Guardian Rank
- Shield
- Scuba
- Clear Effects
- 1 Vault
- 4 Homes

### 🔮 Mystic Rank
- Speed
- Night Vision
- Leap
- 6 Homes

### 🌌 Astral Rank
- Fire Resistance
- Enhanced Shield
- Power I
- 8 Homes

### 🌠 Cosmic Rank
- Float Ability
- Speed II
- Inventory Clear
- 10 Homes

### 👑 Legacy Rank
- Access to ALL skills
- Fly (Lobby Only)
- Power II
- Custom Prefix
- Particle Effects
- 3 Vaults

---

# 💰 Economy System

## Features

- Wallet & Banking
- Daily Rewards
- Trading Systems
- Work Systems
- Casino Systems
- Event Rewards
- Marketplace Economy
- Player Shops

## Planned Expansions

- Auction House
- Jobs System
- Seasonal Economy Events
- Premium Crates
- Expanded trading systems

---

# 🛒 Player Shops

Players can:
- Buy & sell items
- Create businesses
- Build trading empires
- Operate community markets

---

# 🎰 Sky Casino Bot

## Features

- Coinflip
- Roulette
- Wallet systems
- Deposits & withdrawals
- Daily rewards
- Rob system
- Leaderboards
- Interactive menus

---

# 🏰 Spawn Protection System

## Features

- Block break prevention
- Block placement prevention
- Combat restrictions
- Item use restrictions
- Mob spawn prevention
- Operator bypass systems

---

# 🔥 Anti-Grief & Security Systems

## Known Threats

- Lava griefing
- Spawn destruction
- Duplication exploits
- Economy abuse
- Exploit abuse

## Recovery Procedures

- Backup restoration
- Rollbacks
- Investigation logging
- Moderation reviews

---

# 🔨 Moderation System

## Enforcement Philosophy

Zero tolerance for:
- Duplication exploits
- Hacks/cheats
- Spawn griefing
- Toxicity
- Exploit abuse
- Unfair gameplay

---

# 🎉 Events System

## Event Types

- Build Competitions
- Clan Wars
- PvP Tournaments
- End Fight Events
- Airdrop Events
- Treasure Hunts
- Community Challenges
- Seasonal Festivals

---

# ⚔️ Clan Warfare

## Structure

- Team vs Team combat
- Reward pools
- Battlefield arenas
- Elimination objectives

---

# 🤖 Discord Community

## Main Uses

- Announcements
- Reports
- Tickets
- Events
- Moderation
- Economy interaction
- Community discussions

---

# 🧠 AI & Automation Systems

## Features

- AI moderation
- Discord automation
- Minecraft ↔ Discord chat bridge
- Economy tracking
- Automated announcements
- Dashboard monitoring

---

# ⚙️ Technical Systems

## Custom Systems

- Teleport systems
- Lobby systems
- Starter kits
- RTP systems
- Skill systems
- Rank integrations
- Scoreboards
- NPC systems

---

# 📋 Whitelist System

SkyRealms SMP includes an official whitelist application system.

## Application Requirements

Players must provide:
- Minecraft Username
- Discord User ID
- Email Address
- Age
- Rule Agreement Confirmation

---

# 🚀 Future Roadmap

## Gameplay
- Custom mobs
- Dungeons
- Quests
- RPG systems
- Advanced economy

## Technical
- AI-powered moderation
- Better optimization
- Improved anti-cheat
- Advanced automation

---

# ❓ Frequently Asked Questions

## What version is supported?
Minecraft Bedrock Edition.

## Is the server cross-platform?
Yes.

## Is griefing allowed?
No.

---

# 👤 Owner Profile

## Owner
**chriz3656 / CHRIZ**

## Background

- Cybersecurity student
- Minecraft systems developer
- AI & automation enthusiast
- Bedrock infrastructure creator

---

# 📚 Knowledge Base Usage

This document may be used for:
- AI prompts
- Discord bots
- Community onboarding
- Staff documentation
- Website content
- MCP/LLM integrations
- Server planning
- Automation systems

---

# 🌟 Credits

SkyRealms SMP Season 2  
Created and managed by the SkyRealms Team.

🌐 Official Website: https://skyrealm.fun

---

# 📌 Version Information

| Version | Notes |
|---|---|
| Knowledge Base v3.0 | Combined Expanded Edition |

---

# 🚀 Final Message

Welcome to **SkyRealms SMP** 🌌

Build. Compete. Survive. Evolve."""

async def ingest_kb():
    core_logger.info("Starting Knowledge Base ingestion...")
    
    # Clear existing documents to avoid duplicates
    try:
        supabase.table("knowledge_documents").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    except Exception as e:
        core_logger.warning(f"Could not clear table: {e}")

    # Split the KB by top-level headers (# )
    sections = KB_CONTENT.split("\n# ")
    
    count = 0
    for section in sections:
        if not section.strip():
            continue
            
        lines = section.strip().split("\n")
        title = lines[0].strip("# ").strip()
        body = "\n".join(lines[1:]).strip()
        
        # If title is empty (happens on the very first part), use a default
        if not title:
            title = "Introduction"

        try:
            supabase.table("knowledge_documents").insert({
                "category": "skyrealms_smp",
                "title": title,
                "content": body
            }).execute()
            core_logger.info(f"Ingested section: {title}")
            count += 1
        except Exception as e:
            core_logger.error(f"Failed to ingest section '{title}': {e}")

    core_logger.info(f"Ingestion complete. {count} sections added.")

if __name__ == "__main__":
    asyncio.run(ingest_kb())
