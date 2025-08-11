# AI Assistant Chatbot Implementation

## Overview
This document describes the implementation of an AI-powered chatbot widget for the EV User Intelligence Recommendation Platform. The chatbot provides intelligent assistance for electric vehicle-related queries, charging station information, and EV best practices.

## Features

### 🎯 Core Functionality
- **Intelligent EV Assistance**: Specialized knowledge in electric vehicles, charging infrastructure, and sustainability
- **Context-Aware Responses**: Adapts responses based on user experience level and conversation context
- **Quick Reply Buttons**: Pre-defined response options for common queries
- **Real-time Chat**: Live conversation with AI-powered responses
- **Responsive Design**: Mobile-friendly interface that works on all devices

### 🎨 User Interface
- **Floating Chat Button**: Always accessible floating button with pulse animation
- **Expandable Widget**: Minimizable chat interface that doesn't interfere with main content
- **Modern Design**: Clean, professional interface matching the platform's aesthetic
- **Quick Actions**: Emoji picker, file attachments, and send functionality

### 🤖 AI Capabilities
- **OpenRouter Integration**: Uses Claude 3.5 Sonnet for intelligent responses
- **EV-Specific Knowledge**: Specialized prompts for electric vehicle topics
- **Conversation Memory**: Maintains context across conversation turns
- **Safety-First Approach**: Always recommends professional help for critical issues

## Technical Implementation

### Frontend Components

#### 1. ChatbotWidget.js
- Main chat interface component
- Handles message display, input, and API communication
- Manages conversation state and quick replies
- Responsive design with minimize/expand functionality

#### 2. ChatButton.js
- Floating action button for opening the chatbot
- Animated pulse effect and hover states
- Positioned fixed on all pages

#### 3. ChatbotWidget.css
- Comprehensive styling matching the design reference
- Responsive design for mobile and desktop
- Smooth animations and transitions
- Professional color scheme and typography

### Backend API

#### 1. Chatbot Router (`backend/api/chatbot.py`)
- **POST `/api/chatbot/chat`**: Main chat endpoint
- **GET `/api/chatbot/info`**: Chatbot capabilities and configuration
- **GET `/api/chatbot/health`**: Health check and API status

#### 2. OpenRouter Integration
- Uses Claude 3.5 Sonnet model via OpenRouter API
- Configurable model parameters (temperature, max tokens)
- Proper error handling and rate limiting
- Secure API key management

#### 3. Prompt Engineering
- **Base Personality**: Friendly, knowledgeable EV expert
- **Specialized Knowledge**: Charging, maintenance, purchasing, environmental impact
- **Context Awareness**: Adapts to user experience level
- **Safety Guidelines**: Always prioritizes user safety

### Prompt Templates (`models/chatbot_prompts.py`)

#### Knowledge Areas
1. **Charging Stations**: Location, specifications, user experience
2. **EV Purchasing**: Selection criteria, financial considerations, practical factors
3. **Charging Best Practices**: Battery management, speed selection, cost optimization
4. **Range Optimization**: Driving techniques, environmental factors, trip planning
5. **Maintenance & Care**: Regular maintenance, battery care, seasonal considerations
6. **Environmental Impact**: Carbon footprint, air quality, sustainability
7. **Incentives & Policies**: Federal, state, and local programs

#### Context Templates
- **New User**: Welcome and basic education
- **Experienced User**: Advanced topics and optimization
- **Troubleshooting**: Problem diagnosis and safety guidance
- **Trip Planning**: Route optimization and charging stops

## Setup and Configuration

### 1. Environment Variables
Add to your `.env` file:
```bash
# OpenRouter API Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 2. Install Dependencies
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### 3. Get OpenRouter API Key
1. Visit [OpenRouter.ai](https://openrouter.ai/)
2. Create an account and get your API key
3. Add the key to your environment variables

### 4. Start the Application
```bash
# Backend
cd backend
uvicorn app:app --reload

# Frontend
cd frontend
npm start
```

## Usage Examples

### Basic Chat
```
User: "How do I find charging stations near me?"
Bot: "I can help you find charging stations! There are several ways to locate them:
- Use apps like PlugShare, ChargePoint, or Tesla's app
- Check your vehicle's built-in navigation
- Visit websites like OpenChargeMap.org
- Use Google Maps and search for 'EV charging stations'

What's your general location? I can provide more specific guidance."
```

### Quick Reply Interaction
```
Bot: "What would you like to know about electric vehicles?"
[Quick Reply Buttons: "Find charging stations", "Get recommendations", "EV tips"]

User clicks: "Find charging stations"
Bot: "Great! I can help you find charging stations. What's your current location or where are you planning to charge? 📍"
```

### Technical Support
```
User: "My EV won't charge, what should I do?"
Bot: "I'm sorry to hear you're having charging issues. Let's troubleshoot this step by step:

1. Check the basics:
   - Is your charging cable properly connected?
   - Are there any error lights on your vehicle or charger?
   - Is your vehicle's charging port clean and undamaged?

2. Try these steps:
   - Unplug and reconnect the charging cable
   - Try a different charging station if available
   - Check your vehicle's charging settings

⚠️ Important: If you see any warning lights or smell anything unusual, stop immediately and contact a qualified EV technician or your vehicle manufacturer.

What specific symptoms are you experiencing?"
```

## Customization

### Modifying Prompts
Edit `models/chatbot_prompts.py` to customize:
- Base personality and tone
- Knowledge areas and expertise
- Context-specific responses
- Quick reply options

### Styling Changes
Modify `ChatbotWidget.css` to adjust:
- Colors and themes
- Layout and positioning
- Animations and transitions
- Responsive breakpoints

### API Configuration
Update `backend/api/chatbot.py` to modify:
- AI model selection
- Response parameters
- Error handling
- Logging and monitoring

## Security Considerations

### API Key Management
- Never commit API keys to version control
- Use environment variables for sensitive data
- Rotate keys regularly
- Monitor API usage and costs

### User Data Privacy
- Don't store sensitive user information
- Log only necessary interaction data
- Implement proper authentication
- Follow data protection regulations

### Rate Limiting
- Implement request throttling
- Monitor API usage patterns
- Set appropriate limits per user
- Handle rate limit errors gracefully

## Monitoring and Analytics

### Health Checks
- `/api/chatbot/health` endpoint for monitoring
- API key configuration status
- Service availability checks
- Response time monitoring

### Usage Analytics
- Track conversation topics
- Monitor user satisfaction
- Analyze common queries
- Identify improvement areas

### Error Handling
- Comprehensive error logging
- User-friendly error messages
- Fallback responses for API failures
- Graceful degradation

## Future Enhancements

### Planned Features
1. **Multi-language Support**: International EV markets
2. **Voice Integration**: Speech-to-text and text-to-speech
3. **Image Recognition**: Photo-based troubleshooting
4. **Integration with Platform Data**: Real-time station availability
5. **User Preferences**: Personalized responses and recommendations

### Advanced AI Features
1. **Conversation Summaries**: Session recaps and action items
2. **Predictive Responses**: Anticipate user needs
3. **Learning from Interactions**: Improve responses over time
4. **Multi-modal Input**: Support for images and documents

## Troubleshooting

### Common Issues

#### Chatbot Not Opening
- Check browser console for JavaScript errors
- Verify component imports in App.js
- Ensure CSS files are properly loaded

#### API Errors
- Verify OpenRouter API key is set
- Check network connectivity
- Review API rate limits and quotas
- Check backend logs for detailed errors

#### Styling Issues
- Clear browser cache
- Verify CSS file paths
- Check for CSS conflicts with existing styles
- Test on different browsers and devices

### Debug Mode
Enable detailed logging by setting:
```python
logging.basicConfig(level=logging.DEBUG)
```

## Support and Maintenance

### Regular Tasks
- Monitor API usage and costs
- Update prompt templates for accuracy
- Review user feedback and interactions
- Update dependencies and security patches

### Performance Optimization
- Implement response caching
- Optimize prompt lengths
- Monitor response times
- Scale infrastructure as needed

## Contributing

### Development Guidelines
1. Follow existing code style and patterns
2. Add comprehensive error handling
3. Include proper documentation
4. Test on multiple devices and browsers
5. Update this documentation for changes

### Testing
- Test chatbot responses for accuracy
- Verify UI responsiveness
- Check accessibility compliance
- Validate API error handling

---

For technical support or questions about this implementation, please refer to the main project documentation or contact the development team.
