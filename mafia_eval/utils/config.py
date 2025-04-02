import os
import json
from typing import Dict, Any, Optional

DEFAULT_CONFIG = {
    "api_key": "428KgVArXb6sFyseVYDjElDDYZnlCnx8pNa8CfU5dCic6gjOK89WJQQJ99BBACYeBjFXJ3w3AAABACOG5gtQ",
    "endpoint": "https://vare-labs-azure-openai-resource.openai.azure.com/",
    "deployment": "VARELab-GPT4o",
    "api_version": "2025-01-01-preview",
    "simulation": {
        "base_dir": "./simulation",
        "default_personalities": [
            "Diplomat",
            "Sheriff",
            "Conspirator",
            "Jester",
            "Mastermind",
            "Empath"
        ],
        "default_game_count": 5
    },
    "evaluation": {
        "base_dir": "./evaluation",
        "metrics": {
            "task_score_weight": 0.5,
            "coordination_score_weight": 0.5
        }
    },
    "reporting": {
        "base_dir": "./reports"
    },
    "logging": {
        "log_dir": "./logs",
        "level": "INFO"
    }
}

def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from file or use defaults.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    config = DEFAULT_CONFIG.copy()
    
    if config_path and os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                
            # Update default config with user-provided values
            _update_nested_dict(config, user_config)
        except Exception as e:
            print(f"Error loading config file: {str(e)}")
            print("Using default configuration")
    
    return config

def save_config(config: Dict[str, Any], config_path: str) -> None:
    """Save configuration to file.
    
    Args:
        config: Configuration dictionary
        config_path: Path to save configuration
    """
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        print(f"Configuration saved to {config_path}")
    except Exception as e:
        print(f"Error saving config file: {str(e)}")

def _update_nested_dict(original: Dict[str, Any], update: Dict[str, Any]) -> None:
    """Update nested dictionary recursively.
    
    Args:
        original: Original dictionary to update
        update: Dictionary with updates
    """
    for key, value in update.items():
        if key in original and isinstance(original[key], dict) and isinstance(value, dict):
            _update_nested_dict(original[key], value)
        else:
            original[key] = value