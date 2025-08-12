#!/usr/bin/env python3
"""
Test script to verify OpenRouter API key configuration
Run this script to test if your OpenRouter API key is working correctly
"""

import os
import sys
import asyncio
import aiohttp
import json
from datetime import datetime

def test_environment_variables():
    """Test if environment variables are properly set"""
    print("🔍 Testing Environment Variables...")
    
    # Check if we're in the backend directory
    if not os.path.exists('core/config.py'):
        print("❌ Please run this script from the backend directory")
        return False
    
    # Test OpenRouter API key
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if not openrouter_key:
        print("❌ OPENROUTER_API_KEY environment variable not set")
        print("💡 Set it using: export OPENROUTER_API_KEY='your-api-key-here'")
        return False
    
    if openrouter_key == "your_openrouter_api_key_here":
        print("❌ OPENROUTER_API_KEY is still set to placeholder value")
        return False
    
    print(f"✅ OPENROUTER_API_KEY found: {openrouter_key[:20]}...")
    return True

async def test_openrouter_api():
    """Test direct OpenRouter API call"""
    print("\n🚀 Testing OpenRouter API Connection...")
    
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if not openrouter_key:
        print("❌ Cannot test API without API key")
        return False
    
    openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {openrouter_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ev-user-intelligence-platform.com",
        "X-Title": "EV User Intelligence Platform"
    }
    
    payload = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [
            {"role": "system", "content": "You are a helpful EV assistant. Respond briefly."},
            {"role": "user", "content": "Hello! Can you tell me one benefit of electric vehicles?"}
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                openrouter_url, 
                headers=headers, 
                data=json.dumps(payload)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    ai_response = data["choices"][0]["message"]["content"]
                    print(f"✅ API call successful!")
                    print(f"🤖 AI Response: {ai_response}")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ API call failed with status {response.status}")
                    print(f"Error: {error_text}")
                    return False
                    
    except Exception as e:
        print(f"❌ API call failed with error: {e}")
        return False

def test_backend_config():
    """Test backend configuration loading"""
    print("\n⚙️ Testing Backend Configuration...")
    
    try:
        # Add the current directory to Python path
        sys.path.insert(0, os.getcwd())
        
        from core.config import settings
        
        if hasattr(settings, 'OPENROUTER_API_KEY'):
            api_key = settings.OPENROUTER_API_KEY
            if api_key:
                print(f"✅ Backend config loaded: {api_key[:20]}...")
                return True
            else:
                print("❌ Backend config loaded but API key is empty")
                return False
        else:
            print("❌ Backend config doesn't have OPENROUTER_API_KEY attribute")
            return False
            
    except ImportError as e:
        print(f"❌ Failed to import backend config: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing backend config: {e}")
        return False

async def main():
    """Main test function"""
    print("🧪 OpenRouter API Configuration Test")
    print("=" * 50)
    
    # Test environment variables
    env_ok = test_environment_variables()
    
    # Test backend configuration
    config_ok = test_backend_config()
    
    # Test API connection
    api_ok = await test_openrouter_api()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"Environment Variables: {'✅ PASS' if env_ok else '❌ FAIL'}")
    print(f"Backend Configuration: {'✅ PASS' if config_ok else '❌ FAIL'}")
    print(f"API Connection: {'✅ PASS' if api_ok else '❌ FAIL'}")
    
    if all([env_ok, config_ok, api_ok]):
        print("\n🎉 All tests passed! Your OpenRouter API is configured correctly.")
        print("💡 You can now use the chatbot functionality.")
    else:
        print("\n⚠️ Some tests failed. Please check the configuration:")
        if not env_ok:
            print("   - Set the OPENROUTER_API_KEY environment variable")
        if not config_ok:
            print("   - Check backend/core/config.py configuration")
        if not api_ok:
            print("   - Verify your API key and internet connection")
    
    print("\n📚 For more help, see OPENROUTER_SETUP_GUIDE.md")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
