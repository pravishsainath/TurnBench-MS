import importlib
from typing import Dict, List, Any

from verifier.verifier import Verifier

class VerifierFactory:
    """
    Factory class for creating verifiers from config data
    """
    _criteria_functions = None
    
    @classmethod
    def _load_criteria_functions(cls):
        """Load all functions from criteria.py module"""
        if cls._criteria_functions is not None:
            return
            
        try:
            criteria_module = importlib.import_module('verifier.criteria')
            # Create a dictionary of all functions in the module
            cls._criteria_functions = {
                name: func for name, func in criteria_module.__dict__.items()
                if callable(func) and not name.startswith('_')
            }
        except ImportError:
            raise ImportError("Could not import criteria module")
        except Exception as e:
            raise Exception(f"Error loading criteria functions: {e}")
    
    @classmethod
    def create_verifier(cls, config: Dict[str, Any]) -> Verifier:
        """
        Create a verifier from config dictionary
        
        Args:
            config: Dictionary with verifier configuration
            
        Returns:
            Verifier instance
        """
        # Load criteria functions if not already loaded
        cls._load_criteria_functions()
        
        vid = config.get("id")
        description = config.get("description")
        criteria_config = config.get("criteria", [])
        
        # Process criteria to include actual functions
        criteria = []
        for criterion in criteria_config:
            function_name = criterion.get("function")
            if function_name not in cls._criteria_functions:
                raise ValueError(f"Function '{function_name}' not found in criteria module")
                
            criteria.append({
                "description": criterion.get("description"),
                "function": function_name,  # Keep function name for serialization
                "func": cls._criteria_functions[function_name]  # Add actual function
            })
            
        return Verifier(vid, description, criteria)
    
    @classmethod
    def create_verifiers_from_config(cls, config_list: List[Dict[str, Any]]) -> List[Verifier]:
        """
        Create multiple verifiers from a list of config dictionaries
        
        Args:
            config_list: List of verifier configurations
            
        Returns:
            List of Verifier instances
        """
        return [cls.create_verifier(config) for config in config_list]
        
