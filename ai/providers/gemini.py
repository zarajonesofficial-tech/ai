import httpx
from typing import List, Dict, Any, Optional
from ai.providers.base import BaseAIProvider, AIResponse
from core.config import settings
from loguru import logger

class GeminiProvider(BaseAIProvider):
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model = "gemini-1.5-flash"
        self.url = f"https://generativelanguage.googleapis.com/v1/models/{self.model}:generateContent?key={self.api_key}"

    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        system_prompt: Optional[str] = None
    ) -> AIResponse:
        if not self.api_key:
            raise ValueError("Gemini API Key not set")

        # Convert Anthropic/OpenAI format to Gemini format
        contents = []
        # In Gemini 1.5, system instructions should ideally be in a separate field, 
        # but for compatibility, we can prepend to the first user message if needed.
        # However, the 'contents' structure below is common.
        if system_prompt:
            contents.append({"role": "user", "parts": [{"text": f"System Instruction: {system_prompt}"}]})
            contents.append({"role": "model", "parts": [{"text": "Acknowledged."}]})

        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({"role": role, "parts": [{"text": msg["content"]}]})

        payload = {"contents": contents}

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.url,
                json=payload,
                timeout=30.0
            )
            
            if response.status_code != 200:
                logger.error(f"Gemini API Error ({response.status_code}): {response.text}")
                response.raise_for_status()

            data = response.json()
            
            try:
                content = data["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError):
                content = "Error parsing Gemini response"

            # Gemini usage stats
            usage = data.get("usageMetadata", {})
            return AIResponse(
                content=content,
                raw_response=data,
                provider="gemini",
                model=self.model,
                prompt_tokens=usage.get("promptTokenCount", 0),
                completion_tokens=usage.get("candidatesTokenCount", 0)
            )
