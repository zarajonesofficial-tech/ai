from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class AIResponse(BaseModel):
    content: str
    raw_response: Any
    provider: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0

class BaseAIProvider(ABC):
    @abstractmethod
    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        system_prompt: Optional[str] = None
    ) -> AIResponse:
        pass
