import os
from typing import Dict, List, Any, Optional

from openai import OpenAI
from openai.types.chat import ChatCompletionMessage
from models.llm import LLMResponseModel

class LLMClient:
    """Base LLM client class, handling shared logic for all providers"""

    def __init__(
        self, 
        api_key: Optional[str] = None, 
        base_url: Optional[str] = None,
        api_key_env_name: str = "API_KEY", 
        default_base_url: Optional[str] = None
    ) -> None:
        """initialize the base client"""
        # get the API key
        if api_key is None:
            api_key = os.getenv(api_key_env_name)
        if not api_key:
            raise ValueError(f"{api_key_env_name} not provided or found in environment variables.")
        
        if base_url is None and default_base_url:
            base_url = default_base_url

        # create the client instance
        client_kwargs = {"api_key": api_key}
        if base_url:
            client_kwargs["base_url"] = base_url
            
        self.client = OpenAI(**client_kwargs)

    def _get_structured_response(self, response: ChatCompletionMessage) -> Dict[str, Any]:
        """Get structured response from OpenAI API"""
        model_outputs = {
            "content": response.choices[0].message.content.strip(),
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens,
        }

        try:
            model_outputs.update({
                "model_level_reasoning_content": response.choices[0].message.reasoning_content.strip()
            })
        except:
            pass

        try:
            model_outputs.update({
                "prompt_cache_hit_tokens": response.usage.prompt_tokens_details["cached_tokens"]
            })
        except:       
            try:
                model_outputs.update({
                    "prompt_cache_hit_tokens": response.usage.prompt_cache_hit_tokens
                })
            except:
                pass

        try:
            model_outputs.update({
                "reasoning_tokens": response.usage.completion_tokens_details.reasoning_tokens
            })
        except:
            pass

        return model_outputs

    def _get_complete(self, model: str, messages: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
        """use the API to generate a completion"""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                **kwargs
            )
            if response.choices:
                return self._get_structured_response(response)
            else:
                raise Exception("No response choices found.")
        except Exception as e:
            raise e
        
    def complete(self, model: str, messages: List[Dict[str, Any]], **kwargs) -> LLMResponseModel:
        """use the API to generate a completion"""
        raise NotImplementedError("subclass must implement this method")