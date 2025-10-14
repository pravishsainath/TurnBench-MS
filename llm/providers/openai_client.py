import os
from typing import Dict, List, Any, Optional

from llm.providers.base_client import LLMClient, LLMResponseModel

class OpenAIClient(LLMClient):
    """OpenAI API client"""

    def __init__(self, api_key: Optional[str] = None):
        """initialize the OpenAI client"""
        super().__init__(
            api_key=api_key,
            api_key_env_name="OPENAI_API_KEY"
        )

    def complete(self, model: str, messages: List[Dict[str, Any]], **kwargs) -> Any:
        """use the API to generate a completion"""
        try:
            model_outputs = self._get_complete(model, messages, **kwargs)
        except Exception as e:
            raise e

        model_outputs.update({
            "service_provider": "openai"
        })
            
        return LLMResponseModel(**model_outputs)
