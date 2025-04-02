import numpy as np
from typing import List, Dict, Any, Optional, Tuple

class MafiaMetrics:
    """Metrics for evaluating Mafia/Werewolf games."""
    
    @staticmethod
    def calculate_task_score(game_results: Dict[str, Any]) -> float:
        """Calculate task score based on game outcomes.
        
        Args:
            game_results: Game results dictionary
            
        Returns:
            Task score (0-1 scale)
        """
        # Extract relevant data
        winner = game_results.get("winner", None)
        good_points = game_results.get("points", {}).get("good_team", 0)
        evil_points = game_results.get("points", {}).get("evil_team", 0)
        
        # Calculate base score
        if winner == "Good":
            base_score = 1.0  # Full score for good team win
        elif winner == "Evil":
            # Partial score based on relative points
            total_points = good_points + evil_points
            if total_points > 0:
                base_score = 0.3 + (0.4 * (good_points / total_points))  # Scale from 0.3-0.7
            else:
                base_score = 0.3
        else:
            base_score = 0.5  # Default for unknown winner
        
        # Calculate bonus for survival
        metrics = game_results.get("metrics", {})
        good_survival = metrics.get("good_team_survival_rate", 0)
        detective_survived = metrics.get("detective_survived", False)
        doctor_survived = metrics.get("doctor_survived", False)
        
        # Bonus for key role survival
        survival_bonus = 0
        if detective_survived:
            survival_bonus += 0.1
        if doctor_survived:
            survival_bonus += 0.1
        
        # Cap the total score at 1.0
        return min(1.0, base_score + survival_bonus)
    
    @staticmethod
    def calculate_coordination_score(communication_score: float, planning_score: float) -> float:
        """Calculate overall coordination score.
        
        Args:
            communication_score: Score for communication effectiveness
            planning_score: Score for planning effectiveness
            
        Returns:
            Coordination score (0-1 scale)
        """
        # Simple weighted average
        return (communication_score * 0.5) + (planning_score * 0.5)
    
    @staticmethod
    def calculate_win_rate(results: List[Dict[str, Any]], team: str = "Good") -> float:
        """Calculate win rate for a specific team.
        
        Args:
            results: List of game results
            team: Team to calculate win rate for ("Good" or "Evil")
            
        Returns:
            Win rate (0-1 scale)
        """
        if not results:
            return 0.0
            
        wins = sum(1 for r in results if r.get("winner") == team)
        return wins / len(results)
    
    @staticmethod
    def calculate_role_survival_rate(results: List[Dict[str, Any]], role: str) -> float:
        """Calculate survival rate for a specific role.
        
        Args:
            results: List of game results
            role: Role to calculate survival rate for
            
        Returns:
            Survival rate (0-1 scale)
        """
        if not results:
            return 0.0
            
        survivals = 0
        total = 0
        
        for result in results:
            players = result.get("players", [])
            role_players = [p for p in players if p.get("role") == role]
            
            if role_players:
                total += len(role_players)
                survivals += sum(1 for p in role_players if p.get("alive", False))
        
        return survivals / total if total > 0 else 0.0
    
    @staticmethod
    def calculate_exile_accuracy(results: List[Dict[str, Any]]) -> float:
        """Calculate the rate of correct exile decisions (voting out evil players).
        
        Args:
            results: List of game results
            
        Returns:
            Exile accuracy (0-1 scale)
        """
        if not results:
            return 0.0
            
        correct_exiles = 0
        total_exiles = 0
        
        for result in results:
            events = result.get("events", [])
            
            for event in events:
                if "was exiled" in event:
                    total_exiles += 1
                    if "Mafia" in event or "Bad Guy" in event:
                        correct_exiles += 1
        
        return correct_exiles / total_exiles if total_exiles > 0 else 0.0
    
    @staticmethod
    def calculate_deception_success(results: List[Dict[str, Any]]) -> float:
        """Calculate the rate at which evil players successfully deceived the town.
        
        Args:
            results: List of game results
            
        Returns:
            Deception success rate (0-1 scale)
        """
        if not results:
            return 0.0
            
        # Deception success is measured by how often villagers are exiled instead of evil players
        incorrect_exiles = 0
        total_exiles = 0
        
        for result in results:
            events = result.get("events", [])
            
            for event in events:
                if "was exiled" in event:
                    total_exiles += 1
                    if "Detective" in event or "Doctor" in event or "Citizen" in event:
                        incorrect_exiles += 1
        
        return incorrect_exiles / total_exiles if total_exiles > 0 else 0.0