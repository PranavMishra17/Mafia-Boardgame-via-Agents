import os
import json
import logging
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

logger = logging.getLogger(__name__)

class MafiaEvaluator:
    """Evaluates Mafia/Werewolf game simulations."""
    
    def __init__(self, base_dir: str = "./evaluation", sim_dir: str = "./simulation"):
        """Initialize the evaluator.
        
        Args:
            base_dir: Base directory for evaluation outputs
            sim_dir: Directory containing simulation results
        """
        self.base_dir = base_dir
        self.sim_dir = sim_dir
        
        # Create evaluation directory if it doesn't exist
        os.makedirs(base_dir, exist_ok=True)
        
        # Initialize LLM for evaluation
        self.llm = AzureChatOpenAI(
            azure_deployment="VARELab-GPT4o",
            api_key="428KgVArXb6sFyseVYDjElDDYZnlCnx8pNa8CfU5dCic6gjOK89WJQQJ99BBACYeBjFXJ3w3AAABACOG5gtQ",
            api_version="2025-01-01-preview",
            azure_endpoint="https://vare-labs-azure-openai-resource.openai.azure.com/",
            temperature=0.1,  # Low temperature for more consistent evaluations
            max_tokens=1000,
            timeout=None,
            max_retries=2,
        )
    
    def evaluate_game(self, game_id: str, eval_name: str = None) -> Dict[str, Any]:
        """Evaluate a completed game simulation.
        
        Args:
            game_id: ID of the game to evaluate
            eval_name: Custom name for this evaluation
            
        Returns:
            Evaluation results
        """
        if eval_name is None:
            eval_name = f"eval_{game_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
        # Create evaluation directory
        eval_dir = os.path.join(self.base_dir, eval_name)
        os.makedirs(eval_dir, exist_ok=True)
        
        # Find the game directory
        game_dirs = [d for d in os.listdir(self.sim_dir) if game_id in d]
        if not game_dirs:
            raise ValueError(f"Game {game_id} not found in {self.sim_dir}")
        
        game_dir = os.path.join(self.sim_dir, game_dirs[0])
        
        # Load final results
        results_file = os.path.join(game_dir, "final_results.json")
        if not os.path.exists(results_file):
            raise ValueError(f"Final results file not found for game {game_id}")
            
        with open(results_file, 'r') as f:
            game_results = json.load(f)
            
        # Load checkpoints for round-by-round evaluation
        checkpoints_dir = os.path.join(game_dir, "checkpoints")
        checkpoint_files = sorted([f for f in os.listdir(checkpoints_dir) if f.endswith('.json')])
        
        # Skip init and game_start checkpoints
        checkpoint_files = [f for f in checkpoint_files if not (f.startswith('init') or f.startswith('game_start'))]
        
        # Group checkpoints by round
        round_checkpoints = {}
        for file in checkpoint_files:
            round_num = None
            for part in file.split('_'):
                if part.startswith('round') and part[5:].isdigit():
                    round_num = int(part[5:])
                    break
            
            if round_num is not None:
                if round_num not in round_checkpoints:
                    round_checkpoints[round_num] = []
                round_checkpoints[round_num].append(os.path.join(checkpoints_dir, file))
        
        # Evaluate each round
        round_evaluations = {}
        for round_num, checkpoint_paths in round_checkpoints.items():
            round_eval_dir = os.path.join(eval_dir, f"round_{round_num}")
            os.makedirs(round_eval_dir, exist_ok=True)
            
            # Run evaluations for this round
            round_evaluations[round_num] = self._evaluate_round(round_num, checkpoint_paths, round_eval_dir)
            
        # Run global evaluation
        global_eval_dir = os.path.join(eval_dir, "global_evaluation")
        os.makedirs(global_eval_dir, exist_ok=True)
        
        # Evaluate overall game
        global_evaluation = self._evaluate_global(game_results, round_evaluations, global_eval_dir)
        
        # Combine all evaluations
        evaluation_results = {
            "game_id": game_id,
            "evaluation_name": eval_name,
            "round_evaluations": round_evaluations,
            "global_evaluation": global_evaluation
        }
        
        # Save combined evaluation results
        results_path = os.path.join(eval_dir, "evaluation_results.json")
        with open(results_path, 'w') as f:
            json.dump(evaluation_results, f, indent=2)
            
        logger.info(f"Saved evaluation results to {results_path}")
        
        return evaluation_results
    
    def _evaluate_round(self, round_num: int, checkpoint_paths: List[str], 
                        save_dir: str) -> Dict[str, Any]:
        """Evaluate a single round of the game.
        
        Args:
            round_num: Round number
            checkpoint_paths: Paths to checkpoint files for this round
            save_dir: Directory to save evaluation results
            
        Returns:
            Round evaluation results
        """
        logger.info(f"Evaluating round {round_num}")
        
        # Load checkpoints
        checkpoints = []
        for path in checkpoint_paths:
            with open(path, 'r') as f:
                checkpoints.append(json.load(f))
        
        # Sort checkpoints by phase (night, dawn, discussion, voting)
        phases = ["night", "dawn", "discussion", "voting"]
        sorted_checkpoints = sorted(checkpoints, 
                                   key=lambda x: phases.index(x["phase"]) if x["phase"] in phases else 999)
        
        # Extract discussion log if available
        discussion_log = ""
        for checkpoint in sorted_checkpoints:
            if checkpoint["phase"] == "discussion" and checkpoint["discussion_log"]:
                discussion_log = checkpoint["discussion_log"]
                break
        
        # If no discussion found, check other phases
        if not discussion_log:
            for checkpoint in sorted_checkpoints:
                if checkpoint["discussion_log"]:
                    discussion_log = checkpoint["discussion_log"]
                    break
        
        # Evaluate communication effectiveness
        communication_score, communication_feedback = self._evaluate_communication(discussion_log, round_num, save_dir)
        
        # Evaluate strategic planning
        planning_score, planning_feedback = self._evaluate_planning(sorted_checkpoints, round_num, save_dir)
        
        # Create round evaluation
        round_evaluation = {
            "round_num": round_num,
            "communication_score": communication_score,
            "communication_feedback": communication_feedback,
            "planning_score": planning_score,
            "planning_feedback": planning_feedback,
            "coordination_score": (communication_score + planning_score) / 2
        }
        
        # Save round evaluation
        eval_path = os.path.join(save_dir, "round_evaluation.json")
        with open(eval_path, 'w') as f:
            json.dump(round_evaluation, f, indent=2)
            
        logger.info(f"Saved round {round_num} evaluation to {eval_path}")
        
        return round_evaluation
    
    def _evaluate_communication(self, discussion_log: str, round_num: int, 
                              save_dir: str) -> Tuple[float, str]:
        """Evaluate communication effectiveness using LLM.
        
        Args:
            discussion_log: Discussion text for the round
            round_num: Round number
            save_dir: Directory to save evaluation results
            
        Returns:
            Tuple of (score, feedback)
        """
        if not discussion_log:
            return 0.0, "No discussion available for evaluation."
        
        # Prepare prompt for communication evaluation
        prompt = f"""
You are evaluating the communication effectiveness in a Mafia/Werewolf game simulation.
Your task is to rate how well players communicate, share information, and align their decisions.

The discussion log below is from Round {round_num} of a Mafia game.
Some context: In this social deduction game, players are split into two teams:
- Good Team (Villagers): Detective, Doctor, and Citizens
- Evil Team: Mafia and Bad Guy

During the day phase, all players discuss and try to identify the evil players.

Please analyze the discussion log based on the following criteria:
1. Information sharing: How effectively do players share relevant information? Do they explain their reasoning?
2. Alignment: Do good team members work effectively together? Do evil team members subtly coordinate?
3. Strategic discussion: Do players discuss their suspicions and evidence in a logical way?
4. Decision-making: Is there clear progression toward consensus on who to vote out?
5. Deception detection: Do good players show any ability to identify lies or inconsistencies?

Discussion Log:
{discussion_log}

Please provide:
1. A numerical score from 1-5 (where 1 is poor and 5 is excellent) for communication effectiveness
2. A brief explanation of your score, highlighting strengths and weaknesses
3. List the key communication strategies observed in this discussion

Output your response in JSON format like this:
{{
  "score": <numerical score 1-5>,
  "explanation": "<your explanation>",
  "key_strategies": ["strategy1", "strategy2", ...]
}}
"""
        
        try:
            messages = [SystemMessage(content=prompt)]
            response = self.llm.invoke(messages).content
            
            # Parse JSON response
            try:
                evaluation = json.loads(response)
                score = float(evaluation["score"])
                feedback = evaluation["explanation"]
                
                # Normalize score to 0-1 range
                normalized_score = (score - 1) / 4
                
                # Save detailed evaluation
                eval_path = os.path.join(save_dir, "communication_evaluation.json")
                with open(eval_path, 'w') as f:
                    json.dump(evaluation, f, indent=2)
                
                return normalized_score, feedback
                
            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Error parsing LLM response for communication evaluation: {str(e)}")
                logger.error(f"Raw response: {response}")
                return 0.0, "Error in evaluation."
                
        except Exception as e:
            logger.error(f"Error in communication evaluation: {str(e)}")
            return 0.0, f"Evaluation error: {str(e)}"
    
    def _evaluate_planning(self, checkpoints: List[Dict[str, Any]], round_num: int, 
                         save_dir: str) -> Tuple[float, str]:
        """Evaluate strategic planning effectiveness.
        
        Args:
            checkpoints: Checkpoints for this round
            round_num: Round number
            save_dir: Directory to save evaluation results
            
        Returns:
            Tuple of (score, feedback)
        """
        # Extract relevant information from checkpoints
        checkpoint_data = []
        for checkpoint in checkpoints:
            phase_data = {
                "phase": checkpoint["phase"],
                "players": [{"name": p["name"], "role": p["role"], "alive": p["alive"]} 
                           for p in checkpoint["players"]],
                "night_actions": {} if "night_actions" not in checkpoint else checkpoint["night_actions"],
                "points": checkpoint.get("points", {})
            }
            checkpoint_data.append(phase_data)
            
        # Prepare prompt for planning evaluation
        prompt = f"""
You are evaluating the strategic planning effectiveness in a Mafia/Werewolf game simulation.
Your task is to rate how well players coordinate their actions and make strategic decisions.

The checkpoint data below is from Round {round_num} of a Mafia game.
Some context: In this social deduction game, players are split into two teams:
- Good Team (Villagers): Detective, Doctor, and Citizens
- Evil Team: Mafia and Bad Guy

During the night phase, special roles take actions:
- Mafia: Chooses a player to eliminate
- Detective: Investigates a player to determine if they're Mafia
- Doctor: Protects a player from elimination

Please analyze the checkpoint data based on the following criteria:
1. Role effectiveness: How well do players use their special abilities?
2. Target selection: Are night actions strategically chosen?
3. Coordination: Do teams show evidence of coordinated strategy?
4. Adaptability: Do players adjust strategies based on game events?
5. Outcome: Did the actions lead to successful outcomes for either team?

Checkpoint Data:
{json.dumps(checkpoint_data, indent=2)}

Please provide:
1. A numerical score from 1-5 (where 1 is poor and 5 is excellent) for planning effectiveness
2. A brief explanation of your score, highlighting strengths and weaknesses
3. List the key strategic decisions observed in this round

Output your response in JSON format like this:
{{
  "score": <numerical score 1-5>,
  "explanation": "<your explanation>",
  "key_decisions": ["decision1", "decision2", ...]
}}
"""
        
        try:
            messages = [SystemMessage(content=prompt)]
            response = self.llm.invoke(messages).content
            
            # Parse JSON response
            try:
                evaluation = json.loads(response)
                score = float(evaluation["score"])
                feedback = evaluation["explanation"]
                
                # Normalize score to 0-1 range
                normalized_score = (score - 1) / 4
                
                # Save detailed evaluation
                eval_path = os.path.join(save_dir, "planning_evaluation.json")
                with open(eval_path, 'w') as f:
                    json.dump(evaluation, f, indent=2)
                
                return normalized_score, feedback
                
            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Error parsing LLM response for planning evaluation: {str(e)}")
                logger.error(f"Raw response: {response}")
                return 0.0, "Error in evaluation."
                
        except Exception as e:
            logger.error(f"Error in planning evaluation: {str(e)}")
            return 0.0, f"Evaluation error: {str(e)}"
    
    def _evaluate_global(self, game_results: Dict[str, Any], 
                        round_evaluations: Dict[int, Dict[str, Any]],
                        save_dir: str) -> Dict[str, Any]:
        """Evaluate the overall game.
        
        Args:
            game_results: Final game results
            round_evaluations: Evaluation results for each round
            save_dir: Directory to save evaluation results
            
        Returns:
            Global evaluation results
        """
        logger.info("Performing global game evaluation")
        
        # Calculate average coordination score across rounds
        coordination_scores = [round_eval["coordination_score"] for round_eval in round_evaluations.values()]
        avg_coordination_score = sum(coordination_scores) / len(coordination_scores) if coordination_scores else 0
        
        # Extract points from final game results
        good_points = game_results["points"].get("good_team", 0)
        evil_points = game_results["points"].get("evil_team", 0)
        
        # Calculate task completion metrics
        winner = game_results.get("winner", "Unknown")
        
        # Determine task score based on winner and points
        if winner == "Good":
            # Villagers won - full task completion
            task_completion_rate = 1.0
            task_score = 1.0
        elif winner == "Evil":
            # Mafia won - partial task completion based on points
            # Get the ratio of good points to total points as a measure of partial success
            total_points = good_points + evil_points
            task_completion_rate = good_points / total_points if total_points > 0 else 0
            task_score = task_completion_rate * 0.7  # Scale down since they lost
        else:
            # Unknown outcome
            task_completion_rate = 0.5
            task_score = 0.5
        
        # Calculate other performance metrics
        metrics = game_results.get("metrics", {})
        good_survival = metrics.get("good_team_survival_rate", 0)
        
        # Create global evaluation
        global_evaluation = {
            "task_score": task_score,
            "coordination_score": avg_coordination_score,
            "communication_score": sum(round_eval["communication_score"] for round_eval in round_evaluations.values()) / len(round_evaluations) if round_evaluations else 0,
            "planning_score": sum(round_eval["planning_score"] for round_eval in round_evaluations.values()) / len(round_evaluations) if round_evaluations else 0,
            "winner": winner,
            "good_team_points": good_points,
            "evil_team_points": evil_points,
            "task_completion_rate": task_completion_rate,
            "good_team_survival_rate": good_survival,
            "rounds_played": game_results.get("rounds_played", 0)
        }
        
        # Calculate overall performance score
        global_evaluation["overall_score"] = (global_evaluation["task_score"] + global_evaluation["coordination_score"]) / 2
        
        # Save global evaluation
        eval_path = os.path.join(save_dir, "global_evaluation.json")
        with open(eval_path, 'w') as f:
            json.dump(global_evaluation, f, indent=2)
            
        logger.info(f"Saved global evaluation to {eval_path}")
        
        return global_evaluation
    
    def aggregate_evaluations(self, eval_names: List[str] = None) -> Dict[str, Any]:
        """Aggregate evaluations across multiple games.
        
        Args:
            eval_names: List of evaluation names to aggregate. If None, use all.
            
        Returns:
            Aggregated evaluation results
        """
        # Get all evaluation directories if none specified
        if eval_names is None:
            eval_names = [d for d in os.listdir(self.base_dir) 
                         if os.path.isdir(os.path.join(self.base_dir, d))]
        
        all_evaluations = []
        
        # Load each evaluation
        for eval_name in eval_names:
            eval_dir = os.path.join(self.base_dir, eval_name)
            eval_file = os.path.join(eval_dir, "evaluation_results.json")
            
            if os.path.exists(eval_file):
                with open(eval_file, 'r') as f:
                    evaluation = json.load(f)
                    all_evaluations.append(evaluation)
            else:
                logger.warning(f"Evaluation file not found for {eval_name}")
        
        if not all_evaluations:
            return {"error": "No evaluations found"}
        
        # Extract global evaluations
        global_evals = [eval_data["global_evaluation"] for eval_data in all_evaluations]
        
        # Calculate averages for key metrics
        metrics = [
            "task_score", "coordination_score", "communication_score", 
            "planning_score", "overall_score", "good_team_points", 
            "evil_team_points", "task_completion_rate", "good_team_survival_rate"
        ]
        
        aggregated = {}
        for metric in metrics:
            values = [eval_data.get(metric, 0) for eval_data in global_evals]
            aggregated[f"avg_{metric}"] = sum(values) / len(values) if values else 0
            aggregated[f"min_{metric}"] = min(values) if values else 0
            aggregated[f"max_{metric}"] = max(values) if values else 0
        
        # Count winners
        winners = [eval_data.get("winner", "Unknown") for eval_data in global_evals]
        good_wins = sum(1 for w in winners if w == "Good")
        evil_wins = sum(1 for w in winners if w == "Evil")
        
        aggregated["good_win_rate"] = good_wins / len(winners) if winners else 0
        aggregated["evil_win_rate"] = evil_wins / len(winners) if winners else 0
        aggregated["sample_size"] = len(all_evaluations)
        
        # Save aggregated results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_path = os.path.join(self.base_dir, f"aggregated_results_{timestamp}.json")
        with open(results_path, 'w') as f:
            json.dump(aggregated, f, indent=2)
            
        logger.info(f"Saved aggregated results to {results_path}")
        
        return aggregated