#!/usr/bin/env python3
"""
Simple script to check if users exist in Snowflake database.
Run this to verify that user data is being stored correctly.
"""

import os
import sys
from dotenv import load_dotenv
from db.snowflake_connector import SnowflakeManager

# Load environment variables
load_dotenv()

def check_snowflake_users():
    """Check users in Snowflake database."""
    try:
        print("🔍 Checking users in Snowflake database...")
        
        # Connect to Snowflake
        manager = SnowflakeManager()
        print("✅ Connected to Snowflake")
        
        # Get all users
        users = manager.get_all_users()
        
        if users:
            print(f"\n📊 Found {len(users)} users in Snowflake:")
            print("-" * 60)
            for user in users:
                print(f"ID: {user['id']}, Email: {user['email']}, Eco Score: {user['eco_score']}")
                print(f"Created: {user['created_at']}, Updated: {user['updated_at']}")
                print("-" * 60)
        else:
            print("❌ No users found in Snowflake database")
            
        # Check specific user by email
        test_email = input("\n🔍 Enter email to search for (or press Enter to skip): ").strip()
        if test_email:
            user = manager.get_user_by_email(test_email)
            if user:
                print(f"✅ User found: {user}")
            else:
                print(f"❌ User with email '{test_email}' not found")
                
    except Exception as e:
        print(f"❌ Error checking Snowflake users: {e}")
        print("\n💡 Make sure:")
        print("1. Your .env file has correct Snowflake credentials")
        print("2. Snowflake is accessible from your network")
        print("3. The users table exists in your database")

if __name__ == "__main__":
    print("🚗 EV User Intelligence - Snowflake Users Check")
    print("=" * 50)
    check_snowflake_users()
