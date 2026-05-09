from typing import List, Dict, Any, Optional
from ai.orchestrator.intent import Intent, detect_intent
from ai.orchestrator.context import build_context, format_context_for_prompt
from ai.orchestrator.social_mode import handle_social_chat
from ai.orchestrator.social_memory import social_memory
from ai.manager import ai_manager
from utils.logger import core_logger

class AIOrchestrator:
    def __init__(self):
        self.base_system_instruction = (
            "You are the CHRIZ__3656 AI Operational Assistant. "
            "Your goal is to provide accurate, factual information about the server and community. "
            "CRITICAL RULES:\n"
            "1. SCAN ALL provided REAL-TIME SYSTEM CONTEXT sections. Facts are often listed under specific headers.\n"
            "2. USE ONLY the provided context. If a fact (like a skill or a feature) is in the context, you MUST use it.\n"
            "3. If the context TRULY does not contain the answer after checking every section, say 'I don't have that information'.\n"
            "4. Do not hallucinate. Do not use outside knowledge about Minecraft or other servers.\n"
            "5. Be professional, concise, and helpful."
        )

    async def handle_query(self, message: str, channel_id: int = 0, history: List[Dict[str, str]] = None) -> str:
        """
        The main pipeline for processing an AI request.
        Routes between Operational Mode and Social Personality Mode.
        """
        try:
            # 1. Detect Intent
            intent = detect_intent(message)
            core_logger.info(f"AI Orchestrator: Detected intent '{intent.value}'")

            # 2. Routing Logic
            # If it's a general chat/social query and we have a channel_id, use Social Mode
            if intent == Intent.GENERAL_CHAT and channel_id != 0:
                return await handle_social_chat(channel_id, message)

            # 3. Operational Mode (Default for specific intents)
            raw_context = await build_context(intent, message)
            formatted_context = format_context_for_prompt(raw_context)

            full_system_prompt = f"{self.base_system_instruction}\n\n{formatted_context}"

            # Use provided history or fallback to recent channel memory if available
            final_history = history
            if not final_history and channel_id != 0:
                final_history = await social_memory.get_history(channel_id)

            if not final_history:
                final_history = []

            final_history.append({"role": "user", "content": message})

            response = await ai_manager.generate_with_fallback(
                messages=final_history,
                system_prompt=full_system_prompt
            )

            # Save result to memory if possible
            if channel_id != 0:
                await social_memory.add_message(channel_id, "assistant", response.content)

            return response.content

        except Exception as e:
            core_logger.error(f"Orchestrator failed: {e}")
            return "❌ I encountered an internal error while trying to process your request."


orchestrator = AIOrchestrator()
