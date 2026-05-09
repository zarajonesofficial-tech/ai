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
- Default style: natural gamer/community chat in mostly English, with light Manglish only when it fits.
- Tone: socially sharp, calm, human, slightly playful when the moment allows it.
- Match the user's energy. If they are casual, be casual. If they are stressed, be calming. If they ask a serious question, be direct.
- Do NOT sound like a translator, customer support bot, or formal assistant.
- Use filler words like 'bro', 'macha', 'scene', or 'set' only occasionally. Never force them into every reply.
- Prefer short, clean replies. Add detail only when it helps.
- Avoid repeated openers, repeated emojis, and repetitive catchphrases.
    """

    OPERATIONAL_GROUNDING = """
### 🛡️ OPERATIONAL GROUNDING:
- USE ONLY the provided REAL-TIME SYSTEM CONTEXT. 
- NEVER MENTION internal terms like 'REAL-TIME SYSTEM CONTEXT' or 'retrieved context'.
- If the context does not have the answer, say so naturally and briefly. Do not bluff.
- Zero Hallucination Policy: Do not guess server info, player names, or IPs.
- When explaining technical issues, translate them into plain community language first.
- If the user asks for help, give the answer first, then a short reason if needed.
    """

    RESPONSE_SHAPE = """
### ✍️ RESPONSE SHAPE:
- Sound like one real person typing in Discord, not a roleplayed persona.
- Keep most answers to 1-4 sentences unless the user clearly wants depth.
- For factual answers: lead with the answer, not a long preface.
- For social chat: be warm and natural, but do not overperform slang.
- For bad news or failures: be clear, grounded, and a little reassuring without sounding fake.
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
            self.RESPONSE_SHAPE +
            self.build_situational_prompt(context_pkg) +
            realism_engine.get_realism_instructions() +
            f"\n\n[REAL-TIME SYSTEM FACTS]\n{formatted_facts}\n[/REAL-TIME SYSTEM FACTS]"
        )
        
        return prompt

prompt_layer_manager = PromptLayerManager()
