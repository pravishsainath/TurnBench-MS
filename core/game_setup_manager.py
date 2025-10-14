from typing import Dict, List, Any
import json

from models.game import GameSetupModel

class GameSetupManager:
    """
    Game setup manager, responsible for managing the configuration and load specific game setup
    """
    
    def __init__(self, setups: Dict[str, Dict[str, Any]]) -> None:
        """Initialize game setup"""
        self.setups = setups
        
    def load_setup(self, setup_id: str) -> GameSetupModel:
        """Load game setup"""
        try:
            return GameSetupModel(**{**self.setups[setup_id], "setup_id": setup_id})
        except Exception as e:
            raise ValueError(f"Error loading game setup - {setup_id}: {e}")

    def get_setup(self, setup_id: str) -> Dict[str, Any]:
        """Get setup"""
        return self.setups[setup_id]

    def set_active_criteria_ids_by_setup_id(self, setup_id: str, active_criteria_ids: List[int]) -> None:
        """Set active criteria ids by setup id"""
        try:
            self.setups[setup_id]["active_criteria_ids"] = active_criteria_ids
        except Exception as e:
            raise ValueError(f"Error setting active criteria ids for setup {setup_id}: {e}")
    
    def to_json(self, json_path: str) -> None:
        """Save game setup to json file"""
        try:
            with open(json_path, "w") as f:
                json.dump(self.setups, f, indent=4, ensure_ascii=False)
        except Exception as e:
            raise ValueError(f"Error saving game setup to json file: {e}")

    @classmethod
    def from_json(cls, json_path: str) -> 'GameSetupManager':
        """Create game setup from json file"""
        try:
            with open(json_path, "r") as f:
                setups = json.load(f)
            return cls(setups)
        except Exception as e:
            raise ValueError(f"Error creating game setup from json file: {e}")
