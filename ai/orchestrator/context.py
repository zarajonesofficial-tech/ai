import datetime
from typing import Dict, Any, List
from core.repository import op_repo, mod_repo, user_repo
from utils.minecraft import mc_client
from utils.pterodactyl import ptero_client
from ai.knowledge_base import kb
from bot.main import bot as discord_bot
from ai.orchestrator.master_intent_router import Intent

async def build_context(intent: Intent, query: str) -> Dict[str, Any]:
    """
    Retrieves real-time data from the system based on the detected intent.
    """
    context = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "operational_state": {},
        "minecraft": {},
        "pterodactyl": {},
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
    
    if intent == Intent.FACTUAL:
        # Search KB
        matches = await kb.search(query, limit=5)
        context["knowledge_base"] = [
            {"title": m.get("title"), "content": m.get("content")} for m in matches
        ]
        
        # 1. Check MC status (In-game)
        mc_resp = await mc_client.run_command("list")
        context["minecraft"] = {"raw_list": mc_resp or "Offline/Unknown"}
        
        # 2. Check Ptero resources (System metrics)
        ptero_res = await ptero_client.get_resources()
        if ptero_res:
            context["pterodactyl"] = ptero_res

    if intent in [Intent.ACTION, Intent.WORKFLOW]:
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
    
    if context.get("minecraft") and context["minecraft"].get("raw_list"):
        lines.append(f"Minecraft Server Data: {context['minecraft'].get('raw_list')}")
        
    if context.get("pterodactyl") and context["pterodactyl"]:
        p = context["pterodactyl"]
        cpu = p.get('cpu_absolute', 0)
        mem = p.get('memory_bytes', 0) / (1024 * 1024) # MB
        lines.append(f"Panel Metrics: CPU {cpu}%, RAM {mem:.2f}MB, State: {p.get('current_state')}")

    if context.get("discord") and context["discord"]:
        d = context["discord"]
        lines.append(f"Discord Members: {d.get('member_count')} total.")
        
    if context.get("knowledge_base"):
        lines.append("Knowledge Base Facts:")
        for doc in context["knowledge_base"]:
            lines.append(f"- {doc['title']}: {doc['content']}")
            
    if context.get("moderation") and context["moderation"].get("recent_logs"):
        lines.append(f"Recent Moderation Logs: {context['moderation'].get('recent_logs')}")

    lines.append("[/REAL-TIME SYSTEM CONTEXT]")
    return "\n".join(lines)
