#!/usr/bin/env python3
"""
Synchronous test script for OpenRouter API using requests library
Exact format from OpenRouter documentation
"""

import requests
import json
import os
from dotenv import load_dotenv

def test_openrouter_sync():
    """Test OpenRouter API using requests library (synchronous)"""
    print("🔌 Testing OpenRouter API (Synchronous)")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found in environment")
        return False
    
    print(f"✅ API Key loaded: {api_key[:20]}...")
    
    # Test using exact format from OpenRouter documentation
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://ev-user-intelligence-platform.com",  # Optional. Site URL for rankings on openrouter.ai.
            "X-Title": "EV User Intelligence Platform",  # Optional. Site title for rankings on openrouter.ai.
        },
        data=json.dumps({
            "model": "deepseek/deepseek-r1:free",
            "messages": [
                {
                    "role": "user",
                    "content": "Hello! Can you help me find charging stations for electric vehicles?"
                }
            ],
            "max_tokens": 150,
            "temperature": 0.7
        })
    )
    
    print(f"Response Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ API Connection Successful!")
        print(f"Response: {data['choices'][0]['message']['content']}")
        return True
    else:
        print(f"❌ API Error: {response.status_code}")
        print(f"Error details: {response.text}")
        return False

def test_ev_specific_query():
    """Test with EV-specific query"""
    print("\n🚗 Testing EV-Specific Query")
    print("=" * 40)
    
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        print("❌ API key not available")
        return False
    
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://ev-user-intelligence-platform.com",
            "X-Title": "EV User Intelligence Platform",
        },
        data=json.dumps({
            "model": "deepseek/deepseek-r1:free",
            "messages": [
                {
                    "role": "user",
                    "content": "I'm in Coimbatore and need to find charging stations. Can you help me?"
                }
            ],
            "max_tokens": 200,
            "temperature": 0.7
        })
    )
    
    print(f"Response Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ EV Query Successful!")
        print(f"Response: {data['choices'][0]['message']['content']}")
        return True
    else:
        print(f"❌ EV Query Failed: {response.status_code}")
        print(f"Error: {response.text}")
        return False

def main():
    """Main test function"""
    print("🚗 OpenRouter API Connection Test")
    print("=" * 60)
    
    # Test basic connection
    basic_test = test_openrouter_sync()
    
    if basic_test:
        # Test EV-specific query
        ev_test = test_ev_specific_query()
        
        print("\n" + "=" * 60)
        print("📊 Test Summary:")
        print(f"   Basic API Connection: {'✅ Working' if basic_test else '❌ Failed'}")
        print(f"   EV-Specific Query: {'✅ Working' if ev_test else '❌ Failed'}")
        
        if basic_test and ev_test:
            print("\n🎉 OpenRouter API is fully connected and working!")
            print("   Your chatbot should now work with real AI responses.")
        else:
            print("\n⚠️  Basic connection works but EV queries may have issues.")
    else:
        print("\n❌ Basic API connection failed. Check your API key and internet connection.")

if __name__ == "__main__":
    main()
