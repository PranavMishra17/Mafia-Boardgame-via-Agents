from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import json
import logging
import random
import time
import uuid
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import threading
from flask import copy_current_request_context

import sys

# Setup logging with proper encoding
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mafia_game.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mafia_game.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
#api_key = os.getenv("AZURE_OPENAI_API_KEY")
#endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

api_key = "428KgVArXb6sFyseVYDjElDDYZnlCnx8pNa8CfU5dCic6gjOK89WJQQJ99BBACYeBjFXJ3w3AAABACOG5gtQ"
endpoint = "https://vare-labs-azure-openai-resource.openai.azure.com/"

app = Flask(__name__, static_folder="./static", template_folder="./templates")
CORS(app)

# Personality templates
PERSONALITIES = {
    "Diplomat": {
        "description": "Calm, rational, and diplomatic. Tries to mediate between players and find logical solutions.",
        "attributes": {
            "truthfulness": 0.9,
            "aggressiveness": 0.2,
            "suspicion": 0.5,
            "persuasiveness": 0.8,
            "loyalty": 0.8
        },
        "prompt_style": "You are diplomatic and calm. You seek to understand all sides and mediate conflict. You speak in a composed, thoughtful manner and avoid making accusations without evidence."
    },
    "Sheriff": {
        "description": "Direct, authoritative, and justice-focused. Takes charge of investigations.",
        "attributes": {
            "truthfulness": 0.8,
            "aggressiveness": 0.7,
            "suspicion": 0.8,
            "persuasiveness": 0.6,
            "loyalty": 0.9
        },
        "prompt_style": "You are authoritative and direct. You take charge in conversations and aren't afraid to make accusations. You speak with conviction and often use imperatives."
    },
    "Conspirator": {
        "description": "Paranoid, sees connections everywhere, and questions everything.",
        "attributes": {
            "truthfulness": 0.4,
            "aggressiveness": 0.5,
            "suspicion": 1.0,
            "persuasiveness": 0.6,
            "loyalty": 0.3
        },
        "prompt_style": "You see conspiracies everywhere. You're highly suspicious and question everyone's motives, even your allies. You speak in a nervous, questioning manner with many rhetorical questions."
    },
    "Jester": {
        "description": "Humorous, light-hearted, but observant. Uses humor to deflect and observe.",
        "attributes": {
            "truthfulness": 0.7,
            "aggressiveness": 0.3,
            "suspicion": 0.6,
            "persuasiveness": 0.5,
            "loyalty": 0.6
        },
        "prompt_style": "You use humor in all situations. You deflect tension with jokes but observe carefully. You speak casually with puns and jokes while making your points."
    },
    "Mastermind": {
        "description": "Strategic, calculating, and manipulative. Thinks several steps ahead.",
        "attributes": {
            "truthfulness": 0.3,
            "aggressiveness": 0.4,
            "suspicion": 0.7,
            "persuasiveness": 0.9,
            "loyalty": 0.2
        },
        "prompt_style": "You are calculating and strategic. You plan several moves ahead and manipulate others subtly. You speak confidently but reveal only what serves your purpose."
    },
    "Empath": {
        "description": "Emotionally intelligent, reads people well, and connects with others.",
        "attributes": {
            "truthfulness": 0.9,
            "aggressiveness": 0.1,
            "suspicion": 0.6,
            "persuasiveness": 0.7,
            "loyalty": 0.8
        },
        "prompt_style": "You read emotions extremely well. You connect with others on an emotional level and speak gently. You often reference how others seem to be feeling."
    },
    "Wildcard": {
        "description": "Unpredictable, chaotic, and difficult to read. Changes strategies frequently.",
        "attributes": {
            "truthfulness": 0.5,
            "aggressiveness": 0.6,
            "suspicion": 0.5,
            "persuasiveness": 0.5,
            "loyalty": 0.4
        },
        "prompt_style": "You are unpredictable and chaotic. You change your mind frequently and seem to follow no consistent pattern. Your speech patterns vary wildly from calm to excited."
    },
    "Veteran": {
        "description": "Experienced, knowledgeable about game mechanics, and strategic.",
        "attributes": {
            "truthfulness": 0.7,
            "aggressiveness": 0.6,
            "suspicion": 0.8,
            "persuasiveness": 0.7,
            "loyalty": 0.7
        },
        "prompt_style": "You're extremely knowledgeable about how this game works. You analyze patterns methodically and speak with authority about game strategy."
    },
    "Innocent": {
        "description": "Naive, trusting, and honest. Easy to read but also easy to mislead.",
        "attributes": {
            "truthfulness": 1.0,
            "aggressiveness": 0.1,
            "suspicion": 0.2,
            "persuasiveness": 0.4,
            "loyalty": 0.9
        },
        "prompt_style": "You are naive and trusting. You believe what others tell you and rarely suspect deception. You speak honestly and directly, sharing your thoughts openly."
    },
    "Manipulator": {
        "description": "Charming, deceptive, and influential. Skilled at swaying others' opinions.",
        "attributes": {
            "truthfulness": 0.2,
            "aggressiveness": 0.3,
            "suspicion": 0.7,
            "persuasiveness": 1.0,
            "loyalty": 0.1
        },
        "prompt_style": "You are charming and manipulative. You subtly influence others while appearing helpful. You speak in a friendly, engaging manner while carefully guiding conversations."
    }
}

# Game state storage
games = {}

class Player:
    def __init__(self, name, personality, role=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.personality = personality
        self.role = role
        self.alive = True
        self.memory = ConversationBufferMemory()
        self.llm = AzureChatOpenAI(
            azure_deployment="VARELab-GPT4o",
            api_key=api_key,
            api_version="2025-01-01-preview",
            azure_endpoint=endpoint,
            temperature=0.7,
            max_tokens=500,
            timeout=None,
            max_retries=2,
        )
        
    # Add this to the Player.get_base_prompt method in app.py:

    def get_base_prompt(self):
        # Check if personality exists in the predefined list
        if self.personality in PERSONALITIES:
            personality_info = PERSONALITIES[self.personality]
            prompt_style = personality_info['prompt_style']
        else:
            # Handle custom personalities
            prompt_style = f"You have a unique personality as {self.personality}."
            
        base_prompt = f"""
    You are playing a fun board game of Mafia with friends. Your name is {self.name} and you have the personality of a {self.personality}.
    {prompt_style}

    Your current role is {self.role}. 

    Remember:
    - This is a social game about deception and deduction - nobody is actually dying or being exiled
    - You can directly question other players about their night, role, or actions
    - You can lie about your identity if it serves your strategy
    - You can blame other players for actions or accuse them based on their behavior
    - You can pretend to be a different role (like claiming to be Detective when you're not)
    - Express emotions naturally - frustration, excitement, begging others to believe you, etc.
    - Use your intuition and try to convince others to trust you
    - Keep your responses conversational and brief (2-4 lines)
    """
        
        if self.role == "Mafia":
            base_prompt += """
    You're on the evil team! Your goal is to eliminate the good players without revealing your true identity.
    - You know who the Bad Guy is and should work together with them
    - Consider lying about your role (pretending to be Detective, Doctor, or Citizen)
    - Be strategic about who you accuse - don't be too obvious about protecting your evil teammate
    - You might want to falsely claim you're Detective and "cleared" your evil teammate
    - Don't reveal your true role unless absolutely necessary or strategically advantageous
    """
        elif self.role == "Bad Guy":
            base_prompt += """
    You're on the evil team! Your goal is to eliminate the good players without revealing your true identity.
    - You know who the Mafia is and should work together with them
    - Consider lying about your role (pretending to be Detective, Doctor, or Citizen)
    - Be strategic about who you accuse - don't be too obvious about protecting your evil teammate
    - You might want to claim innocence or even pretend to suspect your evil teammate (to throw off suspicion)
    - Don't reveal your true role unless absolutely necessary or strategically advantageous
    """
        elif self.role == "Detective":
            base_prompt += """
    You're on the good team! Your goal is to identify and vote out the Mafia and Bad Guy.
    - You can investigate one player each night to determine if they're Mafia
    - You can choose whether to reveal your role or keep it secret for safety
    - You might want to share your investigation results, but be careful - revealing yourself makes you a target
    - Watch how players respond to accusations - guilty players often overreact or deflect
    - Trust your intuition and try to convince others to follow your lead
    """
        elif self.role == "Doctor":
            base_prompt += """
    You're on the good team! Your goal is to identify and vote out the Mafia and Bad Guy.
    - You can protect one player each night from being killed
    - You can choose whether to reveal your role or keep it secret for safety
    - Be careful about revealing who you protected - it gives information to the Mafia
    - Watch player behavior closely - evil players might slip up in their lies
    - Be careful who you trust with your true identity
    """
        else:  # Citizen
            base_prompt += """
    You're on the good team! Your goal is to identify and vote out the Mafia and Bad Guy.
    - You have no special night ability, but your vote is crucial
    - Listen carefully to everyone's claims and look for inconsistencies
    - Anyone could be lying about their role - trust your instincts
    - Don't be afraid to challenge suspicious behavior or statements
    - You can pretend to be a special role if it helps your strategy, but it's risky
    """
            
        return base_prompt

    def generate_response(self, context, game_state):
        role_info = f"Your role is {self.role}."
        if not self.alive:
            return "I'm dead and can't participate in the discussion."
            
        if self.role in ["Mafia", "Bad Guy"]:
            # Add information about their evil partner
            evil_partner = ""
            for player in game_state["players"]:
                if player.name != self.name and player.role in ["Mafia", "Bad Guy"]:
                    evil_partner = player.name
            role_info += f" You know that {evil_partner} is your evil partner."
        
        system_prompt = f"""{self.get_base_prompt()}

        Current game state:
        - It is currently {game_state['phase']}
        - You are {self.role}
        - {role_info}
        - Living players: {', '.join([p.name for p in game_state['players'] if p.alive])}
        - Dead players: {', '.join([p.name for p in game_state['players'] if not p.alive])}

        Previous game events:
        {game_state['events_log']}

        Remember this is a social deduction game:
        - You can directly ask other players questions
        - You can lie about your role or actions if it helps your team
        - You can make emotional appeals or express frustration/anger
        - You can claim to have information you don't actually have
        - You can beg others to trust you or claim strong intuition

        Your goal is to survive and help your team win. If you're good (Detective, Doctor, Citizen), you want to identify and vote out the Mafia and Bad Guy. If you're evil (Mafia, Bad Guy), you want to eliminate good players without being discovered.

        Respond in 2-4 lines maximum, as if you're speaking to the other players.
        """
        
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=context)
            ]
            response = self.llm.invoke(messages).content
            # Log the conversation
            logger.info(f"Player {self.name} ({self.role}) - Context: {context}")
            logger.info(f"Player {self.name} ({self.role}) - Response: {response}")
            return response
        except Exception as e:
            logger.error(f"Error generating response for {self.name}: {str(e)}")
            return "I need a moment to gather my thoughts..."

    def make_night_decision(self, game_state):
        living_players = [p for p in game_state["players"] if p.alive and p.name != self.name]
        if not living_players:
            return None
            
        player_names = [p.name for p in living_players]
        
        # Update night decision prompts in make_night_decision method
        if self.role == "Mafia":
            prompt = f"""
        {self.get_base_prompt()}

        It's night time - time for the Mafia to strike! Choose someone to eliminate.

        Current living players: {', '.join(player_names)}

        Think strategically about who to target:
        - Is there someone who seems suspicious of you?
        - Is the Detective or Doctor a threat to your plans?
        - Which player's elimination would cause the most confusion?

        Based on the game so far, who would you like to eliminate? Respond with ONLY the name of one player from the list above.
        """
        elif self.role == "Detective":
            prompt = f"""
        {self.get_base_prompt()}

        It's night time - time to investigate! Choose a player to determine if they're the Mafia.

        Current living players: {', '.join(player_names)}

        Think about who to investigate:
        - Who acted suspiciously during discussions?
        - Who made accusations that seemed unfounded?
        - Who has been too quiet or too loud?

        Based on the game so far, who would you like to investigate? Respond with ONLY the name of one player from the list above.
        """
        elif self.role == "Doctor":
            prompt = f"""
        {self.get_base_prompt()}

        It's night time - time to protect someone! Choose a player to save from elimination.

        Current living players: {', '.join(player_names)}

        Think about who to protect:
        - Who might be targeted by the Mafia tonight?
        - Is there someone crucial to the good team's success?
        - Should you protect yourself or someone else?

        Based on the game so far, who would you like to protect? Respond with ONLY the name of one player from the list above.
        """
        else:
            return None  # Regular citizens don't make night decisions
            
        try:
            messages = [SystemMessage(content=prompt)]
            response = self.llm.invoke(messages).content
            
            # Clean up response to just get the name
            for player_name in player_names:
                if player_name.lower() in response.lower():
                    logger.info(f"Player {self.name} ({self.role}) chose {player_name}")
                    return player_name
                    
            # If no valid name found, choose randomly
            random_choice = random.choice(player_names)
            logger.info(f"Player {self.name} ({self.role}) made invalid choice, randomly selecting {random_choice}")
            return random_choice
            
        except Exception as e:
            logger.error(f"Error in night decision for {self.name}: {str(e)}")
            return random.choice(player_names)  # Fallback to random choice

    def vote(self, game_state):
        living_players = [p for p in game_state["players"] if p.alive and p.name != self.name]
        if not living_players:
            return None
            
        player_names = [p.name for p in living_players]
        
        prompt = f"""
        {self.get_base_prompt()}

        It's time to vote! The town must decide who to exile based on your discussion.

        Current living players: {', '.join(player_names)}

        The recent discussion has included:
        {game_state['discussion_log']}

        Consider carefully:
        - Who has made inconsistent claims?
        - Who seems to be protecting suspicious players?
        - Who has failed to contribute useful information?
        - What does your gut tell you about who's evil?

        Based on the discussions, who would you vote to exile? Respond with ONLY the name of one player from the list above.
        """
        
        try:
            messages = [SystemMessage(content=prompt)]
            response = self.llm.invoke(messages).content
            
            # Clean up response to just get the name
            for player_name in player_names:
                if player_name.lower() in response.lower():
                    logger.info(f"Player {self.name} ({self.role}) voted for {player_name}")
                    return player_name
                    
            # If no valid name found, choose randomly
            random_choice = random.choice(player_names)
            logger.info(f"Player {self.name} ({self.role}) made invalid vote, randomly selecting {random_choice}")
            return random_choice
            
        except Exception as e:
            logger.error(f"Error in voting for {self.name}: {str(e)}")
            return random.choice(player_names)  # Fallback to random choice

class Game:
    def __init__(self, game_id, personalities, has_human_player=False):
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
        
        # Create players with selected personalities
        player_offset = 0
        if has_human_player:
            # Create human player first
            self.players.append(Player("Player_1", "Human"))
            player_offset = 1
        
        # Then add AI personalities with proper offset
        for i, personality in enumerate(personalities):
            player_name = f"Player_{i+1+player_offset}"
            self.players.append(Player(player_name, personality))
                
            # Assign roles
            self.assign_roles()
            
    def assign_roles(self):
        # Shuffle players
        random.shuffle(self.players)
        
        # Assign roles
        roles = ["Mafia", "Bad Guy", "Detective", "Doctor"] + ["Citizen"] * (len(self.players) - 4)
        for i, player in enumerate(self.players):
            player.role = roles[i]
            logger.info(f"Assigned {player.name} as {player.role} with {player.personality} personality")
            
    def start_game(self):
        self.phase = "night"
        self.round = 1
        self.events_log.append(f"Game started. Round {self.round}.")
        logger.info(f"Game {self.id} started with {len(self.players)} players")
        return self.get_state()
        
    def get_state(self):
        return {
            "id": self.id,
            "players": self.players,
            "phase": self.phase,
            "round": self.round,
            "events_log": "\n".join(self.events_log),
            "discussion_log": "\n".join(self.discussion_log),
            "game_over": self.check_game_over()[0],
            "winner": self.check_game_over()[1]
        }
        
    def process_night(self):
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
        return self.night_actions
        
    def resolve_night(self):
        self.phase = "dawn"
        
        # Process detective investigation
        detective_success = False
        if self.night_actions["detective_target"]:
            target_player = next((p for p in self.players if p.name == self.night_actions["detective_target"]), None)
            if target_player and target_player.role == "Mafia":
                detective_success = True
                
        # Process mafia kill
        killed_player = None
        if self.night_actions["mafia_target"] and self.night_actions["mafia_target"] != self.night_actions["doctor_target"]:
            target_player = next((p for p in self.players if p.name == self.night_actions["mafia_target"]), None)
            if target_player:
                target_player.alive = False
                killed_player = target_player.name
                self.events_log.append(f"{killed_player} was killed during the night.")
        
        # Create dawn announcement
        dawn_results = {
            "detective_success": detective_success,
            "doctor_success": self.night_actions["mafia_target"] == self.night_actions["doctor_target"],
            "killed_player": killed_player
        }
        
        # Add to event log
        self.events_log.append(f"Dawn of Day {self.round}:")
        self.events_log.append(f"Detective {'' if detective_success else 'failed to'} identify the Mafia.")
        
        if dawn_results["doctor_success"] and self.night_actions["mafia_target"]:
            self.events_log.append(f"Doctor successfully saved {self.night_actions['doctor_target']}.")
        elif killed_player:
            self.events_log.append(f"{killed_player} was found dead.")
        else:
            self.events_log.append("No one died during the night.")
            
        logger.info(f"Dawn results: {dawn_results}")
        return dawn_results
        
    def start_discussion(self):
        self.phase = "discussion"
        self.discussion_log = []
        return self.get_state()
        
    # Complete rewrite of simulate_discussion method
    def simulate_discussion(self, num_rounds=3):
        logger.info(f"Starting discussion for game {self.id}")
        self.discussion_log = []
        living_players = [p for p in self.players if p.alive]
        
        # Only add the first round header and wait for players to respond in sequence
        round_header = "--- Discussion Round 1 ---"
        self.discussion_log.append(round_header)
        
        # Start with the first player and let the polling system handle the rest
        self.current_speaker_index = 0
        self.current_round = 1
        
        # If first player is human, add waiting marker
        if self.has_human_player and living_players[0].name == "Player_1":
            self.discussion_log.append("WAITING_FOR_HUMAN_INPUT")
            return
        
        # Otherwise, get first AI player response
        self._get_next_ai_response()
        return

    # New method to handle sequential responses
    def _get_next_ai_response(self):
        living_players = [p for p in self.players if p.alive]
        
        # If we've gone through all players in current round
        if self.current_speaker_index >= len(living_players):
            # Move to next round if not at round 3 yet
            if self.current_round < 3:
                self.current_round += 1
                self.current_speaker_index = 0
                round_header = f"--- Discussion Round {self.current_round} ---"
                self.discussion_log.append(round_header)
                
                # If first player of new round is human
                if self.has_human_player and living_players[0].name == "Player_1":
                    self.discussion_log.append("WAITING_FOR_HUMAN_INPUT")
                    return
            else:
                # Discussion complete
                logger.info("Discussion complete")
                return
        
        # Get current player
        current_player = living_players[self.current_speaker_index]
        
        # If current player is human, add waiting marker
        if self.has_human_player and current_player.name == "Player_1":
            self.discussion_log.append("WAITING_FOR_HUMAN_INPUT")
            self.current_speaker_index += 1
            return
        
        # Get appropriate topic for current round
        topic = "What do you all think happened last night? Who seems suspicious to you?"
        if self.current_round == 2:
            topic = "Let's discuss our suspicions more. Anyone acting strangely?"
        elif self.current_round == 3:
            topic = "We need to decide who to vote out. Make your final case."
        
        # Get context for AI response
        previous_messages = "\n".join(self.discussion_log[-min(5, len(self.discussion_log)):])
        logger.info(f"Getting response from {current_player.name} ({current_player.role})")
        
        try:
            response = current_player.generate_response(f"{topic}\n\nPrevious messages:\n{previous_messages}", self.get_state())
            logger.info(f"Response from {current_player.name}: {response[:50]}...")
            self.discussion_log.append(f"{current_player.name}: {response}")
        except Exception as e:
            logger.error(f"Error getting response from {current_player.name}: {str(e)}")
            self.discussion_log.append(f"{current_player.name}: I'm thinking about what to say...")
        
        # Move to next player
        self.current_speaker_index += 1
        
        # Process next player with a small delay
        time.sleep(0.2)
        self._get_next_ai_response()
    
    # Make sure to add the continue_discussion_from method to the Game class if you haven't already
    def continue_discussion_from(self, current_round, current_position):
        """Continue discussion from a specific point after human input"""
        living_players = [p for p in self.players if p.alive]
            
        # Add each player's response for current round, EXCEPT human
        for player in living_players:
            # If human player, add placeholder and STOP - don't continue to next players
            if self.has_human_player and player.name == "Player_1":
                self.discussion_log.append("WAITING_FOR_HUMAN_INPUT")
                return  # Critical: Return here to pause discussion

        # Calculate which players have already spoken in this round
        spoken_players = set()
        for i in range(current_position, len(self.discussion_log)):
            line = self.discussion_log[i]
            if ":" in line:
                player_name = line.split(":")[0].strip()
                spoken_players.add(player_name)
        
        # Get remaining players for this round
        remaining_players = [p for p in living_players if p.name not in spoken_players]
        topic = "Let's continue our discussion. Who seems suspicious to you?"
        
        # Each remaining player responds for this round
        for player in remaining_players:
            # Skip human player
            if self.has_human_player and player.name == "Player_1":
                continue
                
            # Get previous messages for context
            previous_messages = "\n".join(self.discussion_log[-min(5, len(self.discussion_log)):])
            logger.info(f"Getting response from {player.name} ({player.role})")
            
            try:
                response = player.generate_response(f"{topic}\n\nPrevious messages:\n{previous_messages}", self.get_state())
                logger.info(f"Response from {player.name}: {response[:50]}...")
                
                # Add response to log
                message = f"{player.name}: {response}"
                self.discussion_log.append(message)
                
                # Small delay
                time.sleep(0.2)
            except Exception as e:
                logger.error(f"Error getting response from {player.name}: {str(e)}")
                self.discussion_log.append(f"{player.name}: I'm thinking about what to say...")
                time.sleep(0.2)
        
        # Continue with next rounds if this round is complete
        if current_round < 3:
            # Add next round header
            next_round = current_round + 1
            round_header = f"--- Discussion Round {next_round} ---"
            self.discussion_log.append(round_header)
            time.sleep(0.5)
            
            # Set topic for next round
            if next_round == 2:
                topic = "Let's discuss our suspicions more. Anyone acting strangely?"
            else:
                topic = "We need to decide who to vote out. Make your final case."
            
            # Each player responds for the next round
            for player in living_players:
                # Skip human player - will be prompted by frontend
                if self.has_human_player and player.name == "Player_1":
                    self.discussion_log.append("WAITING_FOR_HUMAN_INPUT")
                    return  # Stop here and wait for human input
                    
                # Get previous messages for context
                previous_messages = "\n".join(self.discussion_log[-min(5, len(self.discussion_log)):])
                logger.info(f"Getting response from {player.name} ({player.role})")
                
                try:
                    response = player.generate_response(f"{topic}\n\nPrevious messages:\n{previous_messages}", self.get_state())
                    logger.info(f"Response from {player.name}: {response[:50]}...")
                    
                    # Add response to log
                    message = f"{player.name}: {response}"
                    self.discussion_log.append(message)
                    
                    # Small delay
                    time.sleep(0.2)
                except Exception as e:
                    logger.error(f"Error getting response from {player.name}: {str(e)}")
                    self.discussion_log.append(f"{player.name}: I'm thinking about what to say...")
                    time.sleep(0.2)
    
    def process_voting(self):
        self.phase = "voting"
        living_players = [p for p in self.players if p.alive]
        
        # Each living player votes
        votes = {}
        for player in living_players:
            vote = player.vote(self.get_state())
            if vote:
                votes[vote] = votes.get(vote, 0) + 1
                
        # Find player with most votes
        if votes:
            exiled_player_name = max(votes.items(), key=lambda x: x[1])[0]
            exiled_player = next((p for p in self.players if p.name == exiled_player_name), None)
            
            if exiled_player:
                exiled_player.alive = False
                self.events_log.append(f"{exiled_player.name} ({exiled_player.role}) was exiled from the city.")
                logger.info(f"Player {exiled_player.name} ({exiled_player.role}) was exiled")
                
                # Check if game is over
                game_over, winner = self.check_game_over()
                if game_over:
                    self.events_log.append(f"Game Over! {winner} team wins!")
                    return {"exiled": exiled_player.name, "exiled_role": exiled_player.role, "game_over": True, "winner": winner}
                
                # Move to next night
                self.phase = "night"
                self.round += 1
                self.events_log.append(f"Night {self.round} begins.")
                return {"exiled": exiled_player.name, "exiled_role": exiled_player.role, "game_over": False}
                
        # No valid votes
        self.events_log.append("No one was exiled due to a tie or invalid votes.")
        self.phase = "night"
        self.round += 1
        return {"exiled": None, "game_over": False}
        
    def check_game_over(self):
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/personalities', methods=['GET'])
def get_personalities():
    return jsonify(PERSONALITIES)



#@app.route('/api/create_game', methods=['POST'])
#def create_game():
    data = request.json
    personalities = data.get('personalities', [])
    
    if len(personalities) != 6:
        return jsonify({"error": "Please select exactly 6 personalities"}), 400
        
    game_id = str(uuid.uuid4())
    games[game_id] = Game(game_id, personalities)
    
    return jsonify({
        "game_id": game_id,
        "message": "Game created successfully"
    })

@app.route('/api/start_game/<game_id>', methods=['POST'])
def start_game(game_id):
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404
        
    game = games[game_id]
    game_state = game.start_game()
    
    return jsonify({
        "message": "Game started",
        "state": {
            "phase": game_state["phase"],
            "round": game_state["round"],
            "players": [{"name": p.name, "personality": p.personality, "alive": p.alive} for p in game_state["players"]],
            "events": game_state["events_log"]
        }
    })


# Add this endpoint to your Flask app.py file

@app.route('/api/debug_api_keys', methods=['GET'])
def debug_api_keys():
    """Check if API keys are loaded and valid."""
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    
    if not api_key or not endpoint:
        logger.warning("API keys are missing or invalid")
        return jsonify({
            "status": "error",
            "message": "API keys are missing or invalid",
            "api_key_mask": mask_string(api_key) if api_key else None,
            "endpoint_mask": mask_string(endpoint) if endpoint else None
        })
    
    logger.info("API keys loaded successfully")
    return jsonify({
        "status": "ok",
        "message": "API keys loaded successfully",
        "api_key_mask": mask_string(api_key),
        "endpoint_mask": mask_string(endpoint)
    })

def mask_string(s):
    """Mask a string to show only first and last 4 characters."""
    if not s or len(s) < 8:
        return "****"
    return s[:4] + "*" * (len(s) - 8) + s[-4:]

# Modify process_night function to handle human night actions
@app.route('/api/process_night/<game_id>', methods=['POST'])
def process_night(game_id):
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404
        
    game = games[game_id]
    
    # Skip AI decisions for roles already chosen by human
    for player in game.players:
        if not player.alive:
            continue
            
        if game.has_human_player and player.name == "Player_1":
            # Skip human player - they'll use human_night_action endpoint
            continue
            
        if player.role == "Mafia" and not game.night_actions["mafia_target"]:
            game.night_actions["mafia_target"] = player.make_night_decision(game.get_state())
        elif player.role == "Detective" and not game.night_actions["detective_target"]:
            game.night_actions["detective_target"] = player.make_night_decision(game.get_state())
        elif player.role == "Doctor" and not game.night_actions["doctor_target"]:
            game.night_actions["doctor_target"] = player.make_night_decision(game.get_state())
    
    logger.info(f"Night actions: {game.night_actions}")
    return jsonify({
        "message": "Night actions processed",
        "actions": game.night_actions
    })

@app.route('/api/resolve_night/<game_id>', methods=['POST'])
def resolve_night(game_id):
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404
        
    game = games[game_id]
    dawn_results = game.resolve_night()
    
    return jsonify({
        "message": "Night resolved",
        "results": dawn_results,
        "state": {
            "phase": game.phase,
            "round": game.round,
            "events": game.events_log[-3:],  # Last 3 events
            "players": [{"name": p.name, "personality": p.personality, "alive": p.alive} for p in game.players]
        }
    })

@app.route('/api/start_discussion/<game_id>', methods=['POST'])
def start_discussion(game_id):
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404
        
    game = games[game_id]
    game.start_discussion()
    
    return jsonify({
        "message": "Discussion started",
        "state": {
            "phase": game.phase,
            "round": game.round
        }
    })


@app.route('/api/simulate_discussion/<game_id>', methods=['POST'])
def simulate_discussion(game_id):
    if game_id not in games:
        logger.error(f"Game {game_id} not found")
        return jsonify({"error": "Game not found"}), 404
        
    game = games[game_id]
    
    # Start a background thread to run the discussion simulation
    @copy_current_request_context
    def run_discussion_in_background():
        logger.info(f"Starting discussion simulation in background thread for game {game_id}")
        try:
            game.simulate_discussion()
            logger.info(f"Background discussion simulation complete for game {game_id}")
        except Exception as e:
            logger.error(f"Error in background discussion simulation: {str(e)}")
    
    # Launch the background thread
    thread = threading.Thread(target=run_discussion_in_background)
    thread.daemon = True
    thread.start()
    
    return jsonify({
        "message": "Discussion simulation started in background",
        "status": "in_progress"
    })

@app.route('/api/discussion_status/<game_id>', methods=['GET'])
def discussion_status(game_id):
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404
        
    game = games[game_id]
    
    # Get the current discussion log
    discussion = game.discussion_log
    
    # Calculate progress information
    living_players = [p for p in game.players if p.alive]
    total_players = len(living_players)
    total_rounds = 3
    expected_messages = total_players * total_rounds + total_rounds # Player messages + round headers
    
    # Count messages from each player to track who's "speaking" next
    player_counts = {}
    current_round = 1
    for line in discussion:
        if line.startswith("---") and "Round" in line:
            try:
                current_round = int(line.split("Round")[1].strip().split()[0])
            except:
                pass
        elif ":" in line:
            player_name = line.split(":")[0].strip()
            if player_name not in player_counts:
                player_counts[player_name] = 1
            else:
                player_counts[player_name] += 1
    
    # Determine who might be speaking next
    next_speaker = None
    if discussion and total_players > 0:
        for player in living_players:
            # If player hasn't spoken in the current round
            count = player_counts.get(player.name, 0)
            if count < current_round:
                next_speaker = player.name
                break
    
    # Check if discussion is still in progress
    thread_active = any(t.name.startswith("Thread-") and t.is_alive() for t in threading.enumerate())
    waiting_for_human = "WAITING_FOR_HUMAN_INPUT" in discussion
    
    # Determine if discussion is in progress based on thread status and message count
    if game.phase == "discussion" and (thread_active or len(discussion) < expected_messages or waiting_for_human):
        in_progress = True
        # Safely calculate progress percentage
        if expected_messages > 0:
            progress_percent = min(100, int((len(discussion) / expected_messages) * 100))
        else:
            progress_percent = 0
    else:
        in_progress = False
        progress_percent = 100
    
    # Debug information
    logger.info(f"Discussion status: {len(discussion)}/{expected_messages} messages, " +
                f"in_progress={in_progress}, thread_active={thread_active}, " +
                f"next_speaker={next_speaker}, progress={progress_percent}%, " +
                f"waiting_for_human={waiting_for_human}")
    
    return jsonify({
        "discussion": discussion,
        "in_progress": in_progress,
        "progress": progress_percent,
        "total_expected": expected_messages,
        "current_count": len(discussion),
        "next_speaker": next_speaker,
        "current_round": current_round,
        "waiting_for_human": waiting_for_human
    })

@app.route('/api/process_voting/<game_id>', methods=['POST'])
def process_voting(game_id):
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404
        
    game = games[game_id]
    
    # Track votes
    votes = {}
    living_players = [p for p in game.players if p.alive]
    
    # Each living player votes
    for player in living_players:
        vote = player.vote(game.get_state())
        if vote:
            votes[player.name] = vote
    
    voting_results = game.process_voting()
    
    return jsonify({
        "message": "Voting processed",
        "results": voting_results,
        "votes": votes,  # Add votes to response
        "state": {
            "phase": game.phase,
            "round": game.round,
            "events": game.events_log[-2:],
            "players": [{"name": p.name, "personality": p.personality, "role": p.role, "alive": p.alive} for p in game.players],
            "game_over": voting_results.get("game_over", False),
            "winner": voting_results.get("winner", None)
        }
    })

@app.route('/api/game_state/<game_id>', methods=['GET'])
def get_game_state(game_id):
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404
        
    game = games[game_id]
    state = game.get_state()
    
    # This line needs to include the role attribute
    return jsonify({
        "id": state["id"],
        "phase": state["phase"],
        "round": state["round"],
        "players": [{"name": p.name, "personality": p.personality, "role": p.role, "alive": p.alive} for p in state["players"]],
        "events": state["events_log"].split("\n"),
        "discussion": state["discussion_log"].split("\n") if state["discussion_log"] else [],
        "game_over": state["game_over"],
        "winner": state["winner"]
    })

@app.route('/api/reset_game/<game_id>', methods=['POST'])
def reset_game(game_id):
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404
        
    # Get current personalities
    personalities = [p.personality for p in games[game_id].players]
    
    # Create new game with same personalities
    games[game_id] = Game(game_id, personalities)
    
    return jsonify({
        "message": "Game reset successfully",
        "game_id": game_id
    })

####################################################################################################################################
# Human player endpoints

####################################################################################################################################

@app.route('/api/human_night_action/<game_id>', methods=['POST'])
def human_night_action(game_id):
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404
        
    game = games[game_id]
    data = request.json
    role = data.get('role')
    target = data.get('target')
    
    if not role or not target:
        return jsonify({"error": "Missing role or target"}), 400
    
    # Update night actions based on the role
    if role == "Mafia":
        game.night_actions["mafia_target"] = target
    elif role == "Detective":
        game.night_actions["detective_target"] = target
    elif role == "Doctor":
        game.night_actions["doctor_target"] = target
    else:
        return jsonify({"error": "Invalid role for night action"}), 400
    
    logger.info(f"Human player with role {role} chose {target}")
    
    return jsonify({
        "message": f"Human player night action set: {role} targeting {target}",
        "status": "success"
    })

# Rewrite human_discussion endpoint
@app.route('/api/human_discussion/<game_id>', methods=['POST'])
def human_discussion(game_id):
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404
        
    game = games[game_id]
    data = request.json
    message = data.get('message')
    
    if not message:
        return jsonify({"error": "Missing message"}), 400
    
    # Remove waiting marker
    try:
        placeholder_index = game.discussion_log.index("WAITING_FOR_HUMAN_INPUT")
        game.discussion_log.pop(placeholder_index)
    except ValueError:
        logger.warning("No waiting marker found")
    
    # Add human message
    game.discussion_log.append(f"Player_1: {message}")
    logger.info(f"Human player added message: {message[:50]}...")
    
    # Continue with next AI responses
    game._get_next_ai_response()
    
    return jsonify({
        "message": "Human message added",
        "status": "success"
    })

@app.route('/api/human_vote/<game_id>', methods=['POST'])
def human_vote(game_id):
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404
        
    game = games[game_id]
    data = request.json
    target = data.get('target')
    
    if not target:
        return jsonify({"error": "Missing target"}), 400
    
    # Record the human player's vote
    # We'll assume Player_1 is always the human player
    human_player = next((p for p in game.players if p.name == "Player_1"), None)
    
    if not human_player:
        return jsonify({"error": "Human player not found"}), 400
    
    # Update votes dictionary (create one if it doesn't exist)
    if not hasattr(game, 'votes'):
        game.votes = {}
    
    game.votes["Player_1"] = target
    logger.info(f"Human player voted for {target}")
    
    return jsonify({
        "message": f"Human player vote recorded for {target}",
        "status": "success"
    })

# Modify existing endpoints to handle human player

@app.route('/api/create_game', methods=['POST'])
def create_game():
    data = request.json
    personalities = data.get('personalities', [])
    is_human_player = data.get('isHumanPlayer', False)
    
    # If human player is selected, we need only 5 AI personalities
    required_count = 5 if is_human_player else 6
    
    if len(personalities) != required_count:
        return jsonify({"error": f"Please select exactly {required_count} personalities"}), 400
        
    game_id = str(uuid.uuid4())
    games[game_id] = Game(game_id, personalities, is_human_player)
    
    return jsonify({
        "game_id": game_id,
        "message": "Game created successfully"
    })

# Add a continue_discussion endpoint for the human player flow
@app.route('/api/continue_discussion/<game_id>', methods=['POST'])
def continue_discussion(game_id):
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404
        
    game = games[game_id]
    
    # Remove the waiting placeholder if it exists
    game.discussion_log = [msg for msg in game.discussion_log if msg != "WAITING_FOR_HUMAN_INPUT"]
    
    # Continue the discussion simulation in the background
    @copy_current_request_context
    def continue_in_background():
        logger.info(f"Continuing discussion simulation in background thread for game {game_id}")
        try:
            # Get current round and position
            current_round = 1
            current_position = 0
            
            for i, line in enumerate(game.discussion_log):
                if line.startswith("--- Discussion Round"):
                    try:
                        current_round = int(line.split("Round")[1].strip().split()[0])
                    except:
                        pass
                    current_position = i
            
            # Continue with AI player responses for the current round
            game.continue_discussion_from(current_round, current_position)
            logger.info(f"Continued discussion simulation complete for game {game_id}")
        except Exception as e:
            logger.error(f"Error in continued discussion simulation: {str(e)}")
    
    # Launch the background thread
    thread = threading.Thread(target=continue_in_background)
    thread.daemon = True
    thread.start()
    
    return jsonify({
        "message": "Discussion continuation started",
        "status": "in_progress"
    })

####################################################################################################################################

if __name__ == '__main__':
    app.run(debug=True)