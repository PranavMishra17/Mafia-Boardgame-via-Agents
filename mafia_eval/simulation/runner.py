import os
import uuid
import json
import logging
import time
import random
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from game.game import Game
from agents.personalities import PERSONALITIES

logger = logging.getLogger(__name__)

class SimulationRunner:
    """Handles running Mafia game simulations."""
    
    def __init__(self, base_dir: str = "./simulation"):
        """Initialize the simulation runner.
        
        Args:
            base_dir: Base directory for simulation outputs
        """
        self.base_dir = base_dir
        # Create the base directory if it doesn't exist
        os.makedirs(base_dir, exist_ok=True)
        
    def run_simulation(self, personalities: Optional[List[str]] = None, 
                      has_human_player: bool = False,
                      num_games: int = 1,
                      fixed_config: Optional[Dict[str, Any]] = None) -> List[str]:
        """Run a set of game simulations.
        
        Args:
            personalities: List of player personalities. If None, random selection
            has_human_player: Whether to include a human player
            num_games: Number of games to simulate
            fixed_config: Fixed configuration options for reproducibility
            
        Returns:
            List of game IDs that were simulated
        """
        game_ids = []
        
        # Validate or randomize personalities
        if personalities is None:
            # Use random personalities from the defined set
            available_personalities = list(PERSONALITIES.keys())
            num_needed = 5 if has_human_player else 6
            personalities = random.sample(available_personalities, num_needed)
            logger.info(f"Randomly selected personalities: {personalities}")
        
        # Run the specified number of games
        for i in range(num_games):
            game_id = str(uuid.uuid4())
            logger.info(f"Starting simulation {i+1}/{num_games}, Game ID: {game_id}")
            
            try:
                # Create game instance
                game = Game(
                    game_id=game_id,
                    personalities=personalities,
                    has_human_player=has_human_player,
                    save_dir=self.base_dir
                )
                
                # Start the game
                game.start_game()
                
                if has_human_player:
                    logger.info("Game initialized with human player, waiting for human interaction")
                    game_ids.append(game_id)
                    continue
                
                # Run full game simulation without human interaction
                self._run_full_game(game)
                game_ids.append(game_id)
                
            except Exception as e:
                logger.error(f"Error in game simulation {game_id}: {str(e)}", exc_info=True)
        
        return game_ids
    
    def run_partial_simulation(self, game_id: str, phase: str = "day") -> Dict[str, Any]:
        """Run a partial simulation starting from a specific game state.
        
        Args:
            game_id: ID of the game to continue/restore
            phase: Phase to simulate ("day" or specific checkpoint)
            
        Returns:
            Results of the partial simulation
        """
        # Find the game checkpoint
        game_dirs = [d for d in os.listdir(self.base_dir) if game_id in d]
        if not game_dirs:
            raise ValueError(f"Game {game_id} not found in {self.base_dir}")
        
        game_dir = os.path.join(self.base_dir, game_dirs[0])
        checkpoints_dir = os.path.join(game_dir, "checkpoints")
        
        # Find appropriate checkpoint file
        checkpoint_files = os.listdir(checkpoints_dir)
        if phase == "day":
            # Find the latest dawn or night checkpoint
            dawn_checkpoints = [f for f in checkpoint_files if "dawn" in f]
            if dawn_checkpoints:
                # Sort to get the latest
                dawn_checkpoints.sort()
                checkpoint_file = dawn_checkpoints[-1]
            else:
                # Fall back to a night checkpoint
                night_checkpoints = [f for f in checkpoint_files if "night" in f]
                if night_checkpoints:
                    night_checkpoints.sort()
                    checkpoint_file = night_checkpoints[-1]
                else:
                    raise ValueError(f"No suitable day-phase checkpoint found for game {game_id}")
        else:
            # Look for specific checkpoint
            matching_checkpoints = [f for f in checkpoint_files if phase in f]
            if not matching_checkpoints:
                raise ValueError(f"No checkpoint matching '{phase}' found for game {game_id}")
            checkpoint_file = matching_checkpoints[0]
        
        # Load checkpoint
        checkpoint_path = os.path.join(checkpoints_dir, checkpoint_file)
        with open(checkpoint_path, 'r') as f:
            checkpoint_data = json.load(f)
        
        logger.info(f"Loaded checkpoint from {checkpoint_path}")
        
        # Create a new partial simulation based on checkpoint
        # This would involve reconstructing the game state and running from there
        # For now, we'll return the checkpoint data
        return {"checkpoint": checkpoint_data, "message": "Partial simulation not fully implemented"}
    
    def _run_full_game(self, game: Game) -> None:
        """Run a full game simulation without human interaction.
        
        Args:
            game: Game instance to simulate
        """
        logger.info(f"Running full game simulation for game {game.id}")
        
        # Continue until game is over
        game_over = False
        while not game_over:
            # Process night phase
            game.process_night()
            
            # Resolve night actions
            game.resolve_night()
            
            # Check if game is over after night
            game_state = game.get_state()
            if game_state["game_over"]:
                logger.info(f"Game {game.id} ended during night phase. Winner: {game_state['winner']}")
                break
            
            # Start discussion
            game.start_discussion()
            
            # Simulate discussion
            game.simulate_discussion(num_rounds=3)
            
            # Process voting
            voting_results = game.process_voting()
            game_over = voting_results["game_over"]
            
            if game_over:
                logger.info(f"Game {game.id} ended after voting. Winner: {voting_results['winner']}")
            else:
                logger.info(f"Round {game.round-1} completed. Starting round {game.round}")
                
                # Optional: Add a small delay between rounds
                time.sleep(0.5)
        
        logger.info(f"Game {game.id} simulation completed")
        
    def load_game(self, game_id: str) -> Optional[Dict[str, Any]]:
        """Load a game's final results.
        
        Args:
            game_id: ID of the game to load
            
        Returns:
            Game results or None if not found
        """
        # Find the game directory
        game_dirs = [d for d in os.listdir(self.base_dir) if game_id in d]
        if not game_dirs:
            logger.warning(f"Game {game_id} not found in {self.base_dir}")
            return None
        
        game_dir = os.path.join(self.base_dir, game_dirs[0])
        results_file = os.path.join(game_dir, "final_results.json")
        
        if not os.path.exists(results_file):
            logger.warning(f"Final results file not found for game {game_id}")
            return None
        
        # Load the results
        with open(results_file, 'r') as f:
            results = json.load(f)
            
        return results