from typing import Optional, List, Dict, Any

from llm.providers.base_client import LLMClient, LLMResponseModel

class GoogleClient(LLMClient):
    """Google AI Studio API client"""

    DEFAULT_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """initialize the GoogleClient"""
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            api_key_env_name="GOOGLE_AI_STUDIO_API_KEY",
            default_base_url=self.DEFAULT_BASE_URL
        )

    def complete(self, model: str, messages: List[Dict[str, Any]], **kwargs) -> Any:
        """use the API to generate a completion"""
        try:
            # kwargs["reasoning_effort"] = "high"
            kwargs["reasoning_effort"] = "low"
            model_outputs = self._get_complete(model, messages, **kwargs)
        except Exception as e:
            raise e

        model_outputs.update({
            "service_provider": "google"
        })
            
        return LLMResponseModel(**model_outputs)