import os
import json
import logging
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict, Any, Optional
from datetime import datetime
import numpy as np

logger = logging.getLogger(__name__)

class ReportGenerator:
    """Generates evaluation reports for Mafia/Werewolf simulations."""
    
    def __init__(self, base_dir: str = "./reports"):
        """Initialize the report generator.
        
        Args:
            base_dir: Base directory for report outputs
        """
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)
    
    def generate_game_report(self, evaluation_data: Dict[str, Any], 
                           report_name: Optional[str] = None) -> str:
        """Generate a report for a single game evaluation.
        
        Args:
            evaluation_data: Evaluation data
            report_name: Custom name for the report
            
        Returns:
            Path to the generated report
        """
        if report_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_name = f"game_report_{evaluation_data.get('game_id', 'unknown')}_{timestamp}"
        
        report_dir = os.path.join(self.base_dir, report_name)
        os.makedirs(report_dir, exist_ok=True)
        
        # Extract data
        game_id = evaluation_data.get("game_id", "unknown")
        round_evals = evaluation_data.get("round_evaluations", {})
        global_eval = evaluation_data.get("global_evaluation", {})
        
        # Create report HTML
        html_content = self._create_game_html_report(game_id, round_evals, global_eval)
        html_path = os.path.join(report_dir, "report.html")
        
        with open(html_path, 'w') as f:
            f.write(html_content)
        
        # Create visualization figures
        aggregated_data = {
            "sample_size": len(round_evals),
            "good_win_rate": global_eval.get("good_team_points", 0) / max(global_eval.get("rounds_played", 1), 1),
            "evil_win_rate": global_eval.get("evil_team_points", 0) / max(global_eval.get("rounds_played", 1), 1),
            # Add other aggregated metrics as needed
        }
        self._create_metric_comparison_chart(aggregated_data, report_dir)
        self._create_win_rate_chart(aggregated_data, report_dir, round_evals, global_eval)
        
        logger.info(f"Generated comparative report at {html_path}")
        return html_path
    
    def _create_game_html_report(self, game_id: str, 
                               round_evals: Dict[int, Dict[str, Any]],
                               global_eval: Dict[str, Any]) -> str:
        """Create HTML content for a game report.
        
        Args:
            game_id: Game ID
            round_evals: Round evaluation data
            global_eval: Global evaluation data
            
        Returns:
            HTML report content
        """
        # Convert round evaluations to a more accessible format
        rounds_data = []
        for round_num, data in round_evals.items():
            rounds_data.append({
                "round": round_num,
                "communication_score": data.get("communication_score", 0),
                "planning_score": data.get("planning_score", 0),
                "coordination_score": data.get("coordination_score", 0),
                "communication_feedback": data.get("communication_feedback", ""),
                "planning_feedback": data.get("planning_feedback", "")
            })
        
        # Sort rounds by round number
        rounds_data.sort(key=lambda x: x["round"])
        
        # Create HTML content
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Mafia Game Evaluation Report - {game_id}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1, h2, h3 {{ color: #333366; }}
                .metric {{ margin-bottom: 10px; }}
                .metric-name {{ font-weight: bold; }}
                .metric-value {{ float: right; }}
                .score-high {{ color: green; }}
                .score-medium {{ color: orange; }}
                .score-low {{ color: red; }}
                .card {{ border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin-bottom: 20px; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .chart-container {{ display: flex; justify-content: center; margin: 20px 0; }}
                .chart {{ width: 100%; max-width: 800px; }}
            </style>
        </head>
        <body>
            <h1>Mafia Game Evaluation Report</h1>
            <p><strong>Game ID:</strong> {game_id}</p>
            <p><strong>Report Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            
            <div class="card">
                <h2>Global Evaluation</h2>
                <div class="metric">
                    <span class="metric-name">Overall Score:</span>
                    <span class="metric-value {self._get_score_class(global_eval.get('overall_score', 0))}">{global_eval.get('overall_score', 0):.2f}</span>
                </div>
                <div class="metric">
                    <span class="metric-name">Task Score:</span>
                    <span class="metric-value {self._get_score_class(global_eval.get('task_score', 0))}">{global_eval.get('task_score', 0):.2f}</span>
                </div>
                <div class="metric">
                    <span class="metric-name">Coordination Score:</span>
                    <span class="metric-value {self._get_score_class(global_eval.get('coordination_score', 0))}">{global_eval.get('coordination_score', 0):.2f}</span>
                </div>
                <div class="metric">
                    <span class="metric-name">Winner:</span>
                    <span class="metric-value">{global_eval.get('winner', 'Unknown')}</span>
                </div>
                <div class="metric">
                    <span class="metric-name">Rounds Played:</span>
                    <span class="metric-value">{global_eval.get('rounds_played', 0)}</span>
                </div>
                <div class="metric">
                    <span class="metric-name">Good Team Points:</span>
                    <span class="metric-value">{global_eval.get('good_team_points', 0)}</span>
                </div>
                <div class="metric">
                    <span class="metric-name">Evil Team Points:</span>
                    <span class="metric-value">{global_eval.get('evil_team_points', 0)}</span>
                </div>
                <div class="metric">
                    <span class="metric-name">Good Team Survival Rate:</span>
                    <span class="metric-value">{global_eval.get('good_team_survival_rate', 0):.2f}</span>
                </div>
            </div>
            
            <div class="chart-container">
                <img class="chart" src="score_radar_chart.png" alt="Score Radar Chart">
            </div>
            
            <div class="card">
                <h2>Round-by-Round Evaluation</h2>
                <div class="chart-container">
                    <img class="chart" src="round_metrics_chart.png" alt="Round Metrics Chart">
                </div>
                
                <table>
                    <tr>
                        <th>Round</th>
                        <th>Communication Score</th>
                        <th>Planning Score</th>
                        <th>Coordination Score</th>
                    </tr>
        """
        
        # Add rows for each round
        for round_data in rounds_data:
            html += f"""
                    <tr>
                        <td>{round_data['round']}</td>
                        <td class="{self._get_score_class(round_data['communication_score'])}">{round_data['communication_score']:.2f}</td>
                        <td class="{self._get_score_class(round_data['planning_score'])}">{round_data['planning_score']:.2f}</td>
                        <td class="{self._get_score_class(round_data['coordination_score'])}">{round_data['coordination_score']:.2f}</td>
                    </tr>
            """
        
        html += """
                </table>
            </div>
            
            <div class="card">
                <h2>Evaluation Feedback</h2>
        """
        
        # Add feedback for each round
        for round_data in rounds_data:
            html += f"""
                <h3>Round {round_data['round']}</h3>
                <h4>Communication</h4>
                <p>{round_data['communication_feedback']}</p>
                <h4>Planning</h4>
                <p>{round_data['planning_feedback']}</p>
            """
        
        html += """
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _create_comparative_html_report(self, aggregated_data: Dict[str, Any]) -> str:
        """Create HTML content for a comparative report.
        
        Args:
            aggregated_data: Aggregated evaluation data
            
        Returns:
            HTML report content
        """
        # Extract key metrics
        sample_size = aggregated_data.get("sample_size", 0)
        good_win_rate = aggregated_data.get("good_win_rate", 0)
        evil_win_rate = aggregated_data.get("evil_win_rate", 0)
        
        # Create metric summaries
        metrics = []
        for key, value in aggregated_data.items():
            if key.startswith("avg_"):
                metric_name = key[4:]  # Remove "avg_" prefix
                min_value = aggregated_data.get(f"min_{metric_name}", 0)
                max_value = aggregated_data.get(f"max_{metric_name}", 0)
                
                metrics.append({
                    "name": metric_name.replace("_", " ").title(),
                    "avg": value,
                    "min": min_value,
                    "max": max_value
                })
        
        # Sort metrics by name
        metrics.sort(key=lambda x: x["name"])
        
        # Create HTML content
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Mafia Game Comparative Evaluation Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1, h2, h3 {{ color: #333366; }}
                .metric {{ margin-bottom: 10px; }}
                .metric-name {{ font-weight: bold; }}
                .metric-value {{ float: right; }}
                .score-high {{ color: green; }}
                .score-medium {{ color: orange; }}
                .score-low {{ color: red; }}
                .card {{ border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin-bottom: 20px; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .chart-container {{ display: flex; justify-content: center; margin: 20px 0; }}
                .chart {{ width: 100%; max-width: 800px; }}
            </style>
        </head>
        <body>
            <h1>Mafia Game Comparative Evaluation Report</h1>
            <p><strong>Report Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p><strong>Sample Size:</strong> {sample_size} games</p>
            
            <div class="card">
                <h2>Win Rates</h2>
                <div class="metric">
                    <span class="metric-name">Good Team Win Rate:</span>
                    <span class="metric-value">{good_win_rate:.2f}</span>
                </div>
                <div class="metric">
                    <span class="metric-name">Evil Team Win Rate:</span>
                    <span class="metric-value">{evil_win_rate:.2f}</span>
                </div>
                
                <div class="chart-container">
                    <img class="chart" src="win_rate_chart.png" alt="Win Rate Chart">
                </div>
            </div>
            
            <div class="card">
                <h2>Performance Metrics</h2>
                <div class="chart-container">
                    <img class="chart" src="metric_comparison_chart.png" alt="Metric Comparison Chart">
                </div>
                
                <table>
                    <tr>
                        <th>Metric</th>
                        <th>Average</th>
                        <th>Minimum</th>
                        <th>Maximum</th>
                    </tr>
        """
        
        # Add rows for each metric
        for metric in metrics:
            html += f"""
                    <tr>
                        <td>{metric['name']}</td>
                        <td class="{self._get_score_class(metric['avg'])}">{metric['avg']:.2f}</td>
                        <td>{metric['min']:.2f}</td>
                        <td>{metric['max']:.2f}</td>
                    </tr>
            """
        
        html += """
                </table>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _get_score_class(self, score: float) -> str:
        """Get CSS class for a score value.
        
        Args:
            score: Score value
            
        Returns:
            CSS class name
        """
        if score >= 0.7:
            return "score-high"
        elif score >= 0.4:
            return "score-medium"
        else:
            return "score-low"
    
    def _create_round_metrics_chart(self, round_evals: Dict[int, Dict[str, Any]], 
                                  save_dir: str) -> None:
        """Create a chart showing metrics across rounds.
        
        Args:
            round_evals: Round evaluation data
            save_dir: Directory to save the chart
        """
        # Convert round evaluations to a more accessible format
        rounds = []
        comm_scores = []
        plan_scores = []
        coord_scores = []
        
        for round_num, data in sorted(round_evals.items()):
            rounds.append(round_num)
            comm_scores.append(data.get("communication_score", 0))
            plan_scores.append(data.get("planning_score", 0))
            coord_scores.append(data.get("coordination_score", 0))
        
        # Create figure
        plt.figure(figsize=(10, 6))
        plt.plot(rounds, comm_scores, 'o-', label='Communication Score')
        plt.plot(rounds, plan_scores, 's-', label='Planning Score')
        plt.plot(rounds, coord_scores, '^-', label='Coordination Score')
        
        plt.title('Round-by-Round Metrics')
        plt.xlabel('Round')
        plt.ylabel('Score')
        plt.ylim(0, 1)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(rounds)
        plt.legend()
        
        # Save figure
        plt.savefig(os.path.join(save_dir, 'round_metrics_chart.png'), bbox_inches='tight')
        plt.close()
    
    def _create_score_radar_chart(self, global_eval: Dict[str, Any], save_dir: str) -> None:
        """Create a radar chart of global evaluation scores.
        
        Args:
            global_eval: Global evaluation data
            save_dir: Directory to save the chart
        """
        # Extract metrics
        metrics = [
            'task_score', 
            'coordination_score', 
            'communication_score', 
            'planning_score'
        ]
        
        values = [global_eval.get(m, 0) for m in metrics]
        
        # Convert metric names for display
        display_names = [m.replace('_', ' ').title() for m in metrics]
        
        # Create a radar chart
        angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False).tolist()
        
        # Close the polygon
        values.append(values[0])
        display_names.append(display_names[0])
        angles.append(angles[0])
        
        # Create figure
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        
        # Plot data
        ax.plot(angles, values, 'o-', linewidth=2)
        ax.fill(angles, values, alpha=0.25)
        
        # Set labels
        ax.set_thetagrids(np.degrees(angles), display_names)
        
        # Set y-axis limits
        ax.set_ylim(0, 1)
        ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'])
        ax.grid(True)
        
        plt.title('Game Performance Metrics', size=15)
        
        # Save figure
        plt.savefig(os.path.join(save_dir, 'score_radar_chart.png'), bbox_inches='tight')
        plt.close()
    
    def _create_metric_comparison_chart(self, aggregated_data: Dict[str, Any], 
                                      save_dir: str) -> None:
        """Create a chart comparing key metrics.
        
        Args:
            aggregated_data: Aggregated evaluation data
            save_dir: Directory to save the chart
        """
        # Extract key metrics
        metrics = ['task_score', 'coordination_score', 'communication_score', 'planning_score', 'overall_score']
        
        # Get average, min, max for each metric
        avgs = [aggregated_data.get(f"avg_{m}", 0) for m in metrics]
        mins = [aggregated_data.get(f"min_{m}", 0) for m in metrics]
        maxs = [aggregated_data.get(f"max_{m}", 0) for m in metrics]
        
        # Convert metric names for display
        display_names = [m.replace('_', ' ').title() for m in metrics]
        
        # Create figure
        plt.figure(figsize=(12, 6))
        
        x = range(len(metrics))
        width = 0.25
        
        plt.bar([i - width for i in x], mins, width, label='Minimum', color='#ff9999')
        plt.bar(x, avgs, width, label='Average', color='#66b3ff')
        plt.bar([i + width for i in x], maxs, width, label='Maximum', color='#99ff99')
        
        plt.ylabel('Score')
        plt.title('Performance Metrics Comparison')
        plt.xticks(x, display_names, rotation=45, ha='right')
        plt.ylim(0, 1)
        plt.legend()
        plt.tight_layout()
        
        # Save figure
        plt.savefig(os.path.join(save_dir, 'metric_comparison_chart.png'), bbox_inches='tight')
        plt.close()
    
    def _create_win_rate_chart(self, aggregated_data: Dict[str, Any], save_dir: str) -> None:
        """Create a chart showing win rates.
        
        Args:
            aggregated_data: Aggregated evaluation data
            save_dir: Directory to save the chart
        """
        # Extract win rates
        good_win_rate = aggregated_data.get("good_win_rate", 0)
        evil_win_rate = aggregated_data.get("evil_win_rate", 0)
        
        # Check for zero values to avoid division errors
        if good_win_rate == 0 and evil_win_rate == 0:
            # Create empty chart with message
            plt.figure(figsize=(8, 6))
            plt.text(0.5, 0.5, "No win rate data available", 
                    horizontalalignment='center', verticalalignment='center',
                    transform=plt.gca().transAxes, fontsize=14)
            plt.axis('off')
        else:
            # Create figure
            plt.figure(figsize=(8, 6))
            
            labels = ['Good Team', 'Evil Team']
            sizes = [good_win_rate, evil_win_rate]
            colors = ['#66b3ff', '#ff9999']
            explode = (0.1, 0) if good_win_rate > 0 else (0, 0.1)
            
            plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                    autopct='%1.1f%%', shadow=True, startangle=90)
            plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular
            plt.title('Win Rate Distribution')
        
        # Save figure
        plt.savefig(os.path.join(save_dir, 'win_rate_chart.png'), bbox_inches='tight')
        plt.close()
    
    def generate_comparative_report(self, aggregated_data: Dict[str, Any], report_name: Optional[str] = None) -> str:
        """Generate a comparative report across multiple evaluations."""
        if report_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_name = f"comparative_report_{timestamp}"
        
        report_dir = os.path.join(self.base_dir, report_name)
        os.makedirs(report_dir, exist_ok=True)
        
        # Create report HTML
        html_content = self._create_comparative_html_report(aggregated_data)
        html_path = os.path.join(report_dir, "report.html")
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        # Create visualization figures
        self._create_metric_comparison_chart(aggregated_data, report_dir)
        self._create_win_rate_chart(aggregated_data, report_dir)
        
        logger.info(f"Generated comparative report at {html_path}")
        return html_path