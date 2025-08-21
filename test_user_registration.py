#!/usr/bin/env python3
"""
Test script to verify user registration with Snowflake database.
Run this script to test the complete user registration flow.
"""

import os
import sys
import json
from dotenv import load_dotenv
from db.snowflake_connector import SnowflakeManager
from fastapi.testclient import TestClient

# Load environment variables
load_dotenv()

def test_snowflake_connection():
    """Test Snowflake connection and table creation."""
    try:
        print("🔍 Testing Snowflake connection...")
        
        # Test connection
        manager = SnowflakeManager()
        print("✅ Snowflake connection successful!")
        
        # Test table creation
        print("🔍 Creating tables...")
        manager.create_tables()
        print("✅ Tables created successfully!")
        
        return manager
        
    except Exception as e:
        print(f"❌ Snowflake connection failed: {e}")
        return None

def test_user_registration(manager):
    """Test user registration functionality."""
    try:
        print("\n🔍 Testing user registration...")
        
        # Test user insertion
        test_email = "test@example.com"
        test_password_hash = "test_hash_123"
        
        # Check if user exists
        existing_user = manager.get_user_by_email(test_email)
        if existing_user:
            print(f"⚠️  User {test_email} already exists, deleting...")
            manager.delete_user(existing_user['id'])
        
        # Insert new user
        user_id = manager.insert_user(test_email, test_password_hash, 85.0)
        print(f"✅ User created with ID: {user_id}")
        
        # Verify user was created
        created_user = manager.get_user_by_email(test_email)
        if created_user:
            print(f"✅ User retrieved: {created_user}")
        else:
            print("❌ Failed to retrieve created user")
            return False
        
        # Test user update
        manager.update_user(user_id, eco_score=90.0)
        updated_user = manager.get_user_by_email(test_email)
        if updated_user['eco_score'] == 90.0:
            print("✅ User update successful")
        else:
            print("❌ User update failed")
            return False
        
        # Clean up
        manager.delete_user(user_id)
        print("✅ Test user deleted")
        
        return True
        
    except Exception as e:
        print(f"❌ User registration test failed: {e}")
        return False

def test_api_endpoints():
    """Test the API registration endpoint."""
    try:
        print("\n🔍 Testing API registration endpoint...")
        
        # Import app after setting up environment
        from backend.app import app
        
        client = TestClient(app)
        
        # Test registration data
        test_user_data = {
            "email": "apitest@example.com",
            "password": "testpass123",
            "confirm_password": "testpass123",
            "first_name": "API",
            "last_name": "Test",
            "vehicle_type": "Tesla"
        }
        
        # Test the endpoint
        response = client.post("/login/register", json=test_user_data)
        
        if response.status_code == 200:
            print("✅ API registration endpoint working")
            user_data = response.json()
            print(f"   User created: {user_data}")
            return True
        else:
            print(f"❌ API registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API endpoint test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🚗 EV User Intelligence - User Registration Test")
    print("=" * 50)
    
    # Test 1: Snowflake connection
    manager = test_snowflake_connection()
    if not manager:
        print("\n❌ Cannot proceed without Snowflake connection")
        return
    
    # Test 2: User registration functionality
    user_test_success = test_user_registration(manager)
    
    # Test 3: API endpoints
    api_test_success = test_api_endpoints()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    print(f"Snowflake Connection: {'✅ PASS' if manager else '❌ FAIL'}")
    print(f"User Registration: {'✅ PASS' if user_test_success else '❌ FAIL'}")
    print(f"API Endpoints: {'✅ PASS' if api_test_success else '❌ FAIL'}")
    
    if manager and user_test_success and api_test_success:
        print("\n🎉 All tests passed! User registration is working correctly.")
        print("New accounts will now be saved to your Snowflake database.")
    else:
        print("\n⚠️  Some tests failed. Please check the error messages above.")
        print("Make sure your Snowflake credentials are correct in the .env file.")

if __name__ == "__main__":
    main()
