"""
Roles for the Mafia/Werewolf game.
This module defines the roles, their abilities, and teams.
"""
from typing import Dict, List, Any, Optional

# Role definitions with their properties
ROLES = {
    "Mafia": {
        "team": "Evil",
        "description": "Member of the evil team who eliminates players at night.",
        "night_ability": "kill",
        "night_ability_description": "Choose a player to eliminate during the night phase.",
        "win_condition": "Mafia and Bad Guy players must equal or outnumber the good players.",
        "knows_evil": True  # Knows who the other evil players are
    },
    "Bad Guy": {
        "team": "Evil",
        "description": "Member of the evil team who works with the Mafia.",
        "night_ability": None,
        "night_ability_description": "No special night ability, but works with Mafia during discussions.",
        "win_condition": "Mafia and Bad Guy players must equal or outnumber the good players.",
        "knows_evil": True  # Knows who the other evil players are
    },
    "Detective": {
        "team": "Good",
        "description": "Investigator who can check one player's identity each night.",
        "night_ability": "investigate",
        "night_ability_description": "Choose a player to investigate. You will learn if they are Mafia.",
        "win_condition": "All evil players must be eliminated.",
        "knows_evil": False
    },
    "Doctor": {
        "team": "Good",
        "description": "Healer who can protect one player from elimination each night.",
        "night_ability": "protect",
        "night_ability_description": "Choose a player to protect. If the Mafia targets them, they will survive.",
        "win_condition": "All evil players must be eliminated.",
        "knows_evil": False
    },
    "Citizen": {
        "team": "Good",
        "description": "Regular villager with no special abilities.",
        "night_ability": None,
        "night_ability_description": "No special night ability, but your vote is crucial during the day.",
        "win_condition": "All evil players must be eliminated.",
        "knows_evil": False
    }
}

# Team composition rules
TEAM_RULES = {
    "Evil": {
        "min_players": 2,
        "max_ratio": 0.33,  # Maximum percentage of total players
        "roles": ["Mafia", "Bad Guy"]
    },
    "Good": {
        "min_players": 4,
        "roles": ["Detective", "Doctor", "Citizen"]
    }
}

def get_role_info(role_name: str) -> Dict[str, Any]:
    """Get information about a specific role.
    
    Args:
        role_name: Name of the role
        
    Returns:
        Dictionary with role information
    """
    if role_name in ROLES:
        return ROLES[role_name]
    else:
        raise ValueError(f"Unknown role: {role_name}")

def get_team_members(role_name: str) -> List[str]:
    """Get a list of roles on the same team.
    
    Args:
        role_name: Name of the role
        
    Returns:
        List of roles on the same team
    """
    if role_name not in ROLES:
        raise ValueError(f"Unknown role: {role_name}")
        
    team = ROLES[role_name]["team"]
    return [r for r, info in ROLES.items() if info["team"] == team]

def get_default_role_distribution(player_count: int) -> Dict[str, int]:
    """Get default distribution of roles based on player count.
    
    Args:
        player_count: Number of players
        
    Returns:
        Dictionary with role counts
    """
    if player_count < 6:
        raise ValueError("Game requires at least 6 players")
        
    # Default distribution for different player counts
    if player_count == 6:
        return {
            "Mafia": 1,
            "Bad Guy": 1,
            "Detective": 1,
            "Doctor": 1,
            "Citizen": 2
        }
    elif player_count <= 8:
        return {
            "Mafia": 1,
            "Bad Guy": 1,
            "Detective": 1,
            "Doctor": 1,
            "Citizen": player_count - 4
        }
    else:
        # For larger games, scale up evil team
        mafia_count = max(1, player_count // 6)
        bad_guy_count = max(1, player_count // 8)
        
        return {
            "Mafia": mafia_count,
            "Bad Guy": bad_guy_count,
            "Detective": 1,
            "Doctor": 1,
            "Citizen": player_count - (mafia_count + bad_guy_count + 2)
        }

def check_night_ability(role_name: str) -> Optional[str]:
    """Check if a role has a night ability.
    
    Args:
        role_name: Name of the role
        
    Returns:
        Name of the ability or None
    """
    if role_name in ROLES:
        return ROLES[role_name]["night_ability"]
    return None

def get_night_action_target_validation(role_name: str, target_role: str) -> bool:
    """Check if a night action target is valid for the role.
    
    Args:
        role_name: Name of the role performing the action
        target_role: Role of the target
        
    Returns:
        Whether the target is valid
    """
    # Default validation rules
    if role_name == "Mafia":
        # Mafia can't target other evil team members
        return ROLES[target_role]["team"] != "Evil"
    elif role_name == "Detective":
        # Detective can investigate anyone
        return True
    elif role_name == "Doctor":
        # Doctor can protect anyone, including themselves
        return True
    else:
        # Roles without night abilities can't target anyone
        return False

def process_night_action(role_name: str, action_type: str, 
                         target_role: str, additional_info: Dict[str, Any] = None) -> Dict[str, Any]:
    """Process a night action and determine the outcome.
    
    Args:
        role_name: Name of the role performing the action
        action_type: Type of action (kill, investigate, protect)
        target_role: Role of the target
        additional_info: Additional information for processing
        
    Returns:
        Dictionary with action outcome
    """
    result = {
        "success": False,
        "message": "",
        "target_role": target_role,
        "points_earned": 0
    }
    
    if action_type == "kill" and role_name == "Mafia":
        # Check if target was protected
        if additional_info and additional_info.get("protected_target") == additional_info.get("target_name"):
            result["success"] = False
            result["message"] = "Target was protected by the Doctor."
        else:
            result["success"] = True
            result["message"] = "Successfully eliminated target."
            
            # Award points based on target's role
            if target_role == "Detective":
                result["points_earned"] = 3
            elif target_role == "Doctor":
                result["points_earned"] = 2
            else:
                result["points_earned"] = 1
                
    elif action_type == "investigate" and role_name == "Detective":
        result["success"] = True
        result["is_mafia"] = (target_role == "Mafia")
        
        if target_role == "Mafia":
            result["message"] = "Your investigation reveals that the target is a member of the Mafia!"
            result["points_earned"] = 1
        else:
            result["message"] = "Your investigation reveals that the target is NOT a member of the Mafia."
            
    elif action_type == "protect" and role_name == "Doctor":
        result["success"] = True
        result["message"] = "You have protected your target for this night."
        
        # Points awarded only if protection was successful (determined later)
        
    return result