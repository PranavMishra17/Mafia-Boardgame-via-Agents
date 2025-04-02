import logging
import uuid
import random
from typing import List, Dict, Any, Optional, Tuple

from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.memory import ConversationBufferMemory

from agents.personalities import PERSONALITIES

logger = logging.getLogger(__name__)

class Player:
    def __init__(self, name: str, personality: str, role: Optional[str] = None, is_human: bool = False):
        """Initialize a player in the Mafia game.
        
        Args:
            name: Player's name
            personality: Player's personality type
            role: Player's role in the game (Mafia, Detective, etc.)
            is_human: Whether this player is human-controlled
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.personality = personality
        self.role = role
        self.alive = True
        self.is_human = is_human
        self.memory = ConversationBufferMemory()
        self.thoughts_log = []  # For storing player's internal thought process
        
        # Skip LLM initialization for human players
        if not is_human:
            self.llm = AzureChatOpenAI(
                azure_deployment="VARELab-GPT4o",
                api_key="428KgVArXb6sFyseVYDjElDDYZnlCnx8pNa8CfU5dCic6gjOK89WJQQJ99BBACYeBjFXJ3w3AAABACOG5gtQ",
                api_version="2025-01-01-preview",
                azure_endpoint="https://vare-labs-azure-openai-resource.openai.azure.com/",
                temperature=0.7,
                max_tokens=500,
                timeout=None,
                max_retries=2,
            )
        
    def get_base_prompt(self) -> str:
        """Create the base prompt for the player based on their personality and role."""
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

    def generate_response(self, context: str, game_state: Dict[str, Any]) -> str:
        """Generate a player's response based on game context.
        
        Args:
            context: Current discussion context
            game_state: Current game state
            
        Returns:
            Player's response as a string
        """
        if self.is_human:
            return "WAITING_FOR_HUMAN_INPUT"
            
        if not self.alive:
            return "I'm dead and can't participate in the discussion."
            
        role_info = f"Your role is {self.role}."
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
            
            # Log the thinking process
            self.thoughts_log.append(f"--- Thinking about response to: {context} ---\n{system_prompt}\n")
            
            response = self.llm.invoke(messages).content
            
            # Log the conversation
            logger.info(f"Player {self.name} ({self.role}) - Context: {context}")
            logger.info(f"Player {self.name} ({self.role}) - Response: {response}")
            
            # Log the response to thoughts
            self.thoughts_log.append(f"--- My response ---\n{response}\n")
            
            return response
        except Exception as e:
            logger.error(f"Error generating response for {self.name}: {str(e)}")
            return "I need a moment to gather my thoughts..."

    def make_night_decision(self, game_state: Dict[str, Any]) -> Optional[str]:
        """Make night phase decision based on player role.
        
        Args:
            game_state: Current game state
            
        Returns:
            Name of the player chosen for the night action, or None
        """
        if self.is_human:
            return None  # Human players make decisions through the human_night_action endpoint
            
        living_players = [p for p in game_state["players"] if p.alive and p.name != self.name]
        if not living_players:
            return None
            
        player_names = [p.name for p in living_players]
        
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
            # Log the thinking process
            self.thoughts_log.append(f"--- Night decision thinking ---\n{prompt}\n")
            
            messages = [SystemMessage(content=prompt)]
            response = self.llm.invoke(messages).content
            
            # Log the response
            self.thoughts_log.append(f"--- Night decision ---\n{response}\n")
            
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

    def vote(self, game_state: Dict[str, Any]) -> Optional[str]:
        """Vote for a player to exile during the day phase.
        
        Args:
            game_state: Current game state
            
        Returns:
            Name of the player voted for, or None
        """
        if self.is_human:
            return None  # Human players vote through the human_vote endpoint
            
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
            # Log the thinking process
            self.thoughts_log.append(f"--- Voting thinking ---\n{prompt}\n")
            
            messages = [SystemMessage(content=prompt)]
            response = self.llm.invoke(messages).content
            
            # Log the response
            self.thoughts_log.append(f"--- Voting decision ---\n{response}\n")
            
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
    
    def save_thoughts(self, game_id: str, round_num: int, save_dir: str) -> None:
        """Save player thoughts to a file.
        
        Args:
            game_id: Unique game identifier
            round_num: Current game round
            save_dir: Directory to save the file
        """
        import os
        from datetime import datetime
        
        # Ensure directory exists
        os.makedirs(save_dir, exist_ok=True)
        
        # Create a filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{save_dir}/{self.name}_{self.role}_{game_id}_round{round_num}_{timestamp}.txt"
        
        # Write thoughts to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Player: {self.name}\n")
            f.write(f"Role: {self.role}\n")
            f.write(f"Personality: {self.personality}\n")
            f.write(f"Alive: {self.alive}\n\n")
            f.write("THOUGHTS LOG:\n\n")
            f.write("\n".join(self.thoughts_log))
            
        logger.info(f"Saved thoughts for {self.name} to {filename}")