#!/usr/bin/env python3
"""
Complete setup and run script for EV User Intelligence & Recommendation Platform
"""

import os
import subprocess
import sys
import time

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_env_file():
    """Create a sample .env file if it doesn't exist."""
    env_path = "backend/.env"
    if not os.path.exists(env_path):
        print("\n📝 Creating sample .env file...")
        env_content = """# Snowflake Configuration
SNOWFLAKE_USER=your_snowflake_user
SNOWFLAKE_PASSWORD=your_snowflake_password
SNOWFLAKE_ACCOUNT=your_snowflake_account
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema

# Open Charge Map API
OCM_API_KEY=your_openchargemap_api_key

# ML Model Path
RECOMMENDATION_MODEL_PATH=models/lightfm_model.pkl
"""
        with open(env_path, "w") as f:
            f.write(env_content)
        print("✅ Sample .env file created at backend/.env")
        print("⚠️  Please update the .env file with your actual credentials!")

def main():
    print("🚀 EV User Intelligence & Recommendation Platform Setup")
    print("=" * 60)
    
    # Step 1: Install Python dependencies
    if not run_command("pip install -r backend/requirements.txt", "Installing Python dependencies"):
        return False
    
    # Step 2: Create .env file
    create_env_file()
    
    # Step 3: Train ML models
    if not run_command("python models/train_lightfm.py", "Training LightFM recommendation model"):
        return False
    
    if not run_command("python models/clustering.py", "Training clustering model"):
        return False
    
    # Step 4: Install Node.js dependencies
    if not run_command("cd frontend && npm install", "Installing Node.js dependencies"):
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update backend/.env with your actual credentials")
    print("2. Set up your Snowflake database and run db/create_tables.sql")
    print("3. Run: python db/fetch_and_store_ocm.py (to populate with real station data)")
    print("4. Start backend: uvicorn backend.app:app --reload")
    print("5. Start frontend: cd frontend && npm start")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 