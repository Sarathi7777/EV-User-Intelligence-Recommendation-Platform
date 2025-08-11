#!/usr/bin/env python3
"""
Chatbot Setup Script for EV User Intelligence Recommendation Platform
This script helps you set up and test the AI chatbot functionality.
"""

import os
import sys
import asyncio
import aiohttp
from pathlib import Path

def check_environment():
    """Check if required environment variables are set"""
    print("🔍 Checking environment configuration...")
    
    # Check if we're in the right directory
    if not Path("backend").exists():
        print("❌ Error: Please run this script from the project root directory")
        print("   Current directory:", os.getcwd())
        return False
    
    # Check for .env file
    env_file = Path(".env")
    if env_file.exists():
        print("✅ Found .env file")
    else:
        print("⚠️  No .env file found. Creating one from template...")
        create_env_file()
    
    # Check OpenRouter API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key and api_key != "your_openrouter_api_key_here":
        print("✅ OPENROUTER_API_KEY is configured")
        return True
    else:
        print("❌ OPENROUTER_API_KEY is not configured")
        print("\n📋 To get your OpenRouter API key:")
        print("   1. Go to https://openrouter.ai/")
        print("   2. Sign up for a free account")
        print("   3. Get your API key from the dashboard")
        print("   4. Add it to your .env file:")
        print("      OPENROUTER_API_KEY=your_actual_api_key_here")
        return False

def create_env_file():
    """Create .env file from template"""
    template_file = Path("env_template.txt")
    env_file = Path(".env")
    
    if template_file.exists():
        with open(template_file, 'r') as f:
            template_content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(template_content)
        
        print("✅ Created .env file from template")
        print("📝 Please edit .env file and add your actual API keys")
    else:
        print("❌ Error: env_template.txt not found")

def test_backend_connection():
    """Test if the backend is running and accessible"""
    print("\n🔌 Testing backend connection...")
    
    try:
        import requests
        response = requests.get("http://localhost:8000/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and accessible")
            return True
        else:
            print(f"⚠️  Backend responded with status: {response.status_code}")
            return False
    except ImportError:
        print("⚠️  requests library not installed. Installing...")
        os.system("pip install requests")
        return test_backend_connection()
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running")
        print("   To start the backend:")
        print("   1. cd backend")
        print("   2. python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000")
        return False
    except Exception as e:
        print(f"❌ Error testing backend: {e}")
        return False

def test_chatbot_api():
    """Test the chatbot API endpoints"""
    print("\n🤖 Testing chatbot API...")
    
    try:
        import requests
        
        # Test health endpoint
        print("   Testing /api/chatbot/health...")
        response = requests.get("http://localhost:8000/api/chatbot/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"   ✅ Health check passed: {health_data}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
        
        # Test info endpoint
        print("   Testing /api/chatbot/info...")
        response = requests.get("http://localhost:8000/api/chatbot/info", timeout=10)
        if response.status_code == 200:
            info_data = response.json()
            print(f"   ✅ Info endpoint working: {info_data['name']}")
        else:
            print(f"   ❌ Info endpoint failed: {response.status_code}")
            return False
        
        # Test chat endpoint (this will fail without API key, but we can test the endpoint)
        print("   Testing /api/chatbot/chat...")
        chat_data = {
            "message": "Hello, can you help me find charging stations?",
            "user_id": "test_user",
            "conversation_history": []
        }
        
        response = requests.post("http://localhost:8000/api/chatbot/chat", 
                               json=chat_data, timeout=15)
        
        if response.status_code == 500:
            error_data = response.json()
            if "OPENROUTER_API_KEY" in error_data.get("detail", ""):
                print("   ⚠️  Chat endpoint working but needs API key configured")
                return True
            else:
                print(f"   ❌ Chat endpoint error: {error_data}")
                return False
        elif response.status_code == 200:
            print("   ✅ Chat endpoint working with AI responses!")
            return True
        else:
            print(f"   ❌ Chat endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error testing chatbot API: {e}")
        return False

def main():
    """Main setup function"""
    print("🚗 EV User Intelligence Platform - Chatbot Setup")
    print("=" * 60)
    
    # Check environment
    env_ok = check_environment()
    
    # Test backend
    backend_ok = test_backend_connection()
    
    # Test chatbot API
    chatbot_ok = False
    if backend_ok:
        chatbot_ok = test_chatbot_api()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Setup Summary:")
    print(f"   Environment: {'✅ Ready' if env_ok else '❌ Needs API key'}")
    print(f"   Backend: {'✅ Running' if backend_ok else '❌ Not running'}")
    print(f"   Chatbot API: {'✅ Working' if chatbot_ok else '❌ Needs setup'}")
    
    if env_ok and backend_ok and chatbot_ok:
        print("\n🎉 Chatbot is fully configured and working!")
        print("   You can now use the chatbot in your frontend application.")
    elif not env_ok:
        print("\n🔑 Next steps:")
        print("   1. Get your OpenRouter API key from https://openrouter.ai/")
        print("   2. Add it to your .env file")
        print("   3. Restart your backend server")
        print("   4. Run this script again to test")
    elif not backend_ok:
        print("\n🚀 Next steps:")
        print("   1. Start your backend server")
        print("   2. Run this script again to test")
    else:
        print("\n⚠️  Chatbot API needs configuration")
        print("   Check the error messages above for details")

if __name__ == "__main__":
    main()
