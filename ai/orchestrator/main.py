from typing import List, Dict, Any, Optional
import discord
from ai.orchestrator.master_intent_router import Intent, intent_router
from ai.orchestrator.context import build_context, format_context_for_prompt
from ai.orchestrator.social_mode import handle_social_chat
from ai.orchestrator.social_memory import social_memory
from ai.orchestrator.humanizer import humanizer
from ai.orchestrator.action_executor import action_executor
from ai.orchestrator.workflow_manager import workflow_manager
from ai.orchestrator.prompt_layer_manager import prompt_layer_manager
from ai.orchestrator.realism_engine import realism_engine
from ai.manager import ai_manager
from utils.logger import core_logger

class AIOrchestrator:
    """
    Advanced Orchestrator with Social Context Awareness and Layered Prompts.
    """

    async def handle_query(self, 
                           message: str, 
                           member: Optional[discord.Member] = None, 
                           channel: Optional[discord.TextChannel] = None, 
                           history: List[Dict[str, str]] = None,
                           social_context: Optional[Dict[str, Any]] = None) -> str:
        """
        The master pipeline for processing an AI request.
        Utilizes social context awareness and modular prompt layering.
        """
        try:
            # 1. Detect Intent
            intent = await intent_router.route(message)
            core_logger.info(f"AI Orchestrator: Classified intent as '{intent.value}'")

            # 2. Extract Channel ID for memory/routing
            channel_id = channel.id if channel else 0

            # 3. Handle WORKFLOW / ACTION (Execution priority)
            if intent == Intent.WORKFLOW and member and channel:
                return await workflow_manager.run_workflow(message, member, channel)

            if intent == Intent.ACTION and member and channel:
                return await action_executor.execute(message, member, channel)

            # 4. Fetch Facts (Operational/KB)
            raw_facts = await build_context(intent, message)
            formatted_facts = format_context_for_prompt(raw_facts)

            # 5. Build Layered System Prompt
            # Use the social_context dictionary if provided (built by the Cog)
            context_pkg = social_context or {"author": {"display_name": member.display_name if member else "User"}}
            full_system_prompt = prompt_layer_manager.get_full_system_prompt(context_pkg, formatted_facts)

            # 6. History Management
            final_history = history
            if not final_history and channel_id != 0:
                final_history = await social_memory.get_history(channel_id)
            if not final_history:
                final_history = []
                
            final_history.append({"role": "user", "content": message})

            # 7. Generate Response
            response = await ai_manager.generate_with_fallback(
                messages=final_history,
                system_prompt=full_system_prompt
            )

            content = response.content

            # 8. Realism & Humanization Pass
            content = realism_engine.apply_pacing(content)
            
            if channel:
                content = humanizer.humanize(content)
                await social_memory.add_message(channel_id, "assistant", content)

            return content

        except Exception as e:
            core_logger.error(f"Orchestrator failed: {e}")
            return "❌ I encountered an internal error while trying to process your request."

orchestrator = AIOrchestrator()
