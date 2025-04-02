#!/usr/bin/env python3

import os
import argparse
import logging
import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional

from agents.personalities import PERSONALITIES
from simulation.runner import SimulationRunner
from evaluation.evaluator import MafiaEvaluator
from evaluation.report import ReportGenerator
from utils.logger import setup_logger
from utils.config import load_config

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Mafia Game Simulation and Evaluation")
    
    # Main command subparsers
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Simulation command
    sim_parser = subparsers.add_parser("simulate", help="Run game simulations")
    sim_parser.add_argument("--games", type=int, default=1, help="Number of games to simulate")
    sim_parser.add_argument("--personalities", nargs="+", help="List of personalities to use")
    sim_parser.add_argument("--human", action="store_true", help="Include a human player")
    sim_parser.add_argument("--config", type=str, help="Path to configuration file")
    sim_parser.add_argument("--output", type=str, help="Output directory for simulation results")
    
    # Evaluation command
    eval_parser = subparsers.add_parser("evaluate", help="Evaluate game simulations")
    eval_parser.add_argument("--game-id", type=str, help="ID of game to evaluate")
    eval_parser.add_argument("--all", action="store_true", help="Evaluate all games")
    eval_parser.add_argument("--config", type=str, help="Path to configuration file")
    eval_parser.add_argument("--output", type=str, help="Output directory for evaluation results")
    
    # Report command
    report_parser = subparsers.add_parser("report", help="Generate evaluation reports")
    report_parser.add_argument("--eval-id", type=str, help="ID of evaluation to report")
    report_parser.add_argument("--comparative", action="store_true", help="Generate comparative report")
    report_parser.add_argument("--config", type=str, help="Path to configuration file")
    report_parser.add_argument("--output", type=str, help="Output directory for reports")
    
    # Human game interaction command
    human_parser = subparsers.add_parser("human", help="Interact with a game as a human player")
    human_parser.add_argument("--game-id", type=str, required=True, help="ID of game to interact with")
    human_parser.add_argument("--action", choices=["speak", "vote", "night"], required=True, help="Type of action")
    human_parser.add_argument("--message", type=str, help="Message for discussion")
    human_parser.add_argument("--target", type=str, help="Target for vote or night action")
    human_parser.add_argument("--role", type=str, help="Role for night action")
    
    # Parse args
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config if hasattr(args, "config") and args.config else None)
    
    # Setup logging
    logger = setup_logger(config["logging"]["log_dir"])
    
    # Process command
    if args.command == "simulate":
        run_simulation(args, config, logger)
    elif args.command == "evaluate":
        run_evaluation(args, config, logger)
    elif args.command == "report":
        generate_reports(args, config, logger)
    elif args.command == "human":
        human_interaction(args, config, logger)
    else:
        parser.print_help()

def run_simulation(args, config: Dict[str, Any], logger: logging.Logger) -> None:
    """Run game simulations.
    
    Args:
        args: Command line arguments
        config: Configuration dictionary
        logger: Logger instance
    """
    logger.info("Starting game simulation")
    
    # Setup output directory
    output_dir = args.output if args.output else config["simulation"]["base_dir"]
    
    # Setup personalities
    if args.personalities:
        # Validate personalities
        for personality in args.personalities:
            if personality not in PERSONALITIES and personality != "Human":
                logger.error(f"Invalid personality: {personality}")
                return
        personalities = args.personalities
    else:
        personalities = config["simulation"]["default_personalities"]
    
    # Adjust for human player
    if args.human:
        logger.info("Including human player in simulation")
        if len(personalities) > 5:
            personalities = personalities[:5]  # Limit to 5 AI personalities if human player
    
    # Create simulation runner
    runner = SimulationRunner(base_dir=output_dir)
    
    # Run simulations
    game_ids = runner.run_simulation(
        personalities=personalities,
        has_human_player=args.human,
        num_games=args.games
    )
    
    logger.info(f"Completed {len(game_ids)} game simulations")
    
    # Display game IDs
    print("\nSimulated Games:")
    for game_id in game_ids:
        print(f"  - {game_id}")
    
    # Write game IDs to file for easy reference
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    id_file = os.path.join(output_dir, f"game_ids_{timestamp}.txt")
    with open(id_file, 'w') as f:
        f.write("\n".join(game_ids))
    
    print(f"\nGame IDs saved to {id_file}")

def run_evaluation(args, config: Dict[str, Any], logger: logging.Logger) -> None:
    """Run evaluation on game simulations.
    
    Args:
        args: Command line arguments
        config: Configuration dictionary
        logger: Logger instance
    """
    logger.info("Starting game evaluation")
    
    # Setup directories
    sim_dir = config["simulation"]["base_dir"]
    eval_dir = args.output if args.output else config["evaluation"]["base_dir"]
    
    # Create evaluator
    evaluator = MafiaEvaluator(base_dir=eval_dir, sim_dir=sim_dir)
    
    if args.game_id:
        # Evaluate specific game
        logger.info(f"Evaluating game: {args.game_id}")
        eval_results = evaluator.evaluate_game(args.game_id)
        
        # Display evaluation results summary
        print("\nEvaluation Results:")
        print(f"  Game ID: {args.game_id}")
        print(f"  Evaluation ID: {eval_results['evaluation_name']}")
        print(f"  Overall Score: {eval_results['global_evaluation']['overall_score']:.2f}")
        print(f"  Task Score: {eval_results['global_evaluation']['task_score']:.2f}")
        print(f"  Coordination Score: {eval_results['global_evaluation']['coordination_score']:.2f}")
        print(f"  Winner: {eval_results['global_evaluation']['winner']}")
        
    elif args.all:
        # Find all game directories
        game_dirs = []
        for entry in os.listdir(sim_dir):
            dir_path = os.path.join(sim_dir, entry)
            if os.path.isdir(dir_path) and os.path.exists(os.path.join(dir_path, "final_results.json")):
                game_id = entry.split('_')[0]  # Extract game ID from directory name
                game_dirs.append(game_id)
        
        # Evaluate all games
        logger.info(f"Evaluating {len(game_dirs)} games")
        eval_ids = []
        
        for game_id in game_dirs:
            try:
                eval_results = evaluator.evaluate_game(game_id)
                eval_ids.append(eval_results['evaluation_name'])
                
                print(f"Evaluated game {game_id} - Score: {eval_results['global_evaluation']['overall_score']:.2f}")
            except Exception as e:
                logger.error(f"Error evaluating game {game_id}: {str(e)}")
        
        # Generate aggregate report
        if eval_ids:
            aggregated = evaluator.aggregate_evaluations(eval_ids)
            
            print("\nAggregate Evaluation Results:")
            print(f"  Games evaluated: {aggregated['sample_size']}")
            print(f"  Average overall score: {aggregated['avg_overall_score']:.2f}")
            print(f"  Good team win rate: {aggregated['good_win_rate']:.2f}")
            print(f"  Evil team win rate: {aggregated['evil_win_rate']:.2f}")
    
    else:
        print("Please specify a game ID with --game-id or use --all to evaluate all games")

def generate_reports(args, config: Dict[str, Any], logger: logging.Logger) -> None:
    """Generate evaluation reports.
    
    Args:
        args: Command line arguments
        config: Configuration dictionary
        logger: Logger instance
    """
    logger.info("Starting report generation")
    
    # Setup directories
    eval_dir = config["evaluation"]["base_dir"]
    report_dir = args.output if args.output else config["reporting"]["base_dir"]
    
    # Create report generator
    report_gen = ReportGenerator(base_dir=report_dir)
    
    if args.eval_id:
        # Find evaluation results file
        eval_file = os.path.join(eval_dir, args.eval_id, "evaluation_results.json")
        
        if os.path.exists(eval_file):
            logger.info(f"Generating report for evaluation: {args.eval_id}")
            
            # Load evaluation data
            with open(eval_file, 'r') as f:
                eval_data = json.load(f)
            
            # Generate report
            report_path = report_gen.generate_game_report(eval_data)
            
            print(f"\nReport generated at: {report_path}")
        else:
            print(f"Evaluation results not found for {args.eval_id}")
    
    elif args.comparative:
        # Find all evaluation directories
        eval_dirs = []
        for entry in os.listdir(eval_dir):
            dir_path = os.path.join(eval_dir, entry)
            if os.path.isdir(dir_path) and os.path.exists(os.path.join(dir_path, "evaluation_results.json")):
                eval_dirs.append(entry)
        
        if eval_dirs:
            logger.info(f"Generating comparative report for {len(eval_dirs)} evaluations")
            
            # Load all evaluation data
            evals = []
            for eval_id in eval_dirs:
                eval_file = os.path.join(eval_dir, eval_id, "evaluation_results.json")
                with open(eval_file, 'r') as f:
                    evals.append(json.load(f))
            
            # Create aggregated data
            aggregated = {}
            
            # TODO: Implement more comprehensive aggregation
            # For now, just use a placeholder
            aggregated["sample_size"] = len(evals)
            
            # Generate report
            report_path = report_gen.generate_comparative_report(aggregated)
            
            print(f"\nComparative report generated at: {report_path}")
        else:
            print("No evaluations found")
    
    else:
        print("Please specify an evaluation ID with --eval-id or use --comparative to generate a comparative report")

def human_interaction(args, config: Dict[str, Any], logger: logging.Logger) -> None:
    """Process human interaction with a game.
    
    Args:
        args: Command line arguments
        config: Configuration dictionary
        logger: Logger instance
    """
    logger.info(f"Processing human interaction for game {args.game_id}")
    
    # Find game directory
    sim_dir = config["simulation"]["base_dir"]
    game_dirs = [d for d in os.listdir(sim_dir) if args.game_id in d]
    
    if not game_dirs:
        print(f"Game {args.game_id} not found")
        return
    
    game_dir = os.path.join(sim_dir, game_dirs[0])
    checkpoints_dir = os.path.join(game_dir, "checkpoints")
    
    # Find latest checkpoint
    checkpoint_files = sorted([f for f in os.listdir(checkpoints_dir) if f.endswith('.json')])
    if not checkpoint_files:
        print("No checkpoints found for this game")
        return
    
    latest_checkpoint = checkpoint_files[-1]
    checkpoint_path = os.path.join(checkpoints_dir, latest_checkpoint)
    
    with open(checkpoint_path, 'r') as f:
        checkpoint = json.load(f)
    
    game_phase = checkpoint["phase"]
    
    # Process action based on type
    if args.action == "speak":
        if not args.message:
            print("Please provide a message with --message")
            return
        
        if game_phase != "discussion":
            print(f"Cannot speak during {game_phase} phase")
            return
        
        # Add message to discussion log
        discussion_log = checkpoint.get("discussion_log", "").split("\n")
        
        # Remove waiting marker if present
        if "WAITING_FOR_HUMAN_INPUT" in discussion_log:
            discussion_log.remove("WAITING_FOR_HUMAN_INPUT")
        
        # Add human message
        discussion_log.append(f"Player_1: {args.message}")
        
        # Update checkpoint
        checkpoint["discussion_log"] = "\n".join(discussion_log)
        
        # Save updated checkpoint
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_checkpoint = f"human_discussion_{timestamp}.json"
        new_path = os.path.join(checkpoints_dir, new_checkpoint)
        
        with open(new_path, 'w') as f:
            json.dump(checkpoint, f, indent=2)
        
        print(f"Message added to discussion: '{args.message}'")
        
    elif args.action == "vote":
        if not args.target:
            print("Please provide a target with --target")
            return
        
        if game_phase != "voting" and game_phase != "discussion":
            print(f"Cannot vote during {game_phase} phase")
            return
        
        # Update checkpoint with vote
        if "human_vote" not in checkpoint:
            checkpoint["human_vote"] = {}
        
        checkpoint["human_vote"]["Player_1"] = args.target
        
        # Save updated checkpoint
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_checkpoint = f"human_vote_{timestamp}.json"
        new_path = os.path.join(checkpoints_dir, new_checkpoint)
        
        with open(new_path, 'w') as f:
            json.dump(checkpoint, f, indent=2)
        
        print(f"Vote registered for target: '{args.target}'")
        
    elif args.action == "night":
        if not args.target or not args.role:
            print("Please provide a target with --target and role with --role")
            return
        
        if game_phase != "night":
            print(f"Cannot perform night action during {game_phase} phase")
            return
        
        # Validate role
        valid_roles = ["Mafia", "Detective", "Doctor"]
        if args.role not in valid_roles:
            print(f"Invalid role: {args.role}. Must be one of {valid_roles}")
            return
        
        # Update night actions
        if "night_actions" not in checkpoint:
            checkpoint["night_actions"] = {}
        
        if args.role == "Mafia":
            checkpoint["night_actions"]["mafia_target"] = args.target
        elif args.role == "Detective":
            checkpoint["night_actions"]["detective_target"] = args.target
        elif args.role == "Doctor":
            checkpoint["night_actions"]["doctor_target"] = args.target
        
        # Save updated checkpoint
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_checkpoint = f"human_night_{timestamp}.json"
        new_path = os.path.join(checkpoints_dir, new_checkpoint)
        
        with open(new_path, 'w') as f:
            json.dump(checkpoint, f, indent=2)
        
        print(f"Night action registered: {args.role} targeting {args.target}")
    
    else:
        print(f"Unknown action: {args.action}")

if __name__ == "__main__":
    main()