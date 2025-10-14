import os
import yaml
from typing import Dict, List, Any, Optional, Type

from llm.providers.base_client import LLMClient
from llm.providers.openai_client import OpenAIClient
from llm.providers.openrouter_client import OpenRouterClient
from llm.providers.google_client import GoogleClient
from llm.providers.deepseek_client import DeepSeekClient

class LLMManager:
    """
    Manages different LLM clients, acting as a factory and registry.
    Provides a unified interface to get client instances by provider name.
    Ensures only one instance per client type is created.
    """

    # Map provider names to their respective client classes
    SUPPORTED_CLIENTS: Dict[str, Type[LLMClient]] = {
        "openai": OpenAIClient,
        "openrouter": OpenRouterClient,
        "google": GoogleClient,
        "deepseek": DeepSeekClient,
    }

    def __init__(self, config_path: str = 'configs/model_mapping.yaml'):
        """Initialize LLM manager"""
        self._clients: Dict[str, Dict[str, LLMClient]] = {}  # Cache for client instances
        self.MODEL_MAPPING = self._load_model_mapping(config_path)

    def _load_model_mapping(self, config_path: str) -> Dict[str, Dict[str, str]]:
        """Load model mapping from a YAML file"""
        try:
            if not os.path.exists(config_path):
                raise ValueError(f"Model mapping configuration file {config_path} does not exist")
                
            with open(config_path, 'r', encoding='utf-8') as f:
                model_mapping = yaml.safe_load(f)
                
            # Validate loaded data format
            if not isinstance(model_mapping, dict):
                raise ValueError(f"Model mapping configuration file format is incorrect, should be a dictionary")
                
            return model_mapping
        except Exception as e:
            raise ValueError(f"Error loading model mapping configuration file: {e}")

    def get_client(self, provider_name: str) -> LLMClient:
        """Get or create a client instance for the given provider name."""
        provider_name = provider_name.lower()
        if provider_name not in self.SUPPORTED_CLIENTS:
            raise ValueError(f"Unsupported LLM client provider: {provider_name}. Supported: {list(self.SUPPORTED_CLIENTS.keys())}")

        # Return cached instance if available
        if provider_name in self._clients:
            return self._clients[provider_name]

        # Create, cache, and return a new instance
        client_class = self.SUPPORTED_CLIENTS[provider_name]
        try:
            client_instance = client_class()
            self._clients[provider_name] = client_instance
            return client_instance
        except ValueError as e:
            raise ValueError(f"Error initializing client '{provider_name}': {e}")
        except Exception as e:
            raise Exception(f"Unexpected error initializing client '{provider_name}': {e}")

    def list_available_clients(self) -> List[str]:
        """List all supported LLM client providers."""
        return list(self.SUPPORTED_CLIENTS.keys())

    def get_provider_model_name(self, generic_model_name: str, provider_name: str) -> Optional[str]:
        """Get the provider-specific model name for a given generic name and provider."""
        generic_model_name = generic_model_name.lower()
        provider_name = provider_name.lower()
        
        model_info = self.MODEL_MAPPING.get(generic_model_name)
        if not model_info:
            raise ValueError(f"Generic model name '{generic_model_name}' not found in mapping.")
            
        provider_specific_name = model_info.get(provider_name)
        if not provider_specific_name:
            raise ValueError(f"Provider '{provider_name}' mapping not found for model '{generic_model_name}'.")
            
        return provider_specific_name

    def list_available_generic_models(self) -> List[str]:
        """List all generic model names defined in the mapping."""
        return list(self.MODEL_MAPPING.keys())
    
    def list_available_provider_for_generic_model(self, generic_model_name: str) -> List[str]:
        """List all provider names for a given generic model name."""
        generic_model_name = generic_model_name.lower()
        model_info = self.MODEL_MAPPING.get(generic_model_name)
        if not model_info:
            raise ValueError(f"Generic model name '{generic_model_name}' not found in mapping.")
        return list(model_info.keys())
    
    def list_available_models_and_providers(self) -> Dict[str, List[str]]:
        """List all available models and providers."""
        return self.MODEL_MAPPING
