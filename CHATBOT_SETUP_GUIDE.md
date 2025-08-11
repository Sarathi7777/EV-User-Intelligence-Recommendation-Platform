# 🤖 EV Assistant Chatbot - Setup Guide

## Overview
The EV Assistant Chatbot is an AI-powered conversational interface that helps users with electric vehicle-related questions, charging station information, and recommendations. It uses the OpenRouter API to provide intelligent, context-aware responses.

## ✨ Features

### 🎯 Core Capabilities
- **Charging Station Assistance**: Find and recommend charging stations
- **EV Tips & Best Practices**: Battery care, range optimization, charging strategies
- **Interactive Conversations**: Context-aware responses with follow-up questions
- **Quick Reply System**: Pre-built responses for common queries
- **Fallback Responses**: Helpful information even when AI is unavailable

### 🚀 Technical Features
- **Real-time AI Responses**: Powered by OpenRouter API
- **Conversation Memory**: Remembers context from previous messages
- **Error Handling**: Graceful fallbacks and helpful error messages
- **Responsive UI**: Modern, mobile-friendly chat interface
- **Floating Action Button**: Easy access from anywhere in the app

## 🛠️ Setup Instructions

### 1. Get OpenRouter API Key
1. Visit [https://openrouter.ai/](https://openrouter.ai/)
2. Sign up for a free account
3. Navigate to your dashboard
4. Copy your API key

### 2. Configure Environment
1. Copy `env_template.txt` to `.env` in your project root
2. Add your OpenRouter API key:
   ```bash
   OPENROUTER_API_KEY=your_actual_api_key_here
   ```

### 3. Install Dependencies
```bash
# Backend dependencies
cd backend
pip install -r requirements.txt

# Frontend dependencies
cd ../frontend
npm install
```

### 4. Start the Backend
```bash
cd backend
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 5. Start the Frontend
```bash
cd frontend
npm start
```

### 6. Test the Setup
```bash
# From project root
python setup_chatbot.py
```

## 🔧 Configuration

### Backend Configuration (`backend/api/chatbot.py`)
```python
CHATBOT_CONFIG = {
    "name": "EV Assistant",
    "personality": "friendly, helpful, knowledgeable about electric vehicles",
    "model": "deepseek/deepseek-r1:free",  # OpenRouter model
    "max_tokens": 1000,
    "temperature": 0.7
}
```

### Available Models
- `deepseek/deepseek-r1:free` - Free tier, good performance
- `anthropic/claude-3.5-sonnet` - High quality, paid tier
- `openai/gpt-4` - Premium model, paid tier
- `meta-llama/llama-3.1-8b-instruct` - Open source option

## 📱 Usage Examples

### Basic Conversation Flow
1. **User**: "Find charging stations"
2. **Bot**: "Great! I can help you find charging stations. What's your current location?"
3. **User**: "Coimbatore"
4. **Bot**: "Perfect! Coimbatore has several great charging options..." (with specific recommendations)

### Quick Reply System
- Pre-built buttons for common actions
- Contextual follow-up questions
- Progressive information disclosure

### Error Handling
- Graceful fallbacks when AI is unavailable
- Helpful local responses for common queries
- Clear error messages for troubleshooting

## 🚨 Troubleshooting

### Common Issues

#### 1. "AI service not configured" Error
**Problem**: OpenRouter API key not set
**Solution**: 
```bash
# Add to .env file
OPENROUTER_API_KEY=your_actual_key_here
# Restart backend server
```

#### 2. "Backend is not running" Error
**Problem**: FastAPI server not started
**Solution**:
```bash
cd backend
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

#### 3. "Rate limit exceeded" Error
**Problem**: Too many API calls to OpenRouter
**Solution**: Wait a few minutes or upgrade your OpenRouter plan

#### 4. Chatbot not responding interactively
**Problem**: AI responses are generic or predefined
**Solution**: 
- Check if API key is valid
- Verify OpenRouter service status
- Check backend logs for errors

### Debug Steps
1. **Check Backend Logs**:
   ```bash
   cd backend
   python -c "import logging; logging.basicConfig(level=logging.DEBUG)"
   ```

2. **Test API Endpoints**:
   ```bash
   curl http://localhost:8000/api/chatbot/health
   curl http://localhost:8000/api/chatbot/info
   ```

3. **Verify Environment**:
   ```bash
   python setup_chatbot.py
   ```

## 🔒 Security Considerations

### API Key Management
- Never commit API keys to version control
- Use environment variables for sensitive data
- Rotate API keys regularly
- Monitor API usage for unusual activity

### Rate Limiting
- Implement request throttling
- Monitor API quotas
- Handle rate limit errors gracefully

### Input Validation
- Sanitize user inputs
- Limit message length
- Validate conversation history

## 📊 Monitoring & Analytics

### Logging
- All API calls are logged
- Error responses are captured
- User interactions are tracked

### Health Checks
- `/api/chatbot/health` endpoint
- API key configuration status
- Service availability monitoring

## 🚀 Future Enhancements

### Planned Features
- **Multi-language Support**: Hindi, Tamil, and other regional languages
- **Voice Integration**: Speech-to-text and text-to-speech
- **Advanced Analytics**: User behavior insights
- **Personalization**: User preference learning
- **Integration**: Connect with station data APIs

### Customization Options
- **Prompt Templates**: Modify AI behavior
- **Response Styles**: Adjust tone and format
- **Quick Replies**: Add custom action buttons
- **UI Themes**: Customize appearance

## 📚 API Reference

### Endpoints

#### `POST /api/chatbot/chat`
Main chat endpoint for user interactions
```json
{
  "message": "User message",
  "user_id": "user123",
  "conversation_history": [
    {"role": "user", "content": "Previous message"},
    {"role": "assistant", "content": "Previous response"}
  ]
}
```

#### `GET /api/chatbot/health`
Health check endpoint
```json
{
  "status": "healthy",
  "openrouter_configured": true,
  "timestamp": "2024-01-01T00:00:00"
}
```

#### `GET /api/chatbot/info`
Chatbot information and capabilities
```json
{
  "name": "EV Assistant",
  "personality": "friendly, helpful...",
  "capabilities": ["EV technology information", "..."],
  "model": "deepseek/deepseek-r1:free",
  "status": "online"
}
```

## 🤝 Support

### Getting Help
1. Check this guide for common solutions
2. Review backend logs for error details
3. Test with the setup script
4. Check OpenRouter service status

### Contributing
- Report bugs with detailed error messages
- Suggest improvements for user experience
- Contribute to prompt engineering
- Help with localization

---

**Happy EV Charging! 🚗⚡**
