import os
import json
from typing import Dict, Any

import yaml

def load_json_file(file_path: str) -> Dict[str, Any]:
    """load json file"""
    if not file_path or not os.path.exists(file_path):
        raise ValueError(f"File not found: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise Exception(f"Error loading json file: {e}")

def save_json_file(data: Dict[str, Any], file_path: str):
    """save json file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        raise Exception(f"Error saving json file: {e}")

def load_yaml_config(yaml_path: str) -> Dict[str, Any]:
    """load yaml config"""
    config_path = yaml_path
    if not config_path or not os.path.exists(config_path):
        raise ValueError(f"Config file not found: {config_path}")
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            yaml_config = yaml.safe_load(f)
            return yaml_config or {}
    except Exception as e:
        raise Exception(f"Error loading yaml config: {e}")