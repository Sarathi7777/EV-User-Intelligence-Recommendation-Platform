#!/usr/bin/env python3
"""
Test script to verify chatbot connection to OpenRouter API
"""

import os
import asyncio
import aiohttp
from dotenv import load_dotenv
import json

async def test_openrouter_connection():
    """Test the connection to OpenRouter API"""
    print("🔌 Testing OpenRouter API Connection")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check if API key is loaded
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found in environment")
        return False
    
    print(f"✅ API Key loaded: {api_key[:20]}...")
    
    # Test API connection using exact OpenRouter format
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ev-user-intelligence-platform.com",
        "X-Title": "EV User Intelligence Platform"
    }
    
    payload = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [
            {"role": "user", "content": "Hello! Can you help me find charging stations?"}
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    try:
        print("🌐 Connecting to OpenRouter API...")
        print(f"   URL: {url}")
        print(f"   Model: {payload['model']}")
        print(f"   Payload: {json.dumps(payload, indent=2)}")
        
        async with aiohttp.ClientSession() as session:
            # Use json.dumps() exactly as per OpenRouter documentation
            async with session.post(url, headers=headers, data=json.dumps(payload)) as response:
                print(f"   Response Status: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    print("✅ API Connection Successful!")
                    print(f"   Response: {data['choices'][0]['message']['content'][:100]}...")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ API Error: {response.status}")
                    print(f"   Error details: {error_text}")
                    return False
                    
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def test_environment_loading():
    """Test if environment variables are loaded properly"""
    print("\n🔍 Testing Environment Variables")
    print("=" * 40)
    
    # Test before loading .env
    print("Before load_dotenv():")
    print(f"  OPENROUTER_API_KEY: {'SET' if os.getenv('OPENROUTER_API_KEY') else 'NOT SET'}")
    
    # Load .env file
    print("\nLoading .env file...")
    load_dotenv()
    
    # Test after loading .env
    print("\nAfter load_dotenv():")
    api_key = os.getenv('OPENROUTER_API_KEY')
    print(f"  OPENROUTER_API_KEY: {'SET' if api_key else 'NOT SET'}")
    
    if api_key:
        print(f"  API Key preview: {api_key[:20]}...")
        print(f"  API Key length: {len(api_key)} characters")
        print("  ✅ Environment variables loaded successfully!")
        return True
    else:
        print("  ❌ Failed to load OPENROUTER_API_KEY")
        return False

async def main():
    """Main test function"""
    print("🚗 EV Assistant Chatbot - Connection Test")
    print("=" * 60)
    
    # Test environment loading
    env_ok = test_environment_loading()
    
    if not env_ok:
        print("\n❌ Environment setup failed. Cannot proceed with API test.")
        return
    
    # Test API connection
    api_ok = await test_openrouter_connection()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    print(f"   Environment: {'✅ Ready' if env_ok else '❌ Failed'}")
    print(f"   API Connection: {'✅ Working' if api_ok else '❌ Failed'}")
    
    if env_ok and api_ok:
        print("\n🎉 Chatbot is fully connected to OpenRouter API!")
        print("   You can now use the AI-powered chatbot in your application.")
    elif env_ok and not api_ok:
        print("\n⚠️  Environment is set up but API connection failed.")
        print("   Check your internet connection and API key validity.")
    else:
        print("\n❌ Setup incomplete. Check the error messages above.")

if __name__ == "__main__":
    asyncio.run(main())
