#!/usr/bin/env python3
"""
Snowflake Integration Setup Script for EV User Intelligence
==================================================

This script helps you:
1. Configure Snowflake connection
2. Test the connection
3. Create database tables
4. Fetch and store Open Charge Map data
5. Verify the integration

Usage:
    python setup_snowflake_integration.py
"""

import os
import sys
import json
import getpass
from pathlib import Path
from typing import Dict, Any, Optional

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent))

def create_env_file() -> bool:
    """Create .env file with user input."""
    print("=== Snowflake Configuration ===")
    print("Please provide your Snowflake credentials:")
    
    config = {}
    
    # Snowflake credentials
    config['SNOWFLAKE_USER'] = input("Snowflake Username: ").strip()
    config['SNOWFLAKE_PASSWORD'] = getpass.getpass("Snowflake Password: ")
    config['SNOWFLAKE_ACCOUNT'] = input("Snowflake Account (e.g., xy12345.us-east-1): ").strip()
    config['SNOWFLAKE_WAREHOUSE'] = input("Snowflake Warehouse: ").strip()
    config['SNOWFLAKE_DATABASE'] = input("Snowflake Database: ").strip()
    config['SNOWFLAKE_SCHEMA'] = input("Snowflake Schema: ").strip()
    
    # Open Charge Map API
    print("\n=== Open Charge Map API ===")
    print("Get your free API key from: https://openchargemap.io/site/develop/api")
    config['OCM_API_KEY'] = input("Open Charge Map API Key: ").strip()
    
    # ML Model paths
    config['RECOMMENDATION_MODEL_PATH'] = 'models/recommendation_model.pkl'
    
    # Create .env file
    env_path = Path("backend/.env")
    env_path.parent.mkdir(exist_ok=True)
    
    with open(env_path, 'w') as f:
        for key, value in config.items():
            f.write(f"{key}={value}\n")
    
    print(f"\n✅ Environment file created: {env_path}")
    return True

def test_snowflake_connection() -> bool:
    """Test Snowflake connection."""
    print("\n=== Testing Snowflake Connection ===")
    
    try:
        from db.snowflake_connector import SnowflakeManager
        
        # Test connection
        manager = SnowflakeManager()
        
        # Test basic query
        result = manager.execute_query("SELECT CURRENT_VERSION() as version")
        if result:
            print(f"✅ Snowflake connection successful!")
            print(f"   Version: {result[0]['version']}")
            return True
        else:
            print("❌ Snowflake connection failed: No response")
            return False
            
    except Exception as e:
        print(f"❌ Snowflake connection failed: {e}")
        return False

def create_database_tables() -> bool:
    """Create database tables."""
    print("\n=== Creating Database Tables ===")
    
    try:
        from db.snowflake_connector import SnowflakeManager
        
        manager = SnowflakeManager()
        manager.create_tables()
        
        print("✅ Database tables created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def test_ocm_api() -> bool:
    """Test Open Charge Map API connection."""
    print("\n=== Testing Open Charge Map API ===")
    
    try:
        import requests
        
        api_key = os.getenv("OCM_API_KEY")
        if not api_key:
            print("❌ OCM_API_KEY not found in environment")
            return False
        
        # Test API with a simple query
        url = "https://api.openchargemap.io/v3/poi"
        params = {
            "key": api_key,
            "output": "json",
            "maxresults": 1,
            "compact": "true"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data:
            print("✅ Open Charge Map API connection successful!")
            print(f"   Sample station: {data[0].get('AddressInfo', {}).get('Title', 'Unknown')}")
            return True
        else:
            print("❌ Open Charge Map API returned no data")
            return False
            
    except Exception as e:
        print(f"❌ Open Charge Map API test failed: {e}")
        return False

def run_ocm_ingestion(countries: list = None, max_stations: int = 100) -> bool:
    """Run Open Charge Map data ingestion."""
    print("\n=== Running Open Charge Map Data Ingestion ===")
    
    if countries is None:
        countries = ["US"]  # Start with US for testing
    
    try:
        from db.fetch_and_store_ocm import OpenChargeMapFetcher
        
        fetcher = OpenChargeMapFetcher()
        
        # Run ingestion for specified countries
        results = fetcher.run_full_ingestion(countries, max_stations)
        
        print("✅ Data ingestion completed!")
        print(f"   Total stations fetched: {results['summary']['total_fetched']}")
        print(f"   Total stations stored: {results['summary']['total_stored']}")
        
        # Save results
        with open("ingestion_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        print("   Results saved to: ingestion_results.json")
        
        return True
        
    except Exception as e:
        print(f"❌ Data ingestion failed: {e}")
        return False

def verify_integration() -> bool:
    """Verify the complete integration."""
    print("\n=== Verifying Integration ===")
    
    try:
        from db.snowflake_connector import SnowflakeManager
        
        manager = SnowflakeManager()
        
        # Check station count
        station_count = manager.get_station_count()
        print(f"   Stations in database: {station_count}")
        
        # Get sample stations
        stations = manager.get_stations(limit=5)
        if stations:
            print(f"   Sample stations:")
            for station in stations[:3]:
                print(f"     - {station['name']} ({station['energy_type']})")
        
        # Test location-based query
        sample_stations = manager.get_stations_by_location(37.7749, -122.4194, 10)
        print(f"   Stations near San Francisco: {len(sample_stations)}")
        
        print("✅ Integration verification successful!")
        return True
        
    except Exception as e:
        print(f"❌ Integration verification failed: {e}")
        return False

def main():
    """Main setup function."""
    print("🚗 EV User Intelligence - Snowflake Integration Setup")
    print("=" * 50)
    
    # Check if .env file exists
    env_path = Path("backend/.env")
    if not env_path.exists():
        print("No .env file found. Let's create one...")
        if not create_env_file():
            print("❌ Failed to create .env file")
            return False
    else:
        print("✅ .env file found")
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv(env_path)
    
    # Test connections
    if not test_snowflake_connection():
        print("❌ Snowflake connection failed. Please check your credentials.")
        return False
    
    if not test_ocm_api():
        print("❌ Open Charge Map API test failed. Please check your API key.")
        return False
    
    # Create tables
    if not create_database_tables():
        print("❌ Failed to create database tables.")
        return False
    
    # Ask user if they want to run data ingestion
    print("\n=== Data Ingestion ===")
    run_ingestion = input("Do you want to fetch and store Open Charge Map data? (y/n): ").lower().strip()
    
    if run_ingestion in ['y', 'yes']:
        # Ask for countries
        print("\nAvailable countries: US, CA, GB, DE, FR, NL, AU, JP")
        countries_input = input("Enter countries to fetch (comma-separated, or 'all'): ").strip()
        
        if countries_input.lower() == 'all':
            countries = ["US", "CA", "GB", "DE", "FR", "NL", "AU", "JP"]
        else:
            countries = [c.strip().upper() for c in countries_input.split(',')]
        
        # Ask for max stations
        max_stations = input("Max stations per country (default 100): ").strip()
        max_stations = int(max_stations) if max_stations.isdigit() else 100
        
        if not run_ocm_ingestion(countries, max_stations):
            print("❌ Data ingestion failed.")
            return False
    
    # Verify integration
    if not verify_integration():
        print("❌ Integration verification failed.")
        return False
    
    print("\n🎉 Setup Complete!")
    print("=" * 50)
    print("Your EV User Intelligence is now connected to Snowflake and ready to use!")
    print("\nNext steps:")
    print("1. Start the backend: cd backend && python -m uvicorn app:app --reload")
    print("2. Start the frontend: cd frontend && npm start")
    print("3. Access the platform at: http://localhost:3000")
    print("\nFor more information, see: PROJECT_SUMMARY.md")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1) 