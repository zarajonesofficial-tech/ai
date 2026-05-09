from typing import List, Dict, Any
from ai.manager import ai_manager
from ai.orchestrator.social_memory import social_memory
from ai.orchestrator.personality_prompt import get_social_prompt
from ai.orchestrator.context import build_context, format_context_for_prompt
from ai.orchestrator.master_intent_router import Intent
from ai.orchestrator.humanizer import humanizer
from utils.logger import ai_logger

async def handle_social_chat(channel_id: int, user_query: str) -> str:
    """
    The pipeline for natural, social conversations.
    Uses example-driven context and a specialized personality prompt.
    Includes a Response Humanization Layer to strip technical jargon.
    """
    try:
        # 1. Fetch real-time status for grounding (Social mode uses base state)
        raw_context = await build_context(Intent.SOCIAL, user_query)
        formatted_context = format_context_for_prompt(raw_context)

        # 2. Get social history for context memory
        history = await social_memory.get_history(channel_id)
        
        # 3. Build the personality-driven system prompt (includes naturalization examples)
        system_prompt = get_social_prompt(formatted_context)

        # 4. Generate response
        ai_logger.info(f"Social Mode: Generating naturalized response for channel {channel_id}")
        response = await ai_manager.generate_with_fallback(
            messages=history,
            system_prompt=system_prompt
        )

        content = response.content

        # 5. Response Humanization Layer
        content = humanizer.humanize(content)
        
        # 6. Save AI's response to memory
        await social_memory.add_message(channel_id, "assistant", content)

        return content

    except Exception as e:
        ai_logger.error(f"Social Mode failed: {e}")
        return "onnu hang aayi bro, pinne nokkam 😭"
