from fastapi import APIRouter, HTTPException
from core.repository import op_repo, ticket_repo, supabase
from utils.minecraft import mc_client
from typing import Dict, Any
import re

router = APIRouter(prefix="/api/state", tags=["Operational State"])

@router.get("")
async def get_state():
    state = await op_repo.get_latest()
    if not state:
        state = {"status": "unknown", "owner_available": False}
    
    # 1. Real Minecraft Player Count
    player_count = 0
    mc_resp = await mc_client.run_command("list")
    if mc_resp:
        # Simple regex to find numbers like "There are 2/20 players online"
        match = re.search(r"(\d+)/\d+", mc_resp)
        if match:
            player_count = int(match.group(1))
        elif "0 players" in mc_resp.lower():
            player_count = 0
        else:
            # Fallback: count lines or other parsing if needed
            player_count = 0

    # 2. Real Active Ticket Count
    tickets_resp = supabase.table("tickets").select("id", count="exact").eq("status", "open").execute()
    ticket_count = tickets_resp.count if hasattr(tickets_resp, 'count') else 0

    # 3. Real AI Token Usage (Total)
    ai_resp = supabase.table("ai_conversations").select("token_usage").execute()
    total_tokens = sum([row.get("token_usage", 0) for row in ai_resp.data]) if ai_resp.data else 0

    return {
        **state,
        "live_players": player_count,
        "active_tickets": ticket_count,
        "total_tokens": total_tokens
    }
