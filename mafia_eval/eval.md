# Mafia Game Evaluation Metrics

## Task Score (TS)
* **Definition**: Measures how well players complete game objectives
* **Calculation**: `(0.5 * win_outcome) + (0.3 * survival_rate) + (0.2 * points_ratio)`
* **Components**:
  - **Win outcome**: 0.5 if good team wins, partial score based on points if they lose
  - **Survival rate**: Percentage of good team members surviving
  - **Points ratio**: Points earned divided by maximum possible points
  - **Key role bonuses**: +0.1 for Detective survival, +0.1 for Doctor survival

## Coordination Score (CS)
* **Definition**: Measures communication and planning effectiveness
* **Calculation**: `(0.5 * communication_score) + (0.5 * planning_score)`
* **Components**:
  - **Communication score**: LLM-evaluated (1-5 scale, normalized to 0-1)
  - **Planning score**: LLM-evaluated (1-5 scale, normalized to 0-1)

## Communication Evaluation
* **Method**: LLM analysis of discussion logs
* **Criteria**:
  - Information sharing quality
  - Team alignment
  - Strategic discussion
  - Decision-making progress
  - Deception detection

## Planning Evaluation
* **Method**: LLM analysis of night actions and voting patterns
* **Criteria**:
  - Role effectiveness
  - Target selection strategy
  - Team coordination
  - Adaptability
  - Strategic outcomes

## Additional Metrics
* **Win rate**: Percentage of games won by each team
* **Role survival rates**: Survival rates for key roles (Detective, Doctor)
* **Exile accuracy**: Rate of correctly exiling evil players
* **Deception success**: Rate at which innocent players are exiled

## Point System
* **Good team points**:
  - Detective identifies Mafia: +1
  - Doctor protects target: +2
  - Exile of evil player: +2
  - Win bonus: +5
* **Evil team points**:
  - Killing Detective: +3
  - Killing Doctor: +2
  - Killing Citizen: +1
  - Getting innocent exiled: +1
  - Win bonus: +5

## Overall Score
Calculated as `(Task Score + Coordination Score) / 2`