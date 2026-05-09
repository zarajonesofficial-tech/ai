from enum import Enum
from typing import List

class Intent(Enum):
    SERVER_STATUS = "server_status"
    MINECRAFT_PLAYERS = "minecraft_players"
    DISCORD_INFO = "discord_info"
    KNOWLEDGE_QUERY = "knowledge_query"
    MODERATION = "moderation"
    TICKET = "ticket"
    GENERAL_CHAT = "general_chat"

def detect_intent(text: str) -> Intent:
    """
    Categorizes the user request based on keyword routing.
    Deterministic and fast.
    """
    text = text.lower()
    
    # 1. Minecraft & Server Status
    if any(k in text for k in ["status", "online", "up?", "working", "maintenance"]):
        return Intent.SERVER_STATUS
    if any(k in text for k in ["player", "who is on", "count", "members"]):
        if "discord" not in text:
            return Intent.MINECRAFT_PLAYERS
    
    # 2. Discord Info
    if any(k in text for k in ["discord", "guild", "server members", "roles", "channel"]):
        return Intent.DISCORD_INFO
        
    # 3. Knowledge Base / Rules / Info
    if any(k in text for k in [
        "rule", "ip", "port", "how to", "info", "what is", "about", "faq", "help", 
        "rank", "skill", "diamond", "legacy", "owner", "chriz", "grief", "cross", 
        "platform", "bedrock", "whitelist", "apply", "application", "cross-platform",
        "economy", "money", "casino", "gamble", "spawn", "protect", "event", "competition",
        "progress", "feature", "clan", "war", "pvp", "shop", "join"
    ]):
        return Intent.KNOWLEDGE_QUERY
        
    # 4. Moderation / Tickets
    if any(k in text for k in ["ban", "mute", "kick", "warn", "report", "incident"]):
        return Intent.MODERATION
    if any(k in text for k in ["ticket", "support", "help me", "admin"]):
        return Intent.TICKET
        
    return Intent.GENERAL_CHAT
