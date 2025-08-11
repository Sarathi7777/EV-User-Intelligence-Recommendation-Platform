#!/usr/bin/env python3
"""
Test script to verify environment variables are loaded from .env file
"""

import os
from dotenv import load_dotenv

def test_environment():
    """Test if environment variables are loaded properly"""
    print("🔍 Testing Environment Variables")
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
    else:
        print("  ❌ Failed to load OPENROUTER_API_KEY")
    
    # Check other important variables
    print("\nOther environment variables:")
    print(f"  SNOWFLAKE_USER: {'SET' if os.getenv('SNOWFLAKE_USER') else 'NOT SET'}")
    print(f"  JWT_SECRET_KEY: {'SET' if os.getenv('JWT_SECRET_KEY') else 'NOT SET'}")
    print(f"  OCM_API_KEY: {'SET' if os.getenv('OCM_API_KEY') else 'NOT SET'}")
    
    # Check if .env file exists
    env_file_path = ".env"
    print(f"\n.env file check:")
    print(f"  File exists: {os.path.exists(env_file_path)}")
    print(f"  Current working directory: {os.getcwd()}")
    
    if os.path.exists(env_file_path):
        print(f"  .env file size: {os.path.getsize(env_file_path)} bytes")
        print(f"  .env file path: {os.path.abspath(env_file_path)}")

if __name__ == "__main__":
    test_environment()
