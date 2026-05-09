import json
from typing import Dict, Any
from ai.orchestrator.realism_engine import realism_engine

class PromptLayerManager:
    """
    Manages the modular system prompt architecture, layering identity, 
    social rules, operational grounding, and situational context.
    """
    
    CORE_IDENTITY = """
You are CHRIZ__3656 AI, the Master Operational Assistant for SkyRealms SMP.
You are a persistent, socially aware AI entity.
CRITICAL: You are an AI, NOT a human. Do not invent a human life, personal relationships, or fake history.
    """

    SOCIAL_RULES = """
### 🗣️ SOCIAL BEHAVIOR:
- Style: 70% English / 30% Manglish Slang. 
- Tone: Intelligent, chill, slightly playful community member.
- Do NOT sound like a translator or formal assistant.
- Use filler words like 'bro', 'macha', 'scene', 'okay bro', 'set' naturally.
    """

    OPERATIONAL_GROUNDING = """
### 🛡️ OPERATIONAL GROUNDING:
- USE ONLY the provided REAL-TIME SYSTEM CONTEXT. 
- NEVER MENTION internal terms like 'REAL-TIME SYSTEM CONTEXT' or 'retrieved context'.
- If the context does not have the answer, say 'I don't have that information' naturally.
- Zero Hallucination Policy: Do not guess server info, player names, or IPs.
    """

    def build_situational_prompt(self, context_pkg: Dict[str, Any]) -> str:
        """Constructs a prompt layer based on the current social situational context."""
        author = context_pkg.get("author", {})
        channel = context_pkg.get("channel", {})
        reply = context_pkg.get("reply_context", {})
        
        lines = ["\n### 🌍 SITUATIONAL AWARENESS:"]
        
        # Channel Awareness
        chan_name = channel.get("name", "unknown")
        if "support" in chan_name or "ticket" in chan_name:
            lines.append("- Channel: Support context. Be more professional and concise.")
        elif "general" in chan_name:
            lines.append("- Channel: General chat. Be more relaxed and conversational.")
        elif "staff" in chan_name:
            lines.append("- Channel: Staff room. Be structured and minimal on jokes.")
        
        # Role Awareness
        if author.get("permissions", {}).get("admin"):
            lines.append(f"- User: {author.get('display_name')} is an ADMIN. You may use a more operational/technical tone if needed.")
        elif author.get("permissions", {}).get("moderator"):
            lines.append(f"- User: {author.get('display_name')} is a MODERATOR.")
        else:
            lines.append(f"- User: {author.get('display_name')} is a Community Member.")

        # Reply Awareness
        if reply:
            lines.append(f"- Interaction: You are replying to {reply.get('reply_to_user')}. Their message was: '{reply.get('reply_to_message')}'")
        
        return "\n".join(lines)

    def get_full_system_prompt(self, context_pkg: Dict[str, Any], formatted_facts: str) -> str:
        """Assembles the final layered system prompt."""
        
        prompt = (
            self.CORE_IDENTITY +
            self.SOCIAL_RULES +
            self.OPERATIONAL_GROUNDING +
            self.build_situational_prompt(context_pkg) +
            realism_engine.get_realism_instructions() +
            f"\n\n[REAL-TIME SYSTEM FACTS]\n{formatted_facts}\n[/REAL-TIME SYSTEM FACTS]"
        )
        
        return prompt

prompt_layer_manager = PromptLayerManager()
