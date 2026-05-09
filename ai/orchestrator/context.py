import datetime
from typing import Dict, Any, List
from core.repository import op_repo, mod_repo, user_repo
from utils.minecraft import mc_client
from ai.knowledge_base import kb
from bot.main import bot as discord_bot
from ai.orchestrator.intent import Intent

async def build_context(intent: Intent, query: str) -> Dict[str, Any]:
    """
    Retrieves real-time data from the system based on the detected intent.
    """
    context = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "operational_state": {},
        "minecraft": {},
        "discord": {},
        "knowledge_base": []
    }

    # 1. Always fetch base operational state
    state = await op_repo.get_latest()
    if state:
        context["operational_state"] = {
            "status": state.get("status"),
            "owner_available": state.get("owner_available"),
            "active_events": state.get("active_events", [])
        }

    # 2. Fetch specific data based on intent
    if intent in [Intent.SERVER_STATUS, Intent.MINECRAFT_PLAYERS]:
        mc_resp = await mc_client.run_command("list")
        context["minecraft"] = {"raw_list": mc_resp or "Offline/Unknown"}

    if intent == Intent.DISCORD_INFO:
        guild = discord_bot.guilds[0] if discord_bot.guilds else None
        if guild:
            context["discord"] = {
                "member_count": guild.member_count,
                "online_members": len([m for m in guild.members if m.status != "offline"]),
                "channels": [c.name for c in guild.text_channels[:10]],
                "roles": [r.name for r in guild.roles if r.name != "@everyone"]
            }

    if intent == Intent.KNOWLEDGE_QUERY or intent == Intent.TICKET:
        # Perform semantic search for facts
        matches = await kb.search(query, limit=3)
        context["knowledge_base"] = [
            {"title": m.get("title"), "content": m.get("content")} for m in matches
        ]

    if intent == Intent.MODERATION:
        # Fetch last 3 incidents for context
        logs = await mod_repo.get_all()
        context["moderation"] = {"recent_logs": logs[-3:] if logs else []}

    return context

def format_context_for_prompt(context: Dict[str, Any]) -> str:
    """
    Converts the context dictionary into a flat string for the system prompt.
    """
    lines = ["[REAL-TIME SYSTEM CONTEXT]"]
    lines.append(f"Current Time (UTC): {context['timestamp']}")
    
    op = context.get("operational_state", {})
    lines.append(f"Global Status: {op.get('status', 'Unknown')}")
    lines.append(f"Owner Available: {op.get('owner_available', False)}")
    
    if context.get("minecraft"):
        lines.append(f"Minecraft Server Data: {context['minecraft'].get('raw_list')}")
        
    if context.get("discord"):
        d = context["discord"]
        lines.append(f"Discord Members: {d.get('member_count')} total, {d.get('online_members')} online.")
        
    if context.get("knowledge_base"):
        lines.append("Knowledge Base Facts:")
        for doc in context["knowledge_base"]:
            lines.append(f"- {doc['title']}: {doc['content']}")
            
    if context.get("moderation"):
        lines.append(f"Recent Moderation Logs: {context['moderation'].get('recent_logs')}")

    lines.append("[/REAL-TIME SYSTEM CONTEXT]")
    return "\n".join(lines)
