from typing import List, Dict, Any, Optional
from ai.providers.base import BaseAIProvider, AIResponse
from ai.providers.bedrock import BedrockProvider
from ai.providers.groq import GroqProvider
from ai.providers.openai import OpenAIProvider
from ai.providers.gemini import GeminiProvider
from core.config import settings
from loguru import logger

class AIProviderManager:
    def __init__(self):
        self.providers: Dict[str, BaseAIProvider] = {}
        self._setup_providers()
        self.primary_name = settings.AI_PRIMARY_PROVIDER

    def _setup_providers(self):
        # Primary & Secondaries
        try:
            self.providers["groq"] = GroqProvider()
        except Exception as e:
            logger.warning(f"Failed to initialize Groq provider: {e}")

        try:
            self.providers["openai"] = OpenAIProvider()
        except Exception as e:
            logger.warning(f"Failed to initialize OpenAI provider: {e}")

        try:
            self.providers["gemini"] = GeminiProvider()
        except Exception as e:
            logger.warning(f"Failed to initialize Gemini provider: {e}")

        try:
            self.providers["bedrock"] = BedrockProvider()
        except Exception as e:
            logger.warning(f"Failed to initialize Bedrock provider: {e}")

    async def generate_with_fallback(
        self, 
        messages: List[Dict[str, str]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        system_prompt: Optional[str] = None
    ) -> AIResponse:
        # Try Primary
        primary = self.providers.get(self.primary_name)
        if primary:
            try:
                return await primary.generate_response(messages, tools, system_prompt)
            except Exception as e:
                logger.error(f"Primary provider {self.primary_name} failed: {e}. Falling back...")
        
        # Try Fallbacks
        for name, provider in self.providers.items():
            if name == self.primary_name:
                continue
            try:
                logger.info(f"Attempting fallback with {name}...")
                return await provider.generate_response(messages, tools, system_prompt)
            except Exception as e:
                logger.error(f"Fallback provider {name} failed: {e}")
        
        raise RuntimeError("All AI providers failed to generate a response.")

ai_manager = AIProviderManager()
