import os
from typing import Any, Dict, List, Optional

from openai import OpenAI

from models.llm import LLMResponseModel


class LLMClient:
    """Base LLM client class, handling shared logic for all providers."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        api_key_env_name: str = "API_KEY",
        default_base_url: Optional[str] = None,
    ) -> None:
        """Initialize the base OpenAI-compatible client."""
        api_key = api_key or os.getenv(api_key_env_name)
        if not api_key:
            raise ValueError(f"{api_key_env_name} not provided or found in environment variables.")

        if base_url is None:
            base_url = default_base_url

        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def _get_structured_response(self, response: Any) -> Dict[str, Any]:
        """Convert an OpenAI response object into a structured dict."""
        if not getattr(response, "choices", None):
            raise ValueError("No response choices found.")

        message = response.choices[0].message
        text = message.content if message and getattr(message, "content", None) is not None else ""

        model_outputs: Dict[str, Any] = {
            "text": text,
            "content": text,
        }

        reasoning_content = getattr(message, "reasoning_content", None) if message else None
        if reasoning_content:
            model_outputs["model_level_reasoning_content"] = reasoning_content

        usage = getattr(response, "usage", None)
        if usage:
            model_outputs.update(
                {
                    "input_tokens": getattr(usage, "prompt_tokens", 0),
                    "output_tokens": getattr(usage, "completion_tokens", 0),
                    "total_tokens": getattr(usage, "total_tokens", 0),
                }
            )

            try:
                prompt_tokens_details = getattr(usage, "prompt_tokens_details", None)
                if prompt_tokens_details and "cached_tokens" in prompt_tokens_details:
                    model_outputs["prompt_cache_hit_tokens"] = prompt_tokens_details["cached_tokens"]
                elif hasattr(usage, "prompt_cache_hit_tokens"):
                    model_outputs["prompt_cache_hit_tokens"] = usage.prompt_cache_hit_tokens
            except Exception:
                pass

            try:
                completion_tokens_details = getattr(usage, "completion_tokens_details", None)
                if completion_tokens_details and hasattr(completion_tokens_details, "reasoning_tokens"):
                    model_outputs["reasoning_tokens"] = completion_tokens_details.reasoning_tokens
            except Exception:
                pass

        return model_outputs

    def _get_complete(self, model: str, messages: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
        """Use the API to generate a completion."""
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs,
        )

        if not response.choices:
            raise ValueError("No response choices found.")

        return self._get_structured_response(response)

    def complete(self, model: str, messages: List[Dict[str, Any]], **kwargs) -> LLMResponseModel:
        """Use the API to generate a completion."""
        raise NotImplementedError("subclass must implement this method")
