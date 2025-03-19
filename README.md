# AI Mafia Game

A modern implementation of the classic social deduction game "Mafia" powered by AI agents with distinct personalities.

![AI Mafia Game Screenshot](https://github.com/PranavMishra17/Mafia-Boardgame-via-Agents/blob/2ea1451b616dbd689ce937722ce12345b3f06c5e/image_2025-03-18_185729797.png)

## Overview

AI Mafia Game is a full-stack application that simulates the classic party game Mafia (also known as Werewolf) where AI agents with unique personalities and characteristics play against each other. The project demonstrates advanced AI integration, real-time simulation, and interactive visualization of complex social dynamics.

## Technology Stack

- **Frontend**: React, CSS3, Modern JavaScript (ES6+)
- **Backend**: Flask, Python 3.9+
- **AI Integration**: Azure OpenAI API, LangChain
- **State Management**: React Hooks
- **API Communication**: RESTful API architecture
- **Development Tools**: Webpack, npm, Git

## Key Features

- **AI Agent Simulation**: Each AI player has a unique personality profile affecting their behavior
- **Complex Decision Making**: AI agents make strategic decisions based on game state and personality traits
- **Real-time Discussion Visualization**: Watch AI agents debate, accuse, and defend themselves
- **Responsive UI**: Modern, responsive interface with interactive game elements
- **Customizable Personalities**: Create and modify personality traits to experiment with different game dynamics
- **Role-based Gameplay**: Classic Mafia roles including Detectives, Doctors, Mafia, and Citizens

## Game Workflow

1. **Setup Phase**:
   - Select 6 AI personalities to participate in the game
   - Each personality has unique traits like truthfulness, aggressiveness, suspicion, etc.
   - Customize personalities or create your own to experiment with different combinations

2. **Game Phase**:
   - **Night**: Secret actions are taken by special roles (Mafia, Detective, Doctor)
   - **Dawn**: Announcements are made about the night's events
   - **Discussion**: AI agents debate and try to identify Mafia members
   - **Voting**: AI agents vote to exile someone based on discussions

3. **Observation**:
   - Watch AI agents with different personalities interact
   - See how deception, logic, and personality traits affect outcomes
   - Analyze game events to understand social dynamics

## Technical Implementation

- **AI Agent Architecture**: Each agent uses LangChain and Azure OpenAI's capabilities for realistic dialogue generation and decision-making
- **Game Engine**: Core game logic implemented in Python with state management
- **Real-time Discussion**: AI agents analyze each other's statements and respond appropriately
- **Personality Modeling**: Quantifiable personality traits influence AI behavior and strategy

## First day
Night actions were processed. Agents will begin the discussion now
![AI Mafia Game Screenshot](https://github.com/PranavMishra17/Mafia-Boardgame-via-Agents/blob/2ea1451b616dbd689ce937722ce12345b3f06c5e/image_2025-03-18_185822657.png)

## End of Day
3 Discussion rounds were held. Convos can be view in the card. After discussion, voting is held, eliminating another player from the game.
![AI Mafia Game Screenshot](https://github.com/PranavMishra17/Mafia-Boardgame-via-Agents/blob/2ea1451b616dbd689ce937722ce12345b3f06c5e/image_2025-03-18_190005501.png)

## Running the Project

### Prerequisites
- Node.js (v14+)
- Python 3.9+
- Azure OpenAI API access

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-mafia-game.git
cd ai-mafia-game
```

2. Install frontend dependencies:
```bash
npm install
```

3. Install backend dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API credentials:
```
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=your_endpoint
```

5. Start the backend server:
```bash
python app.py
```

6. Start the frontend development server:
```bash
npm start
```

7. Open your browser to `http://localhost:3000`

## Learning Opportunity

This project demonstrates several advanced concepts including:

- **AI Agent Development**: Creating AI personalities with specific traits
- **Game Theory**: Implementing strategic decision-making algorithms
- **Full-stack Architecture**: Connecting React frontend with Python backend
- **Real-time Interaction**: Managing complex state between simulated agents
- **Large Language Model Integration**: Leveraging Azure OpenAI for realistic dialogue

## Future Enhancements

- Additional personality traits and roles
- Machine learning to analyze game patterns
- Multiplayer mode with human players
- Advanced analytics on game outcomes
- Mobile app version for on-the-go play

## License

MIT

## Keywords

AI Agents, React, Flask, Python, Azure OpenAI, LangChain, Social Simulation, Game Theory, Strategic Decision Making, Full-Stack Development, UI/UX Design, REST API, JavaScript, Interactive Visualization, Agent-based Modeling, Real-time Simulation
