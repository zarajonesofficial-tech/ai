import httpx
from typing import List, Dict, Any, Optional
from ai.providers.base import BaseAIProvider, AIResponse
from core.config import settings
from loguru import logger

class OpenAIProvider(BaseAIProvider):
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.url = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-4-turbo-preview"

    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        system_prompt: Optional[str] = None
    ) -> AIResponse:
        if not self.api_key:
            raise ValueError("OpenAI API Key not set")

        payload_messages = []
        if system_prompt:
            payload_messages.append({"role": "system", "content": system_prompt})
        payload_messages.extend(messages)

        payload = {
            "model": self.model,
            "messages": payload_messages
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=payload,
                timeout=30.0
            )
            
            if response.status_code != 200:
                logger.error(f"OpenAI API Error ({response.status_code}): {response.text}")
                response.raise_for_status()

            data = response.json()
            
            return AIResponse(
                content=data["choices"][0]["message"]["content"],
                raw_response=data,
                provider="openai",
                model=self.model,
                prompt_tokens=data.get("usage", {}).get("prompt_tokens", 0),
                completion_tokens=data.get("usage", {}).get("completion_tokens", 0)
            )
