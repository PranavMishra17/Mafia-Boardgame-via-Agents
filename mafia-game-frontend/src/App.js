import React, { useState, useEffect, useRef } from 'react';
import './App.css';

// API URL - change to match your Flask server
// Should match your Flask server
const API_URL = 'http://localhost:5000/api';

// Global loading context
const LoadingContext = React.createContext();

const LoadingProvider = ({ children }) => {
  const [loading, setLoading] = useState({ show: false, message: "Loading..." });
  
  return (
    <LoadingContext.Provider value={{ loading, setLoading }}>
      {children}
      {loading.show && <LoadingOverlay message={loading.message} />}
    </LoadingContext.Provider>
  );
};

// Hook to use the loading context
const useLoading = () => {
  const context = React.useContext(LoadingContext);
  if (!context) {
    throw new Error('useLoading must be used within a LoadingProvider');
  }
  return context;
};

// Loading overlay component
const LoadingOverlay = ({ message = "Loading..." }) => {
  return (
    <div className="loading-overlay">
      <div className="loading-container">
        <div className="loading-spinner-large"></div>
        <p className="loading-message">{message}</p>
      </div>
    </div>
  );
};

// Simplified UI components
const Card = ({ children, className }) => (
  <div className={`card ${className || ''}`}>{children}</div>
);

const CardHeader = ({ children }) => <div className="card-header">{children}</div>;
const CardTitle = ({ children }) => <h3 className="card-title">{children}</h3>;
const CardDescription = ({ children }) => <p className="card-description">{children}</p>;
const CardContent = ({ children }) => <div className="card-content">{children}</div>;
const CardFooter = ({ children }) => <div className="card-footer">{children}</div>;



// Replace the Button component with this enhanced version
const Button = ({ children, onClick, variant, size, disabled, isLoading, loadingText }) => {
  const [showTooltip, setShowTooltip] = useState(false);
  
  const handleClick = async (e) => {
    if (isLoading || disabled) return;
    
    // Show loading state
    setShowTooltip(true);
    
    try {
      await onClick(e);
    } finally {
      // Hide loading state
      setShowTooltip(false);
    }
  };
  
  return (
    <div className="button-container" style={{ position: 'relative' }}>
      {showTooltip && loadingText && (
        <div className="tooltip-loading">
          <div className="tooltip-spinner"></div>
          <span>{loadingText}</span>
        </div>
      )}
      <button 
        className={`button ${variant || 'primary'} ${size || 'md'} ${isLoading ? 'button-with-loading' : ''}`} 
        onClick={handleClick}
        disabled={disabled || isLoading}
      >
        {children}
      </button>
    </div>
  );
};

const Progress = ({ value, className }) => (
  <div className={`progress-container ${className || ''}`}>
    <div className="progress-bar" style={{ width: `${value}%` }}></div>
  </div>
);

const Badge = ({ children, variant }) => (
  <span className={`badge ${variant || 'default'}`}>{children}</span>
);

const Label = ({ children, htmlFor }) => (
  <label htmlFor={htmlFor} className="form-label">{children}</label>
);

const Input = ({ id, value, onChange }) => (
  <input 
    id={id} 
    type="text" 
    className="form-input" 
    value={value} 
    onChange={onChange} 
  />
);

const Alert = ({ children, variant }) => (
  <div className={`alert ${variant || 'default'}`}>{children}</div>
);

const AlertTitle = ({ children }) => <h4 className="alert-title">{children}</h4>;
const AlertDescription = ({ children }) => <p className="alert-description">{children}</p>;

const Slider = ({ id, value, min, max, step, onValueChange }) => (
  <input
    id={id}
    type="range"
    min={min}
    max={max}
    step={step}
    value={value[0]}
    onChange={(e) => onValueChange([parseInt(e.target.value)])}
    className="form-slider"
  />
);

// Icons
const Icon = ({ name }) => {
  const icons = {
    AlertCircle: "⚠️",
    CheckCircle: "✅",
    Skull: "☠️",
    Moon: "🌙",
    Sun: "☀️",
    Users: "👥",
    MessageSquare: "💬"
  };
  
  return <span className="icon">{icons[name] || "📌"}</span>;
};

// API functions
const fetchPersonalities = async () => {
  try {
    console.log('Fetching personalities...');
    const response = await fetch(`${API_URL}/personalities`);
    const data = await response.json();
    console.log('Received data:', data);
    return data;
  } catch (error) {
    console.error('Error fetching personalities:', error);
    return {};
  }
};

const createGame = async (personalities) => {
  try {
    const response = await fetch(`${API_URL}/create_game`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ personalities })
    });
    return await response.json();
  } catch (error) {
    console.error('Error creating game:', error);
    return { error: 'Failed to create game' };
  }
};

const startGame = async (gameId) => {
  try {
    const response = await fetch(`${API_URL}/start_game/${gameId}`, {
      method: 'POST',
    });
    return await response.json();
  } catch (error) {
    console.error('Error starting game:', error);
    return { error: 'Failed to start game' };
  }
};

const processNight = async (gameId) => {
  try {
    const response = await fetch(`${API_URL}/process_night/${gameId}`, {
      method: 'POST',
    });
    return await response.json();
  } catch (error) {
    console.error('Error processing night:', error);
    return { error: 'Failed to process night' };
  }
};

const resolveNight = async (gameId) => {
  try {
    const response = await fetch(`${API_URL}/resolve_night/${gameId}`, {
      method: 'POST',
    });
    return await response.json();
  } catch (error) {
    console.error('Error resolving night:', error);
    return { error: 'Failed to resolve night' };
  }
};



const startDiscussion = async (gameId) => {
  try {
    const response = await fetch(`${API_URL}/start_discussion/${gameId}`, {
      method: 'POST',
    });
    return await response.json();
  } catch (error) {
    console.error('Error starting discussion:', error);
    return { error: 'Failed to start discussion' };
  }
};

const simulateDiscussion = async (gameId) => {
  try {
    const response = await fetch(`${API_URL}/simulate_discussion/${gameId}`, {
      method: 'POST',
    });
    return await response.json();
  } catch (error) {
    console.error('Error simulating discussion:', error);
    return { error: 'Failed to simulate discussion' };
  }
};

const processVoting = async (gameId) => {
  try {
    const response = await fetch(`${API_URL}/process_voting/${gameId}`, {
      method: 'POST',
    });
    return await response.json();
  } catch (error) {
    console.error('Error processing voting:', error);
    return { error: 'Failed to process voting' };
  }
};

const getGameState = async (gameId) => {
  try {
    const response = await fetch(`${API_URL}/game_state/${gameId}`);
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching game state:', error);
    return { error: 'Failed to fetch game state' };
  }
};

const resetGame = async (gameId) => {
  try {
    const response = await fetch(`${API_URL}/reset_game/${gameId}`, {
      method: 'POST',
    });
    return await response.json();
  } catch (error) {
    console.error('Error resetting game:', error);
    return { error: 'Failed to reset game' };
  }
};

// Enhanced Personality Card
const PersonalityCard = ({ personality, details, selected, onSelect, onCustomize }) => {
  // Image mapping for personalities
  const personalityImages = {
    Diplomat: "/static/personalities/diplomat.png",
    Sheriff: "/static/personalities/sheriff.png",
    Conspirator: "/static/personalities/conspirator.jpg",
    Jester: "/static/personalities/jester.jpg",
    Mastermind: "/static/personalities/mastermind.jpg",
    Empath: "/static/personalities/empath.png",
    Wildcard: "/static/personalities/wildcard.jpg",
    Veteran: "/static/personalities/veteran.png",
    Innocent: "/static/personalities/innocent.jpg",
    Manipulator: "/static/personalities/manipulator.jpg"
  };

  // Debug: log image path
  const imagePath = personalityImages[personality] || "/static/personalities/default.jpg";
  
  // Add image error handling
  const [imageError, setImageError] = useState(false);
  
  const handleImageError = () => {
    console.error(`Failed to load image for ${personality}: ${imagePath}`);
    setImageError(true);
  };
  
  // Icon mapping for attributes
  const attributeIcons = {
    truthfulness: "✓",
    aggressiveness: "⚔️",
    suspicion: "🔍",
    persuasiveness: "💬",
    loyalty: "🤝",
  };
  
  const handleCardClick = () => {
    onSelect();
  };
  
  return (
    <div 
      className={`personality-card ${selected ? 'selected' : ''}`} 
      onClick={handleCardClick}
    >
      {/* Customize button in top-left corner */}
      <button 
        className="customize-button" 
        onClick={(e) => { e.stopPropagation(); onCustomize(personality); }}
      >
        Customize
      </button>
      
      {/* Show fallback if image fails or use proper image */}
      {imageError ? (
        <div className="personality-image-placeholder">
          <span className="personality-initial">{personality[0]}</span>
        </div>
      ) : (
        <img 
          src={imagePath}
          alt={personality}
          className="personality-image"
          onError={handleImageError}
        />
      )}
      
      <div className="card-header">
        <h3 className="card-title">{personality}</h3>
        <p className="card-description">{details.description}</p>
      </div>
      
      <div className="card-content">
        <div className="attributes">
          {Object.entries(details.attributes).map(([attr, value]) => (
            <div key={attr} className="personality-attribute">
              <span className="attribute-icon">{attributeIcons[attr] || "•"}</span>
              <span className="attribute-name">{attr}</span>
              <div className="attribute-bar">
                <div className="attribute-fill" style={{ width: `${value * 100}%` }}></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

const CustomizePersonalityModal = ({ personality, details, onSave, onCancel }) => {
  const [attributes, setAttributes] = useState(details.attributes);

  const handleAttributeChange = (attr, value) => {
    setAttributes(prev => ({ ...prev, [attr]: value[0] / 100 }));
  };

  return (
    <div className="modal-overlay">
      <Card className="modal-content">
        <CardHeader>
          <CardTitle>Customize {personality}</CardTitle>
          <CardDescription>Adjust the attributes to create your perfect personality</CardDescription>
        </CardHeader>
        <CardContent>
          {Object.entries(attributes).map(([attr, value]) => (
            <div key={attr} className="attribute-slider">
              <div className="attribute-label">
                <Label htmlFor={attr}>{attr}</Label>
                <span>{Math.round(value * 100)}%</span>
              </div>
              <Slider
                id={attr}
                value={[value * 100]}
                min={0}
                max={100}
                step={5}
                onValueChange={(val) => handleAttributeChange(attr, val)}
              />
            </div>
          ))}
        </CardContent>
        <CardFooter>
          <Button variant="outline" onClick={onCancel}>Cancel</Button>
          <Button onClick={() => onSave(personality, attributes)}>Save Changes</Button>
        </CardFooter>
      </Card>
    </div>
  );
};

const ChatBubble = ({ player, message, isDead, personality }) => {
  const getInitial = () => {
    if (!personality) return player[0];
    return personality[0];
  };
  
  return (
    <div className={`chat-bubble ${isDead ? 'dead' : ''}`}>
      <div className={`avatar avatar-${personality || 'Unknown'}`}>
        {getInitial()}
      </div>
      <div className="message">
        <div className="player-name">{player}</div>
        <div className="message-text">{message}</div>
      </div>
    </div>
  );
};

// Add this function to categorize events
const getCategoryForEvent = (event) => {
  if (event.includes('killed') || event.includes('dead')) return 'event-kill';
  if (event.includes('Dawn')) return 'event-dawn';
  if (event.includes('Detective')) return 'event-detective';
  if (event.includes('Doctor')) return 'event-doctor';
  return 'event-game';
};

const NightActionAnimation = ({ action, target, complete, stage }) => {
  const [animationVisible, setAnimationVisible] = useState(true);
  const [targetVisible, setTargetVisible] = useState(false);
  const [fallbackActive, setFallbackActive] = useState(false);
  const animationRef = useRef(null);
  
  useEffect(() => {
    // Reset states when action changes
    setAnimationVisible(true);
    setTargetVisible(false);
    
    // Handle GIF loading error
    if (animationRef.current) {
      const img = new Image();
      img.onload = () => setFallbackActive(false);
      img.onerror = () => setFallbackActive(true);
      img.src = '/static/thinking.gif';
    }
    
    // Show target after delay
    const targetTimer = setTimeout(() => {
      if (target) {
        setTargetVisible(true);
      }
    }, 2000);
    
    // Complete animation after delay
    const completeTimer = setTimeout(() => {
      setAnimationVisible(false);
      complete();
    }, 4000);
    
    return () => {
      clearTimeout(targetTimer);
      clearTimeout(completeTimer);
    };
  }, [action, target, complete]);
  
  // Get appropriate title based on action and stage
  const getActionTitle = () => {
    if (action === 'mafia') {
      return stage === 'start' ? 'The Mafia is choosing their target...' : 'The Mafia has chosen!';
    } else if (action === 'detective') {
      return stage === 'start' ? 'The Detective is investigating...' : 'The Detective has investigated!';
    } else if (action === 'doctor') {
      return stage === 'start' ? 'The Doctor is protecting someone...' : 'The Doctor has protected!';
    }
    return '';
  };

  return (
    <div className="animation-container">
      <div className="action-title">
        {getActionTitle()}
      </div>
      
      {animationVisible ? (
        <div ref={animationRef} className={fallbackActive ? "fallback-animation" : "thinking-animation"}></div>
      ) : null}
      
      {target && (
        <div className={`target-announcement ${targetVisible ? 'visible' : ''}`}>
          <div className="target text-2xl font-bold">
            Selected: {target}
          </div>
        </div>
      )}
    </div>
  );
};

const GameSetup = ({ onStartGame }) => {
  const [personalities, setPersonalities] = useState({});
  const [selectedPersonalities, setSelectedPersonalities] = useState([]);
  const [customizing, setCustomizing] = useState(null);
  const [customPersonality, setCustomPersonality] = useState({ name: '', attributes: {} });
  const [showCustomForm, setShowCustomForm] = useState(false);
  
  const personalityImages = {
    Diplomat: "/static/personalities/diplomat.png",
    Sheriff: "/static/personalities/sheriff.png",
    Conspirator: "/static/personalities/conspirator.jpg",
    Jester: "/static/personalities/jester.jpg",
    Mastermind: "/static/personalities/mastermind.jpg",
    Empath: "/static/personalities/empath.png",
    Wildcard: "/static/personalities/wildcard.jpg",
    Veteran: "/static/personalities/veteran.png",
    Innocent: "/static/personalities/innocent.jpg",
    Manipulator: "/static/personalities/manipulator.jpg"
  };

  useEffect(() => {
    const loadPersonalities = async () => {
      const data = await fetchPersonalities();
      setPersonalities(data);
    };
    
    loadPersonalities();
  }, []);

  useEffect(() => {
    // Debug image paths
    const checkImagePaths = async () => {
      if (Object.keys(personalities).length === 0) return;
      
      console.group('Debugging personality images:');
      
      // Check for "/static" folder existence
      try {
        const staticResponse = await fetch('/static');
        console.log('Static folder response:', staticResponse.status, staticResponse.ok);
      } catch (error) {
        console.error('Error checking static folder:', error);
      }
      
      // Try to fetch each image
      const personalityNames = Object.keys(personalities);
      for (const name of personalityNames) {
        const imagePath = `/static/personalities/${name.toLowerCase()}.jpg`;
        const pngPath = `/static/personalities/${name.toLowerCase()}.png`;
        
        console.log(`Checking ${name} image...`);
        
        try {
          const jpgResponse = await fetch(imagePath);
          console.log(`${name} JPG:`, jpgResponse.status, jpgResponse.ok);
        } catch (error) {
          console.error(`Error fetching ${name} JPG:`, error);
        }
        
        try {
          const pngResponse = await fetch(pngPath);
          console.log(`${name} PNG:`, pngResponse.status, pngResponse.ok);
        } catch (error) {
          console.error(`Error fetching ${name} PNG:`, error);
        }
      }
      
      // Check default image
      try {
        const defaultResponse = await fetch('/static/personalities/default.jpg');
        console.log('Default image:', defaultResponse.status, defaultResponse.ok);
      } catch (error) {
        console.error('Error fetching default image:', error);
      }
      
      console.groupEnd();
    };
    
    checkImagePaths();
  }, [personalities]);

  const handleSelectPersonality = (personality) => {
    console.log('Clicked personality:', personality);
    console.log('Current selected:', selectedPersonalities);
    
    if (selectedPersonalities.includes(personality)) {
      setSelectedPersonalities(prev => {
        const updated = prev.filter(p => p !== personality);
        console.log('Updated (removed):', updated);
        return updated;
      });
    } else if (selectedPersonalities.length < 6) {
      setSelectedPersonalities(prev => {
        const updated = [...prev, personality];
        console.log('Updated (added):', updated);
        return updated;
      });
    }
  };
  

  
  const handleCustomizePersonality = (personality) => {
    setCustomizing(personality);
  };
  
  const handleSaveCustomization = (personality, attributes) => {
    setPersonalities(prev => ({
      ...prev,
      [personality]: {
        ...prev[personality],
        attributes
      }
    }));
    setCustomizing(null);
  };
  
  const handleAddCustomPersonality = () => {
    if (customPersonality.name.trim() === '') return;
    
    setPersonalities(prev => ({
      ...prev,
      [customPersonality.name]: {
        description: "Custom personality",
        attributes: customPersonality.attributes,
        prompt_style: `You have a unique personality as ${customPersonality.name}.`
      }
    }));
    
    setCustomPersonality({ name: '', attributes: {} });
    setShowCustomForm(false);
  };

    // Remove a personality by clicking on its avatar
    const handleRemovePersonality = (personality, e) => {
      e.stopPropagation(); // Prevent other handlers from firing
      setSelectedPersonalities(prev => prev.filter(p => p !== personality));
    };
  
  const handleStartGameClick = async (personalities) => {

      await onStartGame(personalities);
    
  };
  
  return (
    <div className="container">
      <Card className="setup-card">
        <CardHeader>
          <CardTitle>Mafia Game Setup</CardTitle>
          <CardDescription>Select 6 personalities for your game</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="setup-header">
            <div className="selection-info">
              <div className="selection-count">
                Selected: {selectedPersonalities.length}/6
              </div>
              
              {/* Selected personalities avatars */}
              <div className="selected-personalities">
                {selectedPersonalities.map(personality => (
                  <img 
                    key={personality}
                    src={personalityImages[personality] || "/static/personalities/default.jpg"}
                    alt={personality}
                    title={`Remove ${personality}`}
                    className="selected-personality-avatar"
                    onClick={(e) => handleRemovePersonality(personality, e)}
                    onError={(e) => {
                      e.target.onerror = null;
                      e.target.src = "/static/personalities/default.jpg";
                    }}
                  />
                ))}
              </div>
            </div>
            
            <Button 
              disabled={selectedPersonalities.length !== 6} 
              onClick={() => handleStartGameClick(selectedPersonalities)}
              loadingText="Starting game..."
            >
              Start Game
            </Button>
          </div>
          
          <div className="custom-button">
            <Button variant="outline" onClick={() => setShowCustomForm(true)}>
              Create Custom Personality
            </Button>
          </div>
          
          {showCustomForm && (
            <Card className="custom-form">
              <CardHeader>
                <CardTitle>Create Custom Personality</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="form-group">
                  <Label htmlFor="name">Name</Label>
                  <Input 
                    id="name" 
                    value={customPersonality.name} 
                    onChange={(e) => setCustomPersonality(prev => ({ ...prev, name: e.target.value }))}
                  />
                </div>
                
                {['truthfulness', 'aggressiveness', 'suspicion', 'persuasiveness', 'loyalty'].map(attr => (
                  <div key={attr} className="attribute-slider">
                    <div className="attribute-label">
                      <Label htmlFor={attr}>{attr}</Label>
                      <span>{customPersonality.attributes[attr] ? Math.round(customPersonality.attributes[attr] * 100) : 50}%</span>
                    </div>
                    <Slider
                      id={attr}
                      value={[customPersonality.attributes[attr] ? customPersonality.attributes[attr] * 100 : 50]}
                      min={0}
                      max={100}
                      step={5}
                      onValueChange={(val) => setCustomPersonality(prev => ({ 
                        ...prev, 
                        attributes: { ...prev.attributes, [attr]: val[0] / 100 } 
                      }))}
                    />
                  </div>
                ))}
              </CardContent>
              <CardFooter>
                <Button variant="outline" onClick={() => setShowCustomForm(false)}>Cancel</Button>
                <Button onClick={handleAddCustomPersonality}>Add Personality</Button>
              </CardFooter>
            </Card>
          )}
          
          <div className="personalities-grid">
            {Object.entries(personalities).map(([personality, details]) => (
              <PersonalityCard
                key={personality}
                personality={personality}
                details={details}
                selected={selectedPersonalities.includes(personality)}
                onSelect={() => handleSelectPersonality(personality)}
                onCustomize={handleCustomizePersonality}
              />
            ))}
          </div>
        </CardContent>
      </Card>
      
      {customizing && (
        <CustomizePersonalityModal
          personality={customizing}
          details={personalities[customizing]}
          onSave={handleSaveCustomization}
          onCancel={() => setCustomizing(null)}
        />
      )}
    </div>
  );
};


const GamePlay = ({ gameId }) => 
{
  const [gameState, setGameState] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [nightAction, setNightAction] = useState(null);
  const [nightTarget, setNightTarget] = useState(null);
  const [discussion, setDiscussion] = useState([]);
  const [animation, setAnimation] = useState(null);
  const [showRoles, setShowRoles] = useState(true);
  const [animationStage, setAnimationStage] = useState('start');
  const [voteResults, setVoteResults] = useState({});
  const [discussionInProgress, setDiscussionInProgress] = useState(false);
  const [deadPlayers, setDeadPlayers] = useState([]);
  const [newlyDead, setNewlyDead] = useState([]);
  
  const [debug, setDebug] = useState({
    apiKeyStatus: "Not checked",
    agentStatus: {},
    initialized: false
  });

  // Refs
  const eventsContainerRef = useRef(null);
  const chatContainerRef = useRef(null);
  const discussionPollRef = useRef(null);
  
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [discussion]);

  useEffect(() => {
    if (eventsContainerRef.current) {
      eventsContainerRef.current.scrollTop = eventsContainerRef.current.scrollHeight;
    }
  }, [gameState?.events]);
  
  // Update GamePlay component's loadGameState function
  const loadGameState = async () => {
    setLoading(true);
    try {
      const state = await getGameState(gameId);
      setGameState(state);
      
      // Debug agent initialization if not done yet
      if (!debug.initialized) {
        // Check API keys
        try {
          const response = await fetch(`${API_URL}/debug_api_keys`);
          const keyStatus = await response.json();
          setDebug(prev => ({
            ...prev,
            apiKeyStatus: keyStatus.status === "ok" ? "Valid" : "Invalid or missing",
            initialized: true
          }));
        } catch (err) {
          setDebug(prev => ({
            ...prev,
            apiKeyStatus: "Error checking API keys",
            initialized: true
          }));
        }
        
        // Log agent status
        if (state.players) {
          const agentStatuses = {};
          state.players.forEach(player => {
            agentStatuses[player.name] = {
              personality: player.personality,
              role: player.role || "Unknown",
              status: "Initialized"
            };
          });
          setDebug(prev => ({
            ...prev,
            agentStatus: agentStatuses
          }));
        }
      }
    } catch (err) {
      setError('Failed to load game state');
      console.error(err);
    }
    setLoading(false);
  };
  
  // Track newly dead players
// Update with proper dependency array
useEffect(() => {
  if (gameState && gameState.players) {
    const currentDead = gameState.players.filter(p => !p.alive).map(p => p.name);
    
    // Find newly dead players (dead now but weren't before)
    const newly = currentDead.filter(name => !deadPlayers.includes(name));
    if (newly.length > 0) {
      setNewlyDead(newly);
      
      // Reset newly dead after animation
      setTimeout(() => {
        setNewlyDead([]);
      }, 2000);
    }
    
    setDeadPlayers(currentDead);
  }
}, [gameState]); // Only depend on gameState, not deadPlayers

// Also check the initial game state load useEffect:
useEffect(() => {
  loadGameState();
  // eslint-disable-next-line react-hooks/exhaustive-deps
}, [gameId]);
  
  // Clean up polling on unmount
  useEffect(() => {
    return () => {
      if (discussionPollRef.current) {
        clearInterval(discussionPollRef.current);
      }
    };
  }, []);
  
  // Check API response
  useEffect(() => {
    const fetchGameState = async () => {
      try {
        const response = await fetch(`${API_URL}/game_state/${gameId}`);
        const data = await response.json();
        console.log("Raw API Response:", data);
        console.log("Player data includes roles:", data.players.some(p => p.role));
      } catch (error) {
        console.error("Error fetching game state:", error);
      }
    };

    fetchGameState();
  }, [gameId]);
  
  const handleStartGame = async () => {
    try {
      await startGame(gameId);
      await loadGameState();
    } catch (err) {
      setError('Failed to start game');
      console.error(err);
    } 
  };


  
  const handleProcessNight = async () => {
    // Don't use the global loading overlay
    // setGlobalLoading({ show: true, message: "Processing night actions..." });
    
    // Just disable the button directly
    const nightButton = document.querySelector('.night-button');
    if (nightButton) {
      nightButton.disabled = true;
      nightButton.classList.add('button-loading');
    }
    
    try {
      // Process mafia action
      setAnimation('mafia');
      setAnimationStage('start');
      const mafiaResult = await processNight(gameId);
      setNightTarget(mafiaResult.actions.mafia_target);
      setAnimationStage('complete');
      
      // Wait for animation
      await new Promise(resolve => setTimeout(resolve, 5000));
      
      // Process detective action
      setAnimation('detective');
      setAnimationStage('start');
      setNightTarget(mafiaResult.actions.detective_target);
      setAnimationStage('complete');
      
      // Wait for animation
      await new Promise(resolve => setTimeout(resolve, 5000));
      
      // Process doctor action
      setAnimation('doctor');
      setAnimationStage('start');
      setNightTarget(mafiaResult.actions.doctor_target);
      setAnimationStage('complete');
      
      // Wait for animation
      await new Promise(resolve => setTimeout(resolve, 5000));
      
      setAnimation(null);
      setNightTarget(null);
      
      // Resolve night
      await resolveNight(gameId);
      await loadGameState();
    } catch (err) {
      setError('Failed to process night');
      console.error(err);
    } finally {
      // Don't use global loading here
      // setGlobalLoading({ show: false });
      
      // Re-enable the button directly
      if (nightButton) {
        nightButton.disabled = false;
        nightButton.classList.remove('button-loading');
      }
    }
  };
  
  const handleStartDiscussion = async () => {
    setDiscussionInProgress(true);
    
    const discussionButton = document.querySelector('.discussion-button');
    if (discussionButton) {
      discussionButton.disabled = true;
      discussionButton.classList.add('button-loading');
    }
    
    try {
      // First call start_discussion endpoint to change the game phase
      await startDiscussion(gameId);
      
      // Then call simulate_discussion to generate discussion content
      const result = await simulateDiscussion(gameId);
      console.log("Discussion simulation result:", result);
      
      // If we got discussion messages, update state immediately
      if (result.discussion) {
        setDiscussion(result.discussion);
      }
      
      // Start polling for any additional updates
      startPollingDiscussion();
      
      await loadGameState();
    } catch (err) {
      setError('Failed to conduct discussion');
      console.error(err);
      
      // Reset UI state on error
      setDiscussionInProgress(false);
      if (discussionButton) {
        discussionButton.disabled = false;
        discussionButton.classList.remove('button-loading');
      }
    }
    
  };
  
  // Function to poll for discussion updates
  const startPollingDiscussion = () => {
    console.log("Starting discussion polling...");
    
    // Clear any existing polling
    if (discussionPollRef.current) {
      clearInterval(discussionPollRef.current);
    }
    
    const pollInterval = setInterval(async () => {
      try {
        console.log("Polling for discussion updates...");
        const result = await fetch(`${API_URL}/discussion_status/${gameId}`);
        const data = await result.json();
        
        if (data.discussion && data.discussion.length > 0) {
          console.log("Received discussion update:", data.discussion.length, "messages");
          setDiscussion(data.discussion);
        } else {
          console.log("No discussion messages in response");
        }
        
        if (!data.in_progress) {
          console.log("Discussion complete, stopping polling");
          setDiscussionInProgress(false);
          clearInterval(discussionPollRef.current);
          
          // Re-enable the button
          const discussionButton = document.querySelector('.discussion-button');
          if (discussionButton) {
            discussionButton.disabled = false;
            discussionButton.classList.remove('button-loading');
          }
          
          // Final update to game state
          await loadGameState();
        }
      } catch (err) {
        console.error('Error polling discussion:', err);
      }
    }, 2000); // Check every 2 seconds
    
    // Store interval ID for cleanup
    discussionPollRef.current = pollInterval;
  };
  
  const handleProcessVoting = async () => {
    //setGlobalLoading({ show: true, message: "Processing votes..." });
    
    // Disable the button
    const votingButton = document.querySelector('.voting-button');
    if (votingButton) {
      votingButton.disabled = true;
      votingButton.classList.add('button-loading');
    }
    
    try {
      const result = await processVoting(gameId);
      setVoteResults(result.votes || {});
      await loadGameState();
    } catch (err) {
      setError('Failed to process voting');
      console.error(err);
    } finally {
      
      // Re-enable the button
      if (votingButton) {
        votingButton.disabled = false;
        votingButton.classList.remove('button-loading');
      }
    }
  };

  const VotingGraph = ({ votes, players }) => {
    if (!votes || Object.keys(votes).length === 0) return null;
  
    return (
      <div className="voting-graph">
        <h3 className="voting-title">Voting Results</h3>
        <div className="voting-container">
          <div className="voters-column">
            {players.map(player => (
              <div key={`voter-${player.name}`} className="voter-row">
                <div className={`player-node ${!player.alive ? 'player-dead' : ''}`}>
                  {player.name}
                </div>
                {votes[player.name] && (
                  <div className="vote-arrow">
                    ➡️
                  </div>
                )}
              </div>
            ))}
          </div>
          <div className="targets-column">
            {players.map(player => (
              <div key={`target-${player.name}`} className="target-row">
                <div className={`player-node ${!player.alive ? 'player-dead' : ''}`}>
                  {player.name}
                </div>
                <div className="vote-count">
                  {Object.values(votes).filter(target => target === player.name).length} votes
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };
  
  const handleResetGame = async () => {
    setLoading(true);
    
    try {
      await resetGame(gameId);
      setDiscussion([]);
      setNightAction(null);
      setNightTarget(null);
      await loadGameState();
    } catch (err) {
      setError('Failed to reset game');
      console.error(err);
    } 
     
    setLoading(false);
  };
  

  if (loading || !gameState) {
    return (
      <div className="container">
        <div className="loading">
          <div className="loading-spinner-large"></div>
          <p>Loading game state...</p>
        </div>
      </div>
    );
  }
  return (
    <div className="container">
      <div className="game-header">
        <div className="game-title">Mafia Game</div>
        <div className="game-phases">
          <Badge variant={gameState.phase === 'setup' ? 'default' : 'outline'}>Setup</Badge>
          <Badge variant={gameState.phase === 'night' ? 'default' : 'outline'}>Night</Badge>
          <Badge variant={gameState.phase === 'dawn' ? 'default' : 'outline'}>Dawn</Badge>
          <Badge variant={gameState.phase === 'discussion' ? 'default' : 'outline'}>Discussion</Badge>
          <Badge variant={gameState.phase === 'voting' ? 'default' : 'outline'}>Voting</Badge>
        </div>
        <div className="game-round">Round: {gameState.round || 0}</div>
      </div>
      
      {gameState.game_over && (
        <Alert className="game-over-alert">
          <Icon name="CheckCircle" />
          <AlertTitle>Game Over!</AlertTitle>
          <AlertDescription>The {gameState.winner} team wins!</AlertDescription>
        </Alert>
      )}
      
      <div className="game-dashboard">
  {/* Layout all three cards in horizontal row */}
  <div className="game-panels">
    {/* Players Card - reduced width */}
    <Card className="panel-card">
      <CardHeader>
        <CardTitle><Icon name="Users" /> Players</CardTitle>
      </CardHeader>
      <CardContent className="panel-content">
        {gameState.players?.map((player) => (
          <div key={player.name} className={`player-row ${!player.alive ? 'dead' : ''}`}>
            <div className="player-info">
              {!player.alive && <Icon name="Skull" />}
              <span>{player.name}</span>
              {player.role && <span className={`player-role role-${player.role.toLowerCase()}`}>{player.role}</span>}
            </div>
            <Badge>{player.personality}</Badge>
          </div>
        ))}
      </CardContent>
    </Card>

    {/* Game Events Card - reduced width */}
    <Card className="panel-card">
      <CardHeader>
        <CardTitle><Icon name="AlertCircle" /> Game Events</CardTitle>
      </CardHeader>
      <CardContent className="panel-content">
        <ul className="events-list" ref={eventsContainerRef}>
          {gameState.events?.map((event, i) => {
            let eventClass = 'event-game';
            let eventIcon = null;
            
            if (event.includes('Night') && event.includes('begins')) {
              eventClass = 'event-phase';
              eventIcon = '🌙';
            } else if (event.includes('Dawn of Day')) {
              eventClass = 'event-phase';
              eventIcon = '☀️';
            } else if (event.includes('Detective') && event.includes('failed')) {
              eventClass = 'event-detective-fail';
              eventIcon = '🔍❌';
            } else if (event.includes('Detective') && !event.includes('failed')) {
              eventClass = 'event-detective-success';
              eventIcon = '🔍✓';
            } else if (event.includes('killed') || event.includes('dead')) {
              eventClass = 'event-murder';
              eventIcon = '☠️';
            } else if (event.includes('Doctor') && event.includes('saved')) {
              eventClass = 'event-doctor-save';
              eventIcon = '💉';
            } else if (event.includes('exiled')) {
              eventClass = 'event-exile';
              eventIcon = '🚫';
            } else if (event.includes('Game started')) {
              eventClass = 'event-game';
              eventIcon = '🎮';
            }
            
            return (
              <li key={i} className={`event-item ${eventClass}`}>
                {eventIcon && <span className="event-icon">{eventIcon}</span>}
                {event}
              </li>
            );
          })}
        </ul>
      </CardContent>
    </Card>

    {/* Voting Results Card */}
    {Object.keys(voteResults).length > 0 ? (
      <Card className="panel-card">
        <CardHeader>
          <CardTitle><Icon name="Vote" /> Voting Results</CardTitle>
        </CardHeader>
        <CardContent className="panel-content">
          <div className="voting-table">
            <div className="voting-header">
              <div className="vote-col">Votes</div>
              <div className="player-col">Player</div>
              <div className="voted-for-col">Voted For</div>
            </div>
            {gameState.players.map(player => (
              <div key={player.name} className="voting-row">
                <div className="vote-col">{Object.values(voteResults).filter(v => v === player.name).length}</div>
                <div className="player-col">{player.name}</div>
                <div className="voted-for-col">{voteResults[player.name] || "-"}</div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    ) : (
      <Card className="panel-card">
        <CardHeader>
          <CardTitle><Icon name="Vote" />Voting</CardTitle>
        </CardHeader>
        <CardContent className="panel-content">
          <div className="chat-container" ref={chatContainerRef}>
            
          </div>
        </CardContent>
      </Card>
    )}
  </div>
</div>
      
      {animation && (
  <Card>
    <CardContent>
      <NightActionAnimation 
        action={animation} 
        target={nightTarget}
        stage={animationStage}
        complete={() => {}}
      />
    </CardContent>
  </Card>
)}
      
      {gameState.phase === 'setup' && (
        <Card>
          <CardContent>
            <div className="setup-prompt">
              <p>All players have been assigned personalities. Ready to begin?</p>
              <Button 
                onClick={handleStartGame}
                isLoading={false}
                loadingText="Starting game..."
              >
                Begin Game
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
      
      {gameState.phase === 'night' && !animation && (
        <Card>
  <CardHeader>
    <CardTitle>
      <Icon name="Moon" /> Night Phase
    </CardTitle>
  </CardHeader>
  <CardContent>
    <div className="night-prompt">
      <p>Night has fallen. The Mafia, Detective, and Doctor will make their moves...</p>
      <Button className="night-button" onClick={handleProcessNight}>
        Process Night Actions
      </Button>
    </div>
  </CardContent>
</Card>
      )}
      
      {gameState.phase === 'dawn' && (
 <Card>
 <CardHeader>
   <CardTitle>
     <Icon name="Sun" /> Dawn Announcement
   </CardTitle>
 </CardHeader>
 <CardContent>
   <div className="dawn-prompt">
     <p>The sun rises on a new day. Time for the town to discuss what happened.</p>
     <Button 
  className="discussion-button" 
  onClick={handleStartDiscussion}
  isLoading={false}
  loadingText="Discussion ongoing..."
>
  Begin Discussion
</Button>
   </div>
 </CardContent>
</Card>
      )}
      
      {(gameState.phase === 'discussion' || discussion.length > 0) && (
        <Card>
  <CardHeader>
    <CardTitle>
      <Icon name="MessageSquare" /> Town Discussion
    </CardTitle>
  </CardHeader>
  <CardContent>

  {discussionInProgress && (
  <div className="discussion-status">
    <div className="loading-spinner"></div>
    <p>Discussion in progress...</p>
  </div>
)}
{/* Replace the discussion rendering code inside the chat-container in your JSX */}
<div className="chat-container" ref={chatContainerRef}>
  {discussion.length === 0 && discussionInProgress ? (
    <div className="discussion-empty-state">
      <p>Waiting for players to begin discussion...</p>
    </div>
  ) : (
    discussion.map((line, i) => {
      if (!line || line.trim() === '') {
        return null;
      }
      
      if (line.startsWith('---')) {
        return <div key={i} className="discussion-section">{line}</div>;
      }
      
      const colonIndex = line.indexOf(':');
      if (colonIndex > 0) {
        const playerName = line.substring(0, colonIndex).trim();
        const message = line.substring(colonIndex + 1).trim();
        const player = gameState.players?.find(p => p.name === playerName);
        const isDead = player && !player.alive;
        
        return <ChatBubble 
          key={i} 
          player={playerName} 
          message={message} 
          isDead={isDead} 
          personality={player?.personality}
        />;
      }
      
      return <div key={i} className="system-message">{line}</div>;
    })
  )}
  
  {discussionInProgress && (
    <div className="discussion-status">
      <div className="loading-spinner"></div>
      <p>Discussion in progress...</p>
    </div>
  )}
</div>
  </CardContent>
  <CardFooter>
    {gameState.phase === 'discussion' && (
      <Button 
  className="voting-button" 
  onClick={handleProcessVoting}
  isLoading={false}
  loadingText="Processing votes..."
>
  Proceed to Voting
</Button>
    )}
  </CardFooter>
</Card>

      )}
      
      {gameState.game_over && (
        <div className="game-over-actions">
          <Button size="lg" onClick={handleResetGame}>Play Again</Button>
        </div>
      )}
    </div>
  );

};


const App = () => {
  const [gameId, setGameId] = useState(null);
  const [gameStarted, setGameStarted] = useState(false);
  
  const handleStartGame = async (personalities) => {
    try {
      const result = await createGame(personalities);
      if (result.game_id) {
        setGameId(result.game_id);
        setGameStarted(true);
      } else {
        console.error("Failed to create game:", result);
      }
    } catch (err) {
      console.error('Error starting game:', err);
    }
  };

  

  return (
    <div className="app">
      <header className="app-header">
        <div className="container">
          <h1>AI Mafia Game</h1>
        </div>
      </header>
      
      <main className="app-main">
        {!gameStarted ? (
          <GameSetup onStartGame={handleStartGame} />
        ) : (
          <GamePlay gameId={gameId} />
        )}
      </main>
      
      <footer className="app-footer">
        <div className="container">
          <p>&copy; 2025 AI Mafia Game</p>
        </div>
      </footer>
    </div>
  );
};

// Wrap the entire app with LoadingProvider
const AppWithLoading = () => {
  return (
    <LoadingProvider>
      <App />
    </LoadingProvider>
  );
};

export default AppWithLoading;