from typing import Dict
import importlib

class PromptManager:
    """
    Prompt manager, responsible for managing and organizing various prompts used in the game
    Supports template replacement and prompt combination
    """
    PROMPT_CATEGORIES = ["system_prompts", "proposal_prompts", "question_prompts", "deduce_prompts"]
    
    def __init__(self):
        """Initialize prompt manager and load templates from specific modules."""
        self.available_prompts = {}
        self._load_prompts()
    
    def _load_prompts(self):
        """Load prompts from specific modules."""
        for module_name in self.PROMPT_CATEGORIES:
            try:
                # Construct the full module path
                module_path = f'prompt.templates.{module_name}'
                module = importlib.import_module(module_path)
                
                # Iterate through the module's contents
                for name, value in module.__dict__.items():
                    # Load string variables that don't start with an underscore
                    if isinstance(value, str) and not name.startswith('_'):
                        self.available_prompts[name] = value
                        
            except ImportError:
                print(f"Warning: Could not import prompt templates from {module_path}. Module not found or contains errors.")
            except Exception as e:
                print(f"Warning: An error occurred while loading prompts from {module_path}: {e}")
        
    def get_prompt(self, template_name: str) -> str:
        """get the prompt with variables"""
        if template_name not in self.available_prompts:
            raise ValueError(f"Template '{template_name}' not found")
        template = self.available_prompts[template_name]
        return template
    
    def get_all_template_names(self) -> Dict[str, list]:
        """get all template names"""
        return list(self.available_prompts.keys())
