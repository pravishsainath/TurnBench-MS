from typing import Optional, List, Dict, Any

from llm.providers.base_client import LLMClient, LLMResponseModel

class DeepSeekClient(LLMClient):
    """DeepSeek API client"""

    DEFAULT_BASE_URL = "https://api.deepseek.com"

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """initialize the DeepSeek client"""
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            api_key_env_name="DEEPSEEK_API_KEY",
            default_base_url=self.DEFAULT_BASE_URL
        )
        
    def _reformat_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """reformat the messages"""
        return [{"role": message["role"], "content": message["content"][0]["text"]} for message in messages]
    
    def complete(self, model: str, messages: List[Dict[str, Any]], **kwargs) -> LLMResponseModel:
        """use the API to generate a completion"""
        try:
            reformatted_messages = self._reformat_messages(messages)
            model_outputs = self._get_complete(model, reformatted_messages, **kwargs)
        except Exception as e:
            raise e

        model_outputs.update({
            "service_provider": "deepseek"
        })
            
        return LLMResponseModel(**model_outputs)