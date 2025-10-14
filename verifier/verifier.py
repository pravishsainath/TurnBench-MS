from typing import Callable, List, Dict, Any, Optional
import random
import importlib

class Verifier:
    """
    Verifier class that checks if a code satisfies certain criteria
    Each verifier has multiple criteria, but only one is active at a time
    """
    def __init__(
        self, 
        vid: int, 
        description: str, 
        criteria: List[Dict[str, Any]],
    ):
        """Initialize a verifier with id, description and criteria"""
        self.id = vid
        self.description = description
        self.criteria = criteria

    def select_random_criterion(self) -> int:
        """Randomly select one criterion to be active"""
        self.active_index = random.randint(0, len(self.criteria) - 1)
        return self.active_index

    def verify(self, code: str, active_index: int) -> bool:
        """Verify if the code satisfies the active criterion"""
        if active_index >= len(self.criteria):
            raise ValueError("Active index is out of range.")
        
        return self.criteria[active_index]["func"](code)

    def get_active_description(self) -> str:
        """Get the description of the active criterion"""
        if self.active_index is None:
            raise ValueError("Verifier has no active criterion selected.")
        return self.criteria[self.active_index]["description"]
    
    def get_all_criteria_descriptions(self) -> List[str]:
        """Get descriptions of all criteria"""
        return [c["description"] for c in self.criteria]
    
    def to_dict(self, active_index: int=None) -> Dict[str, Any]:
        """Convert a verifier to a dictionary for serialization"""
        criteria_dicts = []
        for criterion in self.criteria:
            criteria_dicts.append({
                "description": criterion["description"],
                "function": criterion.get("function", "")
            })
            
        return {
            "id": self.id,
            "description": self.description,
            "criteria": criteria_dicts,
            "active_index": active_index
        }
