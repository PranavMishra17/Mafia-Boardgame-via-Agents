import logging
import random
import uuid
import json
import os
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from agents.player import Player

logger = logging.getLogger(__name__)

class Game:
    """Main game class for Mafia/Werewolf simulation."""
    
    def __init__(self, game_id: str, personalities: List[str], has_human_player: bool = False,
                 save_dir: str = "./simulation"):
        """Initialize a new game.
        
        Args:
            game_id: Unique game identifier
            personalities: List of personality types for AI players
            has_human_player: Whether the game includes a human player
            save_dir: Directory to save game logs and results
        """
        self.id = game_id
        self.players = []
        self.phase = "setup"
        self.round = 0
        self.events_log = []
        self.discussion_log = []
        self.night_actions = {
            "mafia_target": None,
            "detective_target": None,
            "doctor_target": None
        }
        self.has_human_player = has_human_player
        self.save_dir = os.path.join(save_dir, f"{game_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        os.makedirs(self.save_dir, exist_ok=True)
        
        # Create a checkpoints directory
        self.checkpoints_dir = os.path.join(self.save_dir, "checkpoints")
        os.makedirs(self.checkpoints_dir, exist_ok=True)
        
        # Create a directory for player thoughts
        self.thoughts_dir = os.path.join(self.save_dir, "thoughts")
        os.makedirs(self.thoughts_dir, exist_ok=True)
        
        # Track points for evaluation
        self.points = {
            "good_team": 0,
            "evil_team": 0
        }
        
        # Create players with selected personalities
        player_offset = 0
        if has_human_player:
            # Create human player first
            self.players.append(Player("Player_1", "Human", is_human=True))
            player_offset = 1
        
        # Then add AI personalities with proper offset
        for i, personality in enumerate(personalities):
            player_name = f"Player_{i+1+player_offset}"
            self.players.append(Player(player_name, personality))
        
        # Assign roles
        self.assign_roles()
        logger.info(f"Game {game_id} initialized with {len(self.players)} players")
        
        # Save initial game state
        self._save_checkpoint("init")
                
    def assign_roles(self) -> None:
        """Assign roles to players randomly."""
        # Shuffle players
        random.shuffle(self.players)
        
        # Assign roles
        roles = ["Mafia", "Bad Guy", "Detective", "Doctor"] + ["Citizen"] * (len(self.players) - 4)
        for i, player in enumerate(self.players):
            player.role = roles[i]
            logger.info(f"Assigned {player.name} as {player.role} with {player.personality} personality")
            
    def start_game(self) -> Dict[str, Any]:
        """Start the game and begin the first night phase.
        
        Returns:
            Current game state
        """
        self.phase = "night"
        self.round = 1
        self.events_log.append(f"Game started. Round {self.round}.")
        logger.info(f"Game {self.id} started with {len(self.players)} players")
        
        # Save game state after starting
        self._save_checkpoint("game_start")
        
        return self.get_state()
        
    def get_state(self) -> Dict[str, Any]:
        """Get the current game state.
        
        Returns:
            Dictionary containing game state information
        """
        game_over, winner = self.check_game_over()
        
        return {
            "id": self.id,
            "players": self.players,
            "phase": self.phase,
            "round": self.round,
            "events_log": "\n".join(self.events_log),
            "discussion_log": "\n".join(self.discussion_log) if self.discussion_log else "",
            "game_over": game_over,
            "winner": winner,
            "points": self.points
        }
        
    def process_night(self) -> Dict[str, Any]:
        """Process night phase actions.
        
        Returns:
            Dictionary of night actions
        """
        logger.info(f"Processing night phase for round {self.round}")
        
        # Reset night actions
        self.night_actions = {
            "mafia_target": None,
            "detective_target": None,
            "doctor_target": None
        }
        
        # Get night actions from respective roles
        for player in self.players:
            if not player.alive:
                continue
                
            if player.role == "Mafia":
                self.night_actions["mafia_target"] = player.make_night_decision(self.get_state())
            elif player.role == "Detective":
                self.night_actions["detective_target"] = player.make_night_decision(self.get_state())
            elif player.role == "Doctor":
                self.night_actions["doctor_target"] = player.make_night_decision(self.get_state())
                
        logger.info(f"Night actions: {self.night_actions}")
        
        # Save checkpoint after night decisions
        self._save_checkpoint(f"round{self.round}_night_decisions")
        
        return self.night_actions
        
    def resolve_night(self) -> Dict[str, Any]:
        """Resolve the night phase and transition to dawn.
        
        Returns:
            Dictionary containing dawn results
        """
        logger.info(f"Resolving night phase for round {self.round}")
        self.phase = "dawn"
        
        # Process detective investigation
        detective_success = False
        detective_points = 0
        if self.night_actions["detective_target"]:
            target_player = next((p for p in self.players if p.name == self.night_actions["detective_target"]), None)
            if target_player and target_player.role == "Mafia":
                detective_success = True
                detective_points = 1  # Award points for successful investigation
                self.points["good_team"] += detective_points
                logger.info(f"Detective successfully identified Mafia: +{detective_points} points for good team")
                
        # Process doctor protection
        doctor_success = False
        doctor_points = 0
        if self.night_actions["mafia_target"] and self.night_actions["mafia_target"] == self.night_actions["doctor_target"]:
            doctor_success = True
            doctor_points = 2  # Award points for successful protection
            self.points["good_team"] += doctor_points
            logger.info(f"Doctor successfully protected target: +{doctor_points} points for good team")
                
        # Process mafia kill
        killed_player = None
        mafia_points = 0
        if self.night_actions["mafia_target"] and self.night_actions["mafia_target"] != self.night_actions["doctor_target"]:
            target_player = next((p for p in self.players if p.name == self.night_actions["mafia_target"]), None)
            if target_player:
                target_player.alive = False
                killed_player = target_player.name
                killed_role = target_player.role
                self.events_log.append(f"{killed_player} ({killed_role}) was killed during the night.")
                
                # Award points to evil team for successful kill
                if target_player.role == "Detective":
                    mafia_points = 3  # Extra points for killing detective
                elif target_player.role == "Doctor":
                    mafia_points = 2  # Extra points for killing doctor
                else:
                    mafia_points = 1  # Standard points for killing citizen
                    
                self.points["evil_team"] += mafia_points
                logger.info(f"Mafia killed {target_player.role}: +{mafia_points} points for evil team")
        
        # Create dawn announcement
        dawn_results = {
            "detective_success": detective_success,
            "detective_points": detective_points,
            "doctor_success": doctor_success,
            "doctor_points": doctor_points,
            "killed_player": killed_player,
            "mafia_points": mafia_points
        }
        
        # Add to event log
        self.events_log.append(f"Dawn of Day {self.round}:")
        if detective_success:
            self.events_log.append("Detective successfully identified the Mafia.")
        else:
            self.events_log.append("Detective failed to identify the Mafia.")
        
        if doctor_success and self.night_actions["mafia_target"]:
            self.events_log.append(f"Doctor successfully saved {self.night_actions['doctor_target']}.")
        elif killed_player:
            self.events_log.append(f"{killed_player} was found dead.")
        else:
            self.events_log.append("No one died during the night.")
            
        logger.info(f"Dawn results: {dawn_results}")
        
        # Save checkpoint after night resolution
        self._save_checkpoint(f"round{self.round}_dawn")
        
        return dawn_results
        
    def start_discussion(self) -> Dict[str, Any]:
        """Start the discussion phase.
        
        Returns:
            Current game state
        """
        logger.info(f"Starting discussion phase for round {self.round}")
        self.phase = "discussion"
        self.discussion_log = []
        
        # Save checkpoint at discussion start
        self._save_checkpoint(f"round{self.round}_discussion_start")
        
        return self.get_state()
        
    def simulate_discussion(self, num_rounds: int = 3) -> None:
        """Simulate the discussion phase with multiple rounds.
        
        Args:
            num_rounds: Number of discussion rounds to simulate
        """
        logger.info(f"Simulating discussion for game {self.id}")
        self.discussion_log = []
        living_players = [p for p in self.players if p.alive]
        
        # Run through each discussion round
        for round_num in range(1, num_rounds + 1):
            # Add round header
            round_header = f"--- Discussion Round {round_num} ---"
            self.discussion_log.append(round_header)
            logger.info(f"Starting discussion round {round_num}")
            
            # Get topic for current round
            if round_num == 1:
                topic = "What do you all think happened last night? Who seems suspicious to you?"
            elif round_num == 2:
                topic = "Let's discuss our suspicions more. Anyone acting strangely?"
            else:
                topic = "We need to decide who to vote out. Make your final case."
            
            # Each player speaks in turn
            for player in living_players:
                # Skip if it's a human player in a full simulation
                if player.is_human:
                    self.discussion_log.append("WAITING_FOR_HUMAN_INPUT")
                    continue
                
                # Get previous messages for context
                previous_messages = self.discussion_log[-min(5, len(self.discussion_log)):]
                previous_context = "\n".join(previous_messages)
                
                # Get player response
                logger.info(f"Getting response from {player.name} ({player.role})")
                try:
                    response = player.generate_response(f"{topic}\n\nPrevious messages:\n{previous_context}", self.get_state())
                    self.discussion_log.append(f"{player.name}: {response}")
                except Exception as e:
                    logger.error(f"Error getting response from {player.name}: {str(e)}")
                    self.discussion_log.append(f"{player.name}: I'm thinking about what to say...")
            
            # Save checkpoint after each discussion round
            self._save_checkpoint(f"round{self.round}_discussion_round{round_num}")
            
            # If there's a human player, we need to stop simulation and wait for input
            if self.has_human_player and any("WAITING_FOR_HUMAN_INPUT" in msg for msg in self.discussion_log):
                logger.info("Pausing discussion simulation for human input")
                return
                
        # Save thoughts for all players
        for player in self.players:
            if not player.is_human and player.thoughts_log:
                player.save_thoughts(self.id, self.round, self.thoughts_dir)
                
        logger.info("Discussion simulation completed")
                
    def human_discussion_input(self, message: str) -> None:
        """Process human player input during discussion.
        
        Args:
            message: Human player's message
        """
        # Find and remove waiting placeholder
        try:
            placeholder_index = self.discussion_log.index("WAITING_FOR_HUMAN_INPUT")
            self.discussion_log.pop(placeholder_index)
        except ValueError:
            logger.warning("No waiting marker found for human input")
        
        # Add human message
        self.discussion_log.append(f"Player_1: {message}")
        logger.info(f"Human player added message: {message[:50]}...")
                
    def process_voting(self) -> Dict[str, Any]:
        """Process voting phase where players vote to exile someone.
        
        Returns:
            Dictionary containing voting results
        """
        logger.info(f"Processing voting phase for round {self.round}")
        self.phase = "voting"
        living_players = [p for p in self.players if p.alive]
        
        # Each living player votes
        votes = {}
        vote_details = {}  # Track who voted for whom
        
        for player in living_players:
            # Skip human player in simulation
            if player.is_human and self.has_human_player:
                continue
                
            vote = player.vote(self.get_state())
            if vote:
                votes[vote] = votes.get(vote, 0) + 1
                vote_details[player.name] = vote
                
        # Find player with most votes
        voting_results = {
            "votes": vote_details,
            "exiled": None,
            "exiled_role": None,
            "game_over": False,
            "winner": None
        }
        
        if votes:
            exiled_player_name = max(votes.items(), key=lambda x: x[1])[0]
            exiled_player = next((p for p in self.players if p.name == exiled_player_name), None)
            
            if exiled_player:
                exiled_player.alive = False
                voting_results["exiled"] = exiled_player.name
                voting_results["exiled_role"] = exiled_player.role
                
                # Award points based on who was exiled
                if exiled_player.role in ["Mafia", "Bad Guy"]:
                    points_awarded = 2
                    self.points["good_team"] += points_awarded
                    logger.info(f"Good team exiled evil player: +{points_awarded} points")
                else:
                    points_awarded = 1
                    self.points["evil_team"] += points_awarded
                    logger.info(f"Evil team got innocent player exiled: +{points_awarded} points")
                
                self.events_log.append(f"{exiled_player.name} ({exiled_player.role}) was exiled from the city.")
                logger.info(f"Player {exiled_player.name} ({exiled_player.role}) was exiled")
                
                # Check if game is over
                game_over, winner = self.check_game_over()
                if game_over:
                    self.events_log.append(f"Game Over! {winner} team wins!")
                    voting_results["game_over"] = True
                    voting_results["winner"] = winner
                    
                    # Award final points
                    if winner == "Good":
                        self.points["good_team"] += 5  # Bonus for winning
                    else:
                        self.points["evil_team"] += 5  # Bonus for winning
                        
                    # Save final game state
                    self._save_checkpoint("game_end")
                    self._save_final_results()
                    
                    # Save thoughts for all players
                    for player in self.players:
                        if not player.is_human and player.thoughts_log:
                            player.save_thoughts(self.id, self.round, self.thoughts_dir)

                    # Ensure we always return a proper result dictionary
                    if voting_results is None:
                        voting_results = {
                            "votes": {},
                            "exiled": None,
                            "exiled_role": None,
                            "game_over": False,
                            "winner": None
                        }
                                                
        return voting_results
        
    def check_game_over(self) -> Tuple[bool, Optional[str]]:
        """Check if the game is over.
        
        Returns:
            Tuple of (is_game_over, winner)
        """
        living_players = [p for p in self.players if p.alive]
        good_count = sum(1 for p in living_players if p.role in ["Detective", "Doctor", "Citizen"])
        evil_count = sum(1 for p in living_players if p.role in ["Mafia", "Bad Guy"])
        
        # Evil wins if they equal or outnumber good
        if evil_count >= good_count:
            return True, "Evil"
            
        # Good wins if all evil are eliminated
        if evil_count == 0:
            return True, "Good"
            
        # Game continues
        return False, None
        
    def human_night_action(self, role: str, target: str) -> None:
        """Record a night action for a human player.
        
        Args:
            role: Human player's role
            target: Target of the night action
        """
        if role == "Mafia":
            self.night_actions["mafia_target"] = target
        elif role == "Detective":
            self.night_actions["detective_target"] = target
        elif role == "Doctor":
            self.night_actions["doctor_target"] = target
            
        logger.info(f"Human player with role {role} chose {target} for night action")
        
    def human_vote(self, target: str) -> None:
        """Record a vote for a human player.
        
        Args:
            target: Player the human is voting for
        """
        # Store the vote for later processing
        if not hasattr(self, 'human_vote_target'):
            self.human_vote_target = {}
            
        self.human_vote_target["Player_1"] = target
        logger.info(f"Human player voted for {target}")
        
    def _save_checkpoint(self, checkpoint_name: str) -> None:
        """Save a checkpoint of the current game state.
        
        Args:
            checkpoint_name: Name of the checkpoint
        """
        filename = os.path.join(self.checkpoints_dir, f"{checkpoint_name}.json")
        
        # Convert game state to JSON-serializable format
        state = self.get_state()
        serializable_state = {
            "id": state["id"],
            "phase": state["phase"],
            "round": state["round"],
            "events_log": state["events_log"],
            "discussion_log": state["discussion_log"],
            "points": state["points"],
            "game_over": state["game_over"],
            "winner": state["winner"],
            "players": []
        }
        
        # Add player information
        for player in self.players:
            serializable_state["players"].append({
                "id": player.id,
                "name": player.name,
                "personality": player.personality,
                "role": player.role,
                "alive": player.alive,
                "is_human": player.is_human
            })
            
        # Save to file
        with open(filename, 'w') as f:
            json.dump(serializable_state, f, indent=2)
            
        logger.info(f"Saved checkpoint: {filename}")
        
    def _save_final_results(self) -> None:
        """Save final game results."""
        filename = os.path.join(self.save_dir, "final_results.json")
        
        # Get final state
        state = self.get_state()
        
        # Create results object
        results = {
            "game_id": self.id,
            "rounds_played": self.round,
            "winner": state["winner"],
            "points": self.points,
            "events": self.events_log,
            "players": []
        }
        
        # Add player information
        for player in self.players:
            results["players"].append({
                "name": player.name,
                "personality": player.personality,
                "role": player.role,
                "alive": player.alive,
                "is_human": player.is_human
            })
            
        # Calculate additional metrics for evaluation
        results["metrics"] = {
            "good_team_survival_rate": sum(1 for p in self.players if p.alive and p.role in ["Detective", "Doctor", "Citizen"]) / 
                                      sum(1 for p in self.players if p.role in ["Detective", "Doctor", "Citizen"]),
            "evil_team_survival_rate": sum(1 for p in self.players if p.alive and p.role in ["Mafia", "Bad Guy"]) / 
                                      sum(1 for p in self.players if p.role in ["Mafia", "Bad Guy"]),
            "detective_survived": any(p.role == "Detective" and p.alive for p in self.players),
            "doctor_survived": any(p.role == "Doctor" and p.alive for p in self.players),
            "mafia_survived": any(p.role == "Mafia" and p.alive for p in self.players),
            "bad_guy_survived": any(p.role == "Bad Guy" and p.alive for p in self.players)
        }
        
        # Add additional evaluation metrics similar to MultiAgentBench
        results["evaluation"] = {
            "task_score": self._calculate_task_score(),
            "coordination_score": self._calculate_coordination_score()
        }
        
        # Save to file
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
            
        logger.info(f"Saved final results: {filename}")
        
    def _calculate_task_score(self) -> float:
        """Calculate task score based on game outcomes.
        
        Returns:
            Task score (0-1 scale)
        """
        state = self.get_state()
        
        # Base the task score on points earned and game outcome
        if state["winner"] == "Good":
            # Good team win is worth 50% of total score
            win_score = 0.5
            
            # Calculate bonus based on surviving players
            good_team_count = sum(1 for p in self.players if p.role in ["Detective", "Doctor", "Citizen"])
            surviving_good = sum(1 for p in self.players if p.alive and p.role in ["Detective", "Doctor", "Citizen"])
            survival_rate = surviving_good / good_team_count if good_team_count > 0 else 0
            survival_score = survival_rate * 0.3
            
            # Calculate bonus for task completion
            max_possible_points = 10  # Example value, adjust based on game mechanics
            points_ratio = min(1.0, self.points["good_team"] / max_possible_points)
            points_score = points_ratio * 0.2
            
            return win_score + survival_score + points_score
        else:
            # Evil team won, calculate partial score for good team
            max_possible_points = 8  # Example value for partial game
            points_ratio = min(0.7, self.points["good_team"] / max_possible_points)
            return points_ratio
        
    def _calculate_coordination_score(self) -> float:
        """Calculate coordination score based on communication and planning.
        
        Returns:
            Coordination score (0-1 scale)
        """
        # This is a placeholder. In practice, this would involve analyzing discussions
        # and evaluating how well players coordinated. For now, we'll use a simple heuristic.
        
        # Calculate communication score based on discussion content
        if not self.discussion_log:
            return 0.0
            
        discussion_texts = "\n".join(self.discussion_log)
        
        # Count coordination indicators in discussion
        coordination_terms = [
            "I think", "agree", "suggest", "should we", "together",
            "strategy", "plan", "coordinate", "team", "protect"
        ]
        
        term_count = sum(1 for term in coordination_terms if term in discussion_texts.lower())
        communication_score = min(0.5, term_count / 10)
        
        # Calculate planning score based on successful protection and voting patterns
        planning_indicators = 0
        
        # Successful doctor protection
        if self.night_actions.get("doctor_target") and self.night_actions.get("doctor_target") == self.night_actions.get("mafia_target"):
            planning_indicators += 1
            
        # Successful detective investigations
        detective_player = next((p for p in self.players if p.role == "Detective"), None)
        if detective_player and detective_player.alive:
            planning_indicators += 1
            
        # Exile of evil player
        for event in self.events_log:
            if ("Mafia" in event or "Bad Guy" in event) and "was exiled" in event:
                planning_indicators += 1
                
        planning_score = min(0.5, planning_indicators / 3)
        
        return communication_score + planning_score
                