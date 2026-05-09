from enum import Enum
from typing import List, Dict, Any
from ai.manager import ai_manager
from utils.logger import core_logger

class Intent(Enum):
    WORKFLOW = "workflow"
    ACTION = "action"
    FACTUAL = "factual"
    SOCIAL = "social"

class MasterIntentRouter:
    """
    Advanced LLM-based intent routing to eliminate confusion between 
    Social chat and Infrastructure actions.
    """
    
    SYSTEM_PROMPT = """
    You are an Intent Classifier for an AI Operations platform.
    Your job is to categorize the user's message into one of four categories:
    
    1. WORKFLOW: Multi-step tasks or complex automation requests (e.g., 'start maintenance and restart').
    2. ACTION: Single executable commands (e.g., 'mute @user', 'restart server', 'review whitelist').
    3. FACTUAL: Questions about server status, rules, or players.
    4. SOCIAL: Casual conversation and banter.
    
    CRITICAL: 
    - Commands like 'mention everyone' or 'ping all' are ACTION, not social.
    - Questions like 'how many players' are FACTUAL.
    - Mixed requests like 'say hello and then restart' are WORKFLOW.
    
    Respond ONLY with the category name in lowercase.
    """

    async def route(self, message: str) -> Intent:
        """Determines the primary intent of the user message."""
        try:
            # Use a fast model for intent detection
            resp = await ai_manager.generate_with_fallback(
                messages=[{"role": "user", "content": message}],
                system_prompt=self.SYSTEM_PROMPT
            )
            
            label = resp.content.strip().lower()
            
            if "workflow" in label: return Intent.WORKFLOW
            if "action" in label: return Intent.ACTION
            if "factual" in label: return Intent.FACTUAL
            
            return Intent.SOCIAL # Default
            
        except Exception as e:
            core_logger.error(f"Intent detection failed: {e}. Falling back to keywords.")
            return self._keyword_fallback(message)

    def _keyword_fallback(self, text: str) -> Intent:
        """Deterministic keyword backup if LLM fails."""
        text = text.lower()
        
        # 1. Action/Workflow priority
        if "then" in text or "and then" in text: return Intent.WORKFLOW
        
        actions = ["mute", "ban", "kick", "warn", "restart", "mention", "ping", "clear", "announce", "whitelist", "application"]
        if any(a in text for a in actions): return Intent.ACTION
        
        # 2. Factual
        factuals = ["what", "how", "who", "is", "where", "status", "count", "players", "rule", "ip", "port"]
        if any(f in text for f in factuals): return Intent.FACTUAL
        
        return Intent.SOCIAL

intent_router = MasterIntentRouter()
