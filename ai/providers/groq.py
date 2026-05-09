import httpx
from typing import List, Dict, Any, Optional
from ai.providers.base import BaseAIProvider, AIResponse
from core.config import settings
from loguru import logger

class GroqProvider(BaseAIProvider):
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.3-70b-versatile"

    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        system_prompt: Optional[str] = None
    ) -> AIResponse:
        if not self.api_key:
            raise ValueError("Groq API Key not set")

        payload_messages = []
        if system_prompt:
            payload_messages.append({"role": "system", "content": system_prompt})
        payload_messages.extend(messages)

        payload = {
            "model": self.model,
            "messages": payload_messages,
            "max_tokens": 1024
        }
        
        if tools:
            # Simple conversion of MCP tools to OpenAI format for Groq
            payload["tools"] = [{"type": "function", "function": t} for t in tools]

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=payload,
                timeout=30.0
            )
            
            if response.status_code != 200:
                logger.error(f"Groq API Error ({response.status_code}): {response.text}")
                response.raise_for_status()

            data = response.json()
            
            message = data["choices"][0]["message"]
            content = message.get("content") or ""
            
            # If tool calls are present, they will be in message["tool_calls"]
            # The AIProviderManager or the Cog should handle the actual tool execution loop
            
            return AIResponse(
                content=content,
                raw_response=data,
                provider="groq",
                model=self.model,
                prompt_tokens=data.get("usage", {}).get("prompt_tokens", 0),
                completion_tokens=data.get("usage", {}).get("completion_tokens", 0)
            )
