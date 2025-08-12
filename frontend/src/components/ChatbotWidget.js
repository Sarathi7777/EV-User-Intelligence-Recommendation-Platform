import React, { useState, useRef, useEffect } from 'react';
import './ChatbotWidget.css';
import envConfig from '../env.config.js';

const ChatbotWidget = ({ isOpen, onToggle, user }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: "Hi there! I'm your EV Assistant. I can help you find charging stations, get recommendations, and answer questions about electric vehicles. How can I assist you today? 🚗⚡",
      timestamp: new Date(),
      quickReplies: [
        { text: "Find charging stations", action: "find_stations" },
        { text: "Get recommendations", action: "get_recommendations" },
        { text: "EV tips", action: "ev_tips" }
      ]
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setLoading] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleQuickReply = async (action) => {
    let botMessage = '';
    let quickReplies = [];
    
    switch (action) {
      case 'find_stations':
        botMessage = "Great! I can help you find charging stations. What's your current location or where are you planning to charge? 📍\n\nYou can tell me:\n• City name (e.g., Coimbatore, Chennai, Bangalore)\n• Specific area or landmark\n• Highway or route you're traveling";
        quickReplies = [
          { text: "I'm in Coimbatore", action: "coimbatore_location" },
          { text: "I'm traveling on NH47", action: "highway_route" },
          { text: "Show me all nearby", action: "nearby_stations" }
        ];
        break;
      case 'get_recommendations':
        botMessage = "I'd love to help with recommendations! 🤔\n\nWhat type of recommendations are you looking for?\n• Best charging stations for your route\n• EV models that fit your needs\n• Charging strategies for your lifestyle\n• Cost-saving tips";
        quickReplies = [
          { text: "Charging station recommendations", action: "station_recommendations" },
          { text: "EV model suggestions", action: "ev_models" },
          { text: "Charging strategies", action: "charging_strategies" }
        ];
        break;
      case 'ev_tips':
        botMessage = "Here are some helpful EV tips:\n\n🔋 **Battery Care:**\n• Charge when battery is 20-80% for best longevity\n• Avoid extreme temperatures when charging\n• Use Level 2 charging for daily use\n\n🚗 **Range Optimization:**\n• Plan routes with charging stops\n• Use regenerative braking\n• Keep tires properly inflated\n\nWould you like more specific tips on any of these topics?";
        quickReplies = [
          { text: "Battery maintenance tips", action: "battery_tips" },
          { text: "Range optimization", action: "range_tips" },
          { text: "Charging best practices", action: "charging_tips" }
        ];
        break;
      case 'coimbatore_location':
        botMessage = "Perfect! Coimbatore has several great charging options:\n\n📍 **Popular charging areas:**\n• Race Course - Multiple fast chargers\n• RS Puram - Shopping center chargers\n• Peelamedu - University area stations\n• Saibaba Colony - Residential area options\n\n🔋 **Charging networks:**\n• Tata Power - Reliable and widespread\n• EESL - Government-operated stations\n• Private stations - Hotels and malls\n\nWhat area of Coimbatore are you in, or where are you heading?";
        break;
      case 'highway_route':
        botMessage = "Great choice! Highway charging is essential for long trips. 🛣️\n\n**NH47 (Salem to Coimbatore):**\n• Salem - Multiple fast chargers\n• Erode - Rest area with charging\n• Coimbatore - Multiple options\n\n**Tips for highway charging:**\n• Plan stops every 150-200 km\n• Have backup charging apps ready\n• Check station availability before leaving\n\nWhat's your starting point and destination?";
        break;
      case 'nearby_stations':
        botMessage = "I'd love to show you nearby stations! 📍\n\nTo find the closest charging stations, I need to know:\n• Your current location (city/area)\n• How far you're willing to travel\n• What charging speed you prefer\n\nYou can also use our interactive map feature to see all stations in your area!";
        break;
      case 'station_recommendations':
        botMessage = "Excellent! For the best charging station recommendations, I need to understand your needs:\n\n🚗 **Your EV details:**\n• What connector type does it use?\n• How fast can it charge?\n• What's your typical charging pattern?\n\n📍 **Your location and routes:**\n• Where do you usually drive?\n• Do you take long trips often?\n• Are you looking for home/work charging or public stations?";
        break;
      case 'ev_models':
        botMessage = "Great question! There are many excellent EV options available. 🚗⚡\n\n**Popular EV categories:**\n• **Compact:** Tata Nexon EV, MG ZS EV\n• **Sedan:** Hyundai Kona, MG ZS EV\n• **SUV:** Tata Nexon EV Max, MG ZS EV\n• **Luxury:** Mercedes EQC, Audi e-tron\n\n**Factors to consider:**\n• Budget range\n• Daily driving distance\n• Charging access at home/work\n• Family size and space needs\n\nWhat's your budget and primary use case?";
        break;
      case 'charging_strategies':
        botMessage = "Smart thinking! A good charging strategy can save you time and money. 💡\n\n**Home charging strategy:**\n• Install Level 2 charger for overnight charging\n• Use smart scheduling to charge during off-peak hours\n• Monitor your daily usage patterns\n\n**Public charging strategy:**\n• Plan routes with charging stops\n• Have multiple charging apps ready\n• Consider subscription plans for frequent users\n\n**Trip planning strategy:**\n• Map out charging stops in advance\n• Have backup charging options\n• Consider weather and traffic conditions\n\nWhat's your current charging setup?";
        break;
      case 'battery_tips':
        botMessage = "Battery care is crucial for EV longevity! 🔋\n\n**Daily battery care:**\n• Keep charge between 20-80% for daily use\n• Avoid charging to 100% unless needed for long trips\n• Don't let battery go below 10% regularly\n\n**Temperature management:**\n• Park in shade during hot weather\n• Pre-condition battery before charging in cold weather\n• Avoid charging in extreme temperatures\n\n**Long-term maintenance:**\n• Update your EV software regularly\n• Follow manufacturer's maintenance schedule\n• Monitor battery health indicators\n\nWould you like specific tips for your EV model?";
        break;
      case 'range_tips':
        botMessage = "Maximizing range is key to worry-free EV driving! 📊\n\n**Driving techniques:**\n• Accelerate smoothly and gradually\n• Use regenerative braking effectively\n• Maintain steady speed on highways\n• Coast to stops instead of braking hard\n\n**Route planning:**\n• Choose routes with less elevation change\n• Avoid heavy traffic areas\n• Plan for weather conditions\n• Use eco-mode when available\n\n**Vehicle maintenance:**\n• Keep tires properly inflated\n• Reduce vehicle weight\n• Ensure proper wheel alignment\n• Regular maintenance checks\n\nWhat's your typical driving pattern?";
        break;
      case 'charging_tips':
        botMessage = "Charging smartly makes all the difference! ⚡\n\n**Charging timing:**\n• Charge during off-peak hours for lower costs\n• Use smart charging features if available\n• Plan charging around your daily schedule\n\n**Charging speed selection:**\n• Level 1 (slow): Overnight home charging\n• Level 2 (medium): Daily home/work charging\n• DC Fast: Quick top-ups during trips\n\n**Charging etiquette:**\n• Don't overstay at fast chargers\n• Move your vehicle when fully charged\n• Be considerate of other EV drivers\n• Report broken chargers to operators\n\nWhat charging questions do you have?";
        break;
      default:
        botMessage = "I'm here to help! What would you like to know about electric vehicles or charging?";
    }

    const newMessage = {
      id: Date.now(),
      type: 'bot',
      content: botMessage,
      timestamp: new Date(),
      quickReplies: quickReplies.length > 0 ? quickReplies : undefined
    };

    setMessages(prev => [...prev, newMessage]);
  };

  const callOpenRouterDirectly = async (message, conversationHistory) => {
    const openrouterApiKey = envConfig.OPENROUTER_API_KEY;
    
    if (!openrouterApiKey) {
      throw new Error('OpenRouter API key not configured. Please set REACT_APP_OPENROUTER_API_KEY environment variable.');
    }

    console.log('Attempting direct OpenRouter API call with key:', openrouterApiKey.substring(0, 20) + '...');

    const openrouterUrl = "https://openrouter.ai/api/v1/chat/completions";
    
    const systemPrompt = `You are an EV Assistant, a helpful AI specializing in electric vehicles and charging infrastructure. 
    Help users with EV-related questions, charging station information, and recommendations. 
    Be conversational, friendly, and provide practical, actionable advice.`;
    
    const messages = [
      { role: "system", content: systemPrompt },
      ...conversationHistory.map(msg => ({
        role: msg.role,
        content: msg.content
      })),
      { role: "user", content: message }
    ];

    const payload = {
      model: "deepseek/deepseek-r1:free",
      messages: messages,
      max_tokens: 1000,
      temperature: 0.7
    };

    console.log('Sending payload to OpenRouter:', payload);

    const response = await fetch(openrouterUrl, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${openrouterApiKey}`,
        'Content-Type': 'application/json',
        'HTTP-Referer': window.location.origin,
        'X-Title': 'EV User Intelligence Platform'
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('OpenRouter API error:', response.status, errorText);
      throw new Error(`OpenRouter API error: ${response.status} - ${errorText}`);
    }

    const data = await response.json();
    console.log('OpenRouter API response:', data);
    return data.choices[0].message.content;
  };

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputMessage; // Store the input before clearing
    setInputMessage('');
    setLoading(true);

    try {
      // First try the backend API
      console.log('Attempting backend API call to /api/chatbot/chat');
      const response = await fetch('/api/chatbot/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: currentInput,
          user_id: user?.id || 'anonymous',
          conversation_history: messages.slice(-5).map(m => ({
            role: m.type === 'user' ? 'user' : 'assistant',
            content: m.content
          }))
        })
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Backend API response:', data);
        const botMessage = {
          id: Date.now() + 1,
          type: 'bot',
          content: data.response,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, botMessage]);
      } else {
        // If backend fails, try direct OpenRouter API call
        const errorData = await response.json().catch(() => ({}));
        console.error('Backend API failed:', response.status, errorData);
        console.log('Backend API failed, trying direct OpenRouter API call...');
        
        try {
          const conversationHistory = messages.slice(-5).map(m => ({
            role: m.type === 'user' ? 'user' : 'assistant',
            content: m.content
          }));
          
          const aiResponse = await callOpenRouterDirectly(currentInput, conversationHistory);
          
          const botMessage = {
            id: Date.now() + 1,
            type: 'bot',
            content: aiResponse,
            timestamp: new Date()
          };
          setMessages(prev => [...prev, botMessage]);
        } catch (openrouterError) {
          console.error('OpenRouter API also failed:', openrouterError);
          throw openrouterError; // Re-throw to fall back to static responses
        }
      }
    } catch (error) {
      console.error('All API calls failed, falling back to static responses:', error);
      
      // Try to provide a helpful response based on the user's input
      let helpfulResponse = "";
      const userInput = currentInput.toLowerCase();
      
      if (userInput.includes('coimbatore') || userInput.includes('location') || userInput.includes('where')) {
        helpfulResponse = "Great! Coimbatore is a beautiful city in Tamil Nadu. For charging stations in Coimbatore, I recommend checking:\n\n📍 **Popular areas with charging stations:**\n• Race Course area\n• RS Puram\n• Peelamedu\n• Saibaba Colony\n\n🔋 **Charging networks available:**\n• Tata Power\n• EESL (Energy Efficiency Services Limited)\n• Private stations\n\n💡 **Tip:** Use our station search feature to find real-time availability and plan your charging stops! Would you like me to help you with anything specific about EV charging in Coimbatore?";
      } else if (userInput.includes('charging') || userInput.includes('station')) {
        helpfulResponse = "I'd be happy to help you find charging stations! To give you the best recommendations, could you tell me:\n\n📍 **Your current location or destination?**\n🔋 **What type of connector your EV uses?** (Type 2, CCS, CHAdeMO, etc.)\n⚡ **How fast you need to charge?** (Level 1, Level 2, or DC Fast)\n\nThis will help you provide more specific and useful information!";
      } else if (userInput.includes('ev') || userInput.includes('electric') || userInput.includes('car')) {
        helpfulResponse = "Electric vehicles are fantastic! 🚗⚡ Here are some key benefits:\n\n🌱 **Environmental:** Zero emissions, cleaner air\n💰 **Cost savings:** Lower fuel and maintenance costs\n🔋 **Technology:** Advanced features and smart connectivity\n\nWhat specific aspect of EVs would you like to learn more about? Charging, maintenance, models, or something else?";
      } else if (userInput.includes('battery') || userInput.includes('range')) {
        helpfulResponse = "Great question about EV batteries! 🔋 Here are some key points:\n\n📊 **Range factors:**\n• Battery capacity (kWh)\n• Driving conditions and speed\n• Weather and temperature\n• Use of climate control\n\n💡 **Tips to maximize range:**\n• Drive smoothly and avoid rapid acceleration\n• Use regenerative braking\n• Keep tires properly inflated\n• Plan routes with charging stops\n\nWould you like specific tips for your EV model or charging strategy?";
      } else {
        helpfulResponse = "I'm here to help with all things EV! 🚗⚡ While I'm having some technical difficulties with my AI brain right now, I can still assist you with:\n\n• Finding charging stations\n• EV tips and best practices\n• Understanding EV technology\n• Cost and environmental benefits\n\nWhat would you like to know about electric vehicles?";
      }

      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: helpfulResponse,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  if (!isOpen) return null;

  return (
    <div className={`chatbot-widget ${isMinimized ? 'minimized' : ''}`}>
      {/* Header */}
      <div className="chatbot-header">
        <div className="chatbot-avatar">
          <img src="/api/chatbot/avatar" alt="EV Assistant" onError={(e) => {
            e.target.style.display = 'none';
            e.target.nextSibling.style.display = 'block';
          }} />
          <div className="avatar-fallback">⚡</div>
        </div>
        <div className="chatbot-info">
          <div className="chatbot-name">Chat with EV Assistant</div>
          <div className="chatbot-status">We're online</div>
        </div>
        <div className="chatbot-actions">
          <button 
            className="chatbot-settings"
            onClick={() => console.log('Settings clicked')}
            title="Settings"
          >
            ⋯
          </button>
          <button 
            className="chatbot-minimize"
            onClick={() => setIsMinimized(!isMinimized)}
            title={isMinimized ? "Expand" : "Minimize"}
          >
            {isMinimized ? '↑' : '↓'}
          </button>
        </div>
      </div>

      {/* Chat Area */}
      <div className="chatbot-messages">
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.type}`}>
            <div className="message-content">
              {message.content}
            </div>
            <div className="message-timestamp">
              {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
            {message.quickReplies && message.type === 'bot' && (
              <div className="quick-replies">
                {message.quickReplies.map((reply, index) => (
                  <button
                    key={index}
                    className="quick-reply-btn"
                    onClick={() => handleQuickReply(reply.action)}
                  >
                    {reply.text}
                  </button>
                ))}
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="message bot">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="chatbot-input">
        <button className="chatbot-emoji" title="Add emoji">
          😊
        </button>
        <button className="chatbot-attachment" title="Attach file">
          📎
        </button>
        <input
          ref={inputRef}
          type="text"
          placeholder="Enter your message..."
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={isLoading}
        />
        <button 
          className="chatbot-send"
          onClick={sendMessage}
          disabled={!inputMessage.trim() || isLoading}
          title="Send message"
        >
          ✈️
        </button>
      </div>
    </div>
  );
};

export default ChatbotWidget;
