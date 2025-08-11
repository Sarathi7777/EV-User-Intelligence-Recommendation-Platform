#!/usr/bin/env python3
"""
Test script for the EV Chatbot API
Run this to verify the chatbot is working correctly
"""

import requests
import json
import os
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
CHATBOT_ENDPOINT = f"{BASE_URL}/api/chatbot"

def test_chatbot_health():
    """Test the chatbot health endpoint"""
    print("🔍 Testing chatbot health...")
    
    try:
        response = requests.get(f"{CHATBOT_ENDPOINT}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            print(f"   OpenRouter configured: {data['openrouter_configured']}")
            print(f"   Timestamp: {data['timestamp']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check error: {e}")
        return False

def test_chatbot_info():
    """Test the chatbot info endpoint"""
    print("\n🔍 Testing chatbot info...")
    
    try:
        response = requests.get(f"{CHATBOT_ENDPOINT}/info")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Info endpoint working")
            print(f"   Name: {data['name']}")
            print(f"   Model: {data['model']}")
            print(f"   Capabilities: {len(data['capabilities'])} areas")
            return True
        else:
            print(f"❌ Info endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Info endpoint error: {e}")
        return False

def test_chatbot_chat():
    """Test the main chat endpoint"""
    print("\n🔍 Testing chatbot chat...")
    
    # Check if OpenRouter API key is configured
    if not os.getenv("OPENROUTER_API_KEY"):
        print("⚠️  OPENROUTER_API_KEY not set - skipping chat test")
        print("   Set the environment variable to test full functionality")
        return False
    
    test_message = "Hello! I'm new to electric vehicles. Can you tell me about charging stations?"
    
    try:
        payload = {
            "message": test_message,
            "user_id": "test_user",
            "conversation_history": []
        }
        
        response = requests.post(
            f"{CHATBOT_ENDPOINT}/chat",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat endpoint working")
            print(f"   Response length: {len(data['response'])} characters")
            print(f"   Model used: {data['model_used']}")
            print(f"   Timestamp: {data['timestamp']}")
            print(f"\n📝 Sample response:")
            print(f"   {data['response'][:200]}...")
            return True
        else:
            print(f"❌ Chat endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Chat endpoint error: {e}")
        return False

def test_backend_connection():
    """Test if the backend is running"""
    print("🔍 Testing backend connection...")
    
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ Backend is running and accessible")
            return True
        else:
            print(f"❌ Backend responded with status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("   Make sure the backend is running with: uvicorn app:app --reload")
        return False

def main():
    """Run all tests"""
    print("🚗 EV Chatbot API Test Suite")
    print("=" * 40)
    print(f"Testing against: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test backend connection first
    if not test_backend_connection():
        print("\n❌ Backend connection failed. Please start the backend first.")
        return
    
    # Run chatbot tests
    health_ok = test_chatbot_health()
    info_ok = test_chatbot_info()
    chat_ok = test_chatbot_chat()
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 Test Results Summary")
    print("=" * 40)
    print(f"Backend Connection: {'✅' if True else '❌'}")
    print(f"Health Check: {'✅' if health_ok else '❌'}")
    print(f"Info Endpoint: {'✅' if info_ok else '❌'}")
    print(f"Chat Endpoint: {'✅' if chat_ok else '❌'}")
    
    if health_ok and info_ok:
        print("\n🎉 Basic chatbot functionality is working!")
        if chat_ok:
            print("🎉 Full chatbot functionality is working!")
        else:
            print("⚠️  Chat functionality needs OpenRouter API key configuration")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
    
    print("\n💡 Next steps:")
    if not os.getenv("OPENROUTER_API_KEY"):
        print("   1. Get an API key from https://openrouter.ai/")
        print("   2. Set OPENROUTER_API_KEY environment variable")
        print("   3. Restart the backend")
    print("   4. Test the frontend chatbot widget")
    print("   5. Check the CHATBOT_IMPLEMENTATION.md for details")

if __name__ == "__main__":
    main()
