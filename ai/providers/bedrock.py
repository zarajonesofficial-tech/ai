import json
import boto3
import asyncio
from typing import List, Dict, Any, Optional
from ai.providers.base import BaseAIProvider, AIResponse
from core.config import settings
from loguru import logger

class BedrockProvider(BaseAIProvider):
    def __init__(self):
        self.client = boto3.client(
            service_name='bedrock-runtime',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.model_id = settings.BEDROCK_MODEL_ID

    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        system_prompt: Optional[str] = None
    ) -> AIResponse:
        try:
            # Prepare payload for Claude 3
            payload = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1024,
                "messages": messages
            }
            if system_prompt:
                payload["system"] = system_prompt
            
            # Run blocking boto3 call in executor
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.invoke_model(
                    body=json.dumps(payload),
                    modelId=self.model_id,
                    accept="application/json",
                    contentType="application/json"
                )
            )

            response_body = json.loads(response.get('body').read())
            content = response_body.get('content', [{}])[0].get('text', "")
            
            # Note: Bedrock usage stats extraction varies by model and version
            # For simplicity, we initialize with 0 and can refine later
            return AIResponse(
                content=content,
                raw_response=response_body,
                provider="bedrock",
                model=self.model_id,
                prompt_tokens=response_body.get('usage', {}).get('input_tokens', 0),
                completion_tokens=response_body.get('usage', {}).get('output_tokens', 0)
            )
        except Exception as e:
            logger.error(f"Bedrock generation failed for model {self.model_id}: {str(e)}")
            raise
