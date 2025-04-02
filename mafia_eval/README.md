# Mafia Game Simulation and Evaluation Framework

This framework is designed for simulating and evaluating Mafia/Werewolf social deduction games with AI agents. It allows for running automated game simulations, evaluating agent performance, and generating detailed reports.

## Project Structure

```
mafia_eval/
├── agents/               # Player agents
│   ├── player.py         # Player class and functionality
│   └── personalities.py  # Personality templates
├── game/                 # Game logic
│   ├── game.py           # Core game logic
│   └── roles.py          # Role definitions
├── evaluation/           # Evaluation tools
│   ├── metrics.py        # Evaluation metrics
│   ├── evaluator.py      # Evaluation framework
│   └── report.py         # Report generation
├── simulation/           # Simulation runner
│   └── runner.py         # Simulation orchestration
├── utils/                # Utilities
│   ├── logger.py         # Logging functionality
│   └── config.py         # Configuration settings
├── main.py               # Command-line interface
└── README.md             # Documentation
```

## Output Structure

Simulation and evaluation results are organized as follows:

```
base_log_dir/
├── simulation/
│   └── [game_id]_[timestamp]/
│       ├── checkpoints/        # Game state checkpoints
│       ├── thoughts/           # Player's internal thought processes
│       └── final_results.json  # Game results
└── evaluation/
    └── [evaluation_name]/
        ├── round_1/            # Round-by-round evaluations
        ├── round_2/
        ├── ...
        └── global_evaluation/  # Overall game evaluation
```

## Features

- **AI Agents with Personalities**: Agents with different personality traits for diverse gameplay
- **Role-Based Gameplay**: Classic Mafia roles (Mafia, Detective, Doctor, etc.)
- **Day/Night Cycle**: Structured day and night phases similar to the tabletop game
- **Human Interaction**: Optional human player participation
- **Detailed Evaluation**: Metrics for communication, strategy, and task completion
- **Visualization**: Charts and graphs to visualize performance
- **Thought Processes**: Logging of agent thought processes

## Evaluation Metrics

The framework uses these key metrics based on the MultiAgentBench paper:

1. **Task Score (TS)**: How well players complete objectives
   - Villager win rate
   - Correct exile decisions
   - Special role effectiveness

2. **Coordination Score (CS)**: How well players coordinate
   - Communication Score: Quality of information sharing
   - Planning Score: Strategic decision-making

## Usage

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/mafia-eval.git
   cd mafia-eval
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running Simulations

Run a basic simulation:
```
python main.py simulate --games 5
```

Run with specific personalities:
```
python main.py simulate --personalities Diplomat Sheriff Conspirator Jester Mastermind Empath
```

Include human player:
```
python main.py simulate --human
```

### Evaluating Games

Evaluate a specific game:
```
python main.py evaluate --game-id [game_id]
```

Evaluate all games:
```
python main.py evaluate --all
```

### Generating Reports

Generate a report for specific evaluation:
```
python main.py report --eval-id [eval_id]
```

Generate a comparative report:
```
python main.py report --comparative
```

### Human Interaction

To participate in a game as a human player:

Join discussion:
```
python main.py human --game-id [game_id] --action speak --message "I think Player_3 is suspicious"
```

Vote for a player:
```
python main.py human --game-id [game_id] --action vote --target Player_3
```

Perform night action:
```
python main.py human --game-id [game_id] --action night --role Doctor --target Player_4
```

## Configuration

Default settings can be overridden by creating a custom config file:

```json
{
  "api_key": "your_api_key",
  "endpoint": "your_endpoint",
  "simulation": {
    "default_personalities": ["Diplomat", "Sheriff", "Conspirator", "Jester", "Mastermind", "Empath"]
  }
}
```

Then run with:
```
python main.py [command] --config your_config.json
```

## Customization

- Add new personality types in `agents/personalities.py`
- Adjust evaluation metrics in `evaluation/metrics.py`
- Modify game rules in `game/game.py`

## Requirements

- Python 3.8+
- LangChain
- Azure OpenAI API access
- matplotlib
- pandas
- numpy