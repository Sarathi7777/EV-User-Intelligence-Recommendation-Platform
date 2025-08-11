from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import os
import json
import aiohttp
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chatbot", tags=["chatbot"])

# Chatbot configuration
CHATBOT_CONFIG = {
    "name": "EV Assistant",
    "personality": "friendly, helpful, knowledgeable about electric vehicles",
    "model": "deepseek/deepseek-r1:free",  # OpenRouter model
    "max_tokens": 1000,
    "temperature": 0.7
}

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    user_id: str
    conversation_history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    response: str
    timestamp: str
    model_used: str

# EV-specific prompt templates
EV_PROMPT_TEMPLATES = {
    "greeting": "You are {name}, a helpful AI assistant specializing in electric vehicles and charging infrastructure. You help users with EV-related questions, charging station information, and recommendations.",
    
    "charging_stations": "When discussing charging stations, consider: location, charging speed, connector types, availability, pricing, and user reviews. Always suggest checking real-time availability.",
    
    "ev_tips": "Provide practical EV tips including: battery maintenance, charging best practices, range optimization, cost savings, and environmental benefits.",
    
    "recommendations": "For recommendations, consider: user's location, driving patterns, budget, charging access, and specific needs. Always ask clarifying questions when needed.",
    
    "technical_support": "For technical issues, provide general guidance but always recommend consulting with qualified EV technicians or the vehicle manufacturer for specific problems."
}

def build_system_prompt() -> str:
    """Build the system prompt for the EV assistant"""
    base_prompt = EV_PROMPT_TEMPLATES["greeting"].format(name=CHATBOT_CONFIG["name"])
    
    system_prompt = f"""
{base_prompt}

You are an expert AI assistant specializing in electric vehicles and charging infrastructure. Your role is to provide helpful, accurate, and engaging information to users.

**Key areas of expertise:**
- Electric vehicle technology and specifications
- Charging station locations and information
- EV charging best practices and tips
- Cost analysis and savings calculations
- Environmental impact and sustainability
- EV maintenance and troubleshooting
- Government incentives and policies

**Communication Guidelines:**
- Be conversational, friendly, and professional
- Provide accurate, up-to-date information
- Ask follow-up questions to better understand user needs
- Give specific, actionable advice when possible
- Use emojis sparingly but effectively to maintain engagement
- Break down complex information into digestible parts
- Always encourage further questions and engagement

**Response Style:**
- Be interactive and ask clarifying questions
- Provide location-specific information when possible
- Give practical tips and real-world examples
- Suggest next steps or related topics
- Use bullet points and formatting for readability
- Keep responses concise but comprehensive

**When users ask about locations (like cities):**
- Provide specific charging station recommendations
- Mention popular areas and charging networks
- Suggest using the platform's search features
- Ask about their specific needs in that area

**When users ask about EV topics:**
- Provide practical, actionable information
- Ask about their specific situation or needs
- Suggest related topics they might be interested in
- Encourage them to explore more features of the platform

Current date: {datetime.now().strftime('%Y-%m-%d')}

Remember: Your goal is to be helpful, engaging, and to encourage users to explore more about EVs and use the platform's features effectively.
"""
    return system_prompt.strip()

async def call_openrouter_api(messages: List[dict]) -> str:
    """Call OpenRouter API to get AI response"""
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    
    # Debug logging
    logger.info(f"OpenRouter API key loaded: {'YES' if openrouter_api_key else 'NO'}")
    if openrouter_api_key:
        logger.info(f"API key starts with: {openrouter_api_key[:20]}...")
    else:
        logger.error("No OpenRouter API key found in environment variables")
        logger.error("Available environment variables: " + str([k for k in os.environ.keys() if 'OPENROUTER' in k.upper()]))
    
    if not openrouter_api_key:
        logger.error("OpenRouter API key not configured")
        raise HTTPException(
            status_code=500, 
            detail="AI service not configured. Please set OPENROUTER_API_KEY environment variable."
        )
    
    openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {openrouter_api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ev-user-intelligence-platform.com",
        "X-Title": "EV User Intelligence Platform"
    }
    
    # Prepare payload exactly as per OpenRouter documentation
    payload = {
        "model": CHATBOT_CONFIG["model"],
        "messages": messages,
        "max_tokens": CHATBOT_CONFIG["max_tokens"],
        "temperature": CHATBOT_CONFIG["temperature"]
    }
    
    try:
        logger.info(f"Calling OpenRouter API with model: {CHATBOT_CONFIG['model']}")
        logger.info(f"Message count: {len(messages)}")
        logger.info(f"Payload: {json.dumps(payload, indent=2)}")
        
        async with aiohttp.ClientSession() as session:
            # Use json.dumps() to properly serialize the payload
            async with session.post(
                openrouter_url, 
                headers=headers, 
                data=json.dumps(payload)
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"OpenRouter API error: {response.status} - {error_text}")
                    
                    if response.status == 401:
                        raise HTTPException(
                            status_code=500, 
                            detail="AI service authentication failed. Please check your API key."
                        )
                    elif response.status == 429:
                        raise HTTPException(
                            status_code=500, 
                            detail="AI service rate limit exceeded. Please try again later."
                        )
                    elif response.status == 500:
                        raise HTTPException(
                            status_code=500, 
                            detail="AI service temporarily unavailable. Please try again later."
                        )
                    else:
                        raise HTTPException(
                            status_code=500, 
                            detail=f"AI service error: {response.status}. Please try again later."
                        )
                
                data = await response.json()
                logger.info("Successfully received response from OpenRouter API")
                logger.info(f"Response data: {json.dumps(data, indent=2)}")
                return data["choices"][0]["message"]["content"]
                
    except aiohttp.ClientError as e:
        logger.error(f"HTTP client error: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Failed to communicate with AI service. Please check your internet connection."
        )
    except Exception as e:
        logger.error(f"Unexpected error in OpenRouter API call: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error. Please try again later."
        )

def preprocess_user_message(message: str) -> str:
    """Preprocess user message for better context understanding"""
    # Add common EV-related context if not present
    ev_keywords = ["ev", "electric", "charging", "battery", "tesla", "leaf", "bolt", "station"]
    message_lower = message.lower()
    
    # If message doesn't contain EV keywords, add context
    if not any(keyword in message_lower for keyword in ev_keywords):
        message = f"User query about electric vehicles: {message}"
    
    return message

@router.post("/chat", response_model=ChatResponse)
async def chat_with_assistant(request: ChatRequest):
    """Main chat endpoint for the EV assistant"""
    try:
        # Preprocess user message
        processed_message = preprocess_user_message(request.message)
        
        # Build conversation context
        system_prompt = build_system_prompt()
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history (limit to last 10 messages to avoid token limits)
        if request.conversation_history:
            recent_history = request.conversation_history[-10:]
            for msg in recent_history:
                messages.append({"role": msg.role, "content": msg.content})
        
        # Add current user message
        messages.append({"role": "user", "content": processed_message})
        
        # Get AI response
        ai_response = await call_openrouter_api(messages)
        
        # Log the interaction for monitoring
        logger.info(f"Chat interaction - User: {request.user_id}, Message: {request.message[:100]}...")
        
        return ChatResponse(
            response=ai_response,
            timestamp=datetime.now().isoformat(),
            model_used=CHATBOT_CONFIG["model"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/info")
async def get_chatbot_info():
    """Get chatbot configuration and capabilities"""
    return {
        "name": CHATBOT_CONFIG["name"],
        "personality": CHATBOT_CONFIG["personality"],
        "capabilities": [
            "EV technology information",
            "Charging station assistance",
            "EV tips and best practices",
            "Cost and savings analysis",
            "Environmental impact information",
            "Maintenance guidance",
            "Policy and incentive information"
        ],
        "model": CHATBOT_CONFIG["model"],
        "status": "online"
    }

@router.get("/health")
async def chatbot_health():
    """Health check endpoint for the chatbot service"""
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    return {
        "status": "healthy",
        "openrouter_configured": bool(openrouter_key),
        "timestamp": datetime.now().isoformat()
    }

@router.get("/debug")
async def debug_environment():
    """Debug endpoint to check environment variables"""
    import os
    return {
        "openrouter_api_key_set": bool(os.getenv("OPENROUTER_API_KEY")),
        "api_key_preview": os.getenv("OPENROUTER_API_KEY")[:20] + "..." if os.getenv("OPENROUTER_API_KEY") else "None",
        "all_env_vars": {k: v for k, v in os.environ.items() if "OPENROUTER" in k.upper()},
        "current_working_dir": os.getcwd(),
        "env_file_exists": os.path.exists(".env")
    }
