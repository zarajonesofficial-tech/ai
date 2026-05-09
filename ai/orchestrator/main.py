from typing import List, Dict, Any, Optional
import discord
from ai.orchestrator.master_intent_router import Intent, intent_router
from ai.orchestrator.context import build_context, format_context_for_prompt
from ai.orchestrator.social_mode import handle_social_chat
from ai.orchestrator.social_memory import social_memory
from ai.orchestrator.humanizer import humanizer
from ai.orchestrator.action_executor import action_executor
from ai.orchestrator.workflow_manager import workflow_manager
from ai.manager import ai_manager
from utils.logger import core_logger

class AIOrchestrator:
    def __init__(self):
        self.base_system_instruction = (
            "You are the CHRIZ__3656 AI Operational Assistant. "
            "Your goal is to provide accurate, factual information about the server and community. "
            "CRITICAL RULES:\n"
            "1. SCAN ALL provided REAL-TIME SYSTEM CONTEXT sections. Facts are often listed under specific headers.\n"
            "2. USE ONLY the provided context. If a fact is in the context, you MUST use it.\n"
            "3. **NEVER** mention internal terms like 'REAL-TIME SYSTEM CONTEXT' or 'Minecraft Server Data'. Speak naturally.\n"
            "4. If the context TRULY does not contain the answer, say 'I don't have that information'.\n"
            "5. Do not hallucinate. Be professional, concise, and helpful."
        )

    async def handle_query(self, message: str, member: Optional[discord.Member] = None, channel: Optional[discord.TextChannel] = None, history: List[Dict[str, str]] = None) -> str:
        """
        The master pipeline for processing an AI request.
        Routes between WORKFLOW, ACTION, FACTUAL, and SOCIAL modes.
        """
        try:
            # 1. Detect Intent (LLM-based classification)
            intent = await intent_router.route(message)
            core_logger.info(f"AI Orchestrator: Classified intent as '{intent.value}'")

            # 2. WORKFLOW MODE
            if intent == Intent.WORKFLOW and member and channel:
                return await workflow_manager.run_workflow(message, member, channel)

            # 3. ACTION MODE
            if intent == Intent.ACTION and member and channel:
                return await action_executor.execute(message, member, channel)

            # 4. SOCIAL MODE
            if intent == Intent.SOCIAL and channel:
                return await handle_social_chat(channel.id, message)

            # 5. FACTUAL MODE (Default for queries)
            raw_context = await build_context(intent, message)
            formatted_context = format_context_for_prompt(raw_context)

            full_system_prompt = f"{self.base_system_instruction}\n\n{formatted_context}"

            # History Management
            final_history = history
            if not final_history and channel:
                final_history = await social_memory.get_history(channel.id)
            if not final_history:
                final_history = []
                
            final_history.append({"role": "user", "content": message})

            response = await ai_manager.generate_with_fallback(
                messages=final_history,
                system_prompt=full_system_prompt
            )

            content = response.content

            # Humanization Pass for social channels
            if channel:
                content = humanizer.humanize(content)
                await social_memory.add_message(channel.id, "assistant", content)

            return content

        except Exception as e:
            core_logger.error(f"Orchestrator failed: {e}")
            return "❌ I encountered an internal error while trying to process your request."

orchestrator = AIOrchestrator()
