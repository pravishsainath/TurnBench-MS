from typing import Dict, List, Any, Tuple, Callable
from verifier.verifier import Verifier
import json
import os
from verifier.verifier_factory import VerifierFactory

class VerifierManager:
    """
    Verifier manager, responsible for managing all verifiers in the game
    Provide interfaces for creating, registering and using verifiers
    """
    
    def __init__(self):
        """Initialize verifier manager"""
        self.verifiers = {}

    def verify(self, vid: int, code: str, active_index: int) -> bool:
        """Verify code with specified verifier"""
        verifier = self.get_verifier_by_id(vid)
        return verifier.verify(code, active_index)

    def get_verifier_descriptions(self, verifier_list: List[int]) -> str:
        """Get all verifier descriptions"""
        if not verifier_list:
            raise ValueError("Verifier list is empty")
        
        descriptions = []
        for i, vid in enumerate(verifier_list):
            verifier = self.get_verifier_by_id(vid)
            desc = f"Verifier <{i}>: {verifier.description}"
            
            # Add criteria description
            criteria_descs = []
            for criterion in verifier.criteria:
                criteria_descs.append(f"- Possible criteria: {criterion['description']}")
            
            criteria_str = "\n".join(criteria_descs)
            descriptions.append(f"{desc}\n{criteria_str}")
        
        return "\n".join(descriptions)
       
    def get_verifier_by_id(self, vid: int) -> Verifier:
        """Get verifier by ID"""
        if vid not in self.verifiers:
            raise ValueError(f"Verifier with ID {vid} not found")
        return self.verifiers[vid]
    
    def get_verifier_dict_by_id(self, vid: int) -> Dict[str, Any]:
        """Get verifier in dictionary format by ID"""
        return self.get_verifier_by_id(vid).to_dict()
    
    def get_verifiers_by_ids(self, vids: List[int]) -> List[Dict[str, Any]]:
        """Get verifiers in dictionary format by IDs"""
        return {vid: self.get_verifier_by_id(vid) for vid in vids}
    
    def get_verifiers_by_ids_dict(self, vids: List[int]) -> Dict[int, Dict[str, Any]]:
        """Get verifiers in dictionary format by IDs"""
        return {vid: self.get_verifier_dict_by_id(vid) for vid in vids}
    
    def get_all_verifiers(self) -> Dict[int, Verifier]:
        """Get all verifiers"""
        return self.verifiers
    
    def get_all_verifiers_dict(self) -> Dict[int, Dict[str, Any]]:
        """Get all verifiers in dictionary format"""
        return {vid: self.get_verifier_dict_by_id(vid) for vid in self.verifiers}
    
    def get_verifier_description(self, vid: int) -> str:
        """Get verifier description"""
        verifier = self.get_verifier_by_id(vid)
        return verifier.description
    
    def get_criterion_by_verifier_id_and_criterion_index(self, vid: int, index: int) -> Dict[str, Any]:
        """Get criterion by verifier ID and criterion index"""
        return self.get_verifier_by_id(vid).criteria[index]
    
    
    def load_verifiers_from_config(self, config_path: str) -> None:
        """Load verifiers from config file"""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file {config_path} not found")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            verifiers_config = json.load(f)
        
        # clear all verifiers
        self.verifiers = {}
        
        # create verifiers
        for verifier_config in verifiers_config:
            verifier = VerifierFactory.create_verifier(verifier_config)
            self.verifiers[verifier.id] = verifier
    
    @classmethod
    def from_json(cls, json_path: str) -> 'VerifierManager':
        """Create verifier manager from json file"""
        verifier_manager = cls()
        verifier_manager.load_verifiers_from_config(json_path)
        return verifier_manager

    