#!/usr/bin/env python3
"""
Test Script for Snowflake Integration
====================================

This script tests the complete Snowflake integration including:
1. Connection to Snowflake
2. Database table creation
3. Open Charge Map API connection
4. Data ingestion and storage
5. Query functionality

Usage:
    python test_snowflake_integration.py
"""

import os
import sys
import json
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent))

def test_snowflake_connection():
    """Test basic Snowflake connection."""
    print("🔍 Testing Snowflake connection...")
    
    try:
        from db.snowflake_connector import SnowflakeManager
        
        manager = SnowflakeManager()
        result = manager.execute_query("SELECT CURRENT_VERSION() as version, CURRENT_USER() as user")
        
        if result:
            print(f"✅ Snowflake connection successful!")
            print(f"   Version: {result[0]['version']}")
            print(f"   User: {result[0]['user']}")
            return True
        else:
            print("❌ No response from Snowflake")
            return False
            
    except Exception as e:
        print(f"❌ Snowflake connection failed: {e}")
        return False

def test_table_creation():
    """Test database table creation."""
    print("\n🔍 Testing table creation...")
    
    try:
        from db.snowflake_connector import SnowflakeManager
        
        manager = SnowflakeManager()
        manager.create_tables()
        
        # Verify tables exist
        tables = ["stations", "users", "sessions", "station_usage"]
        for table in tables:
            result = manager.execute_query(f"SHOW TABLES LIKE '{table}'")
            if result:
                print(f"✅ Table '{table}' created successfully")
            else:
                print(f"❌ Table '{table}' not found")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Table creation failed: {e}")
        return False

def test_ocm_api():
    """Test Open Charge Map API connection."""
    print("\n🔍 Testing Open Charge Map API...")
    
    try:
        import requests
        
        api_key = os.getenv("OCM_API_KEY")
        if not api_key:
            print("❌ OCM_API_KEY not found in environment")
            return False
        
        url = "https://api.openchargemap.io/v3/poi"
        params = {
            "key": api_key,
            "output": "json",
            "maxresults": 5,
            "compact": "true"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data:
            print(f"✅ Open Charge Map API connection successful!")
            print(f"   Sample stations: {len(data)}")
            for i, station in enumerate(data[:3]):
                name = station.get("AddressInfo", {}).get("Title", "Unknown")
                print(f"   {i+1}. {name}")
            return True
        else:
            print("❌ Open Charge Map API returned no data")
            return False
            
    except Exception as e:
        print(f"❌ Open Charge Map API test failed: {e}")
        return False

def test_data_ingestion():
    """Test data ingestion with a small sample."""
    print("\n🔍 Testing data ingestion...")
    
    try:
        from db.fetch_and_store_ocm import OpenChargeMapFetcher
        
        fetcher = OpenChargeMapFetcher()
        
        # Test with a small sample (US, 10 stations)
        results = fetcher.run_full_ingestion(["US"], max_stations_per_country=10)
        
        print(f"✅ Data ingestion test completed!")
        print(f"   Fetched: {results['summary']['total_fetched']} stations")
        print(f"   Stored: {results['summary']['total_stored']} stations")
        
        return results['summary']['total_stored'] > 0
        
    except Exception as e:
        print(f"❌ Data ingestion test failed: {e}")
        return False

def test_query_functionality():
    """Test query functionality."""
    print("\n🔍 Testing query functionality...")
    
    try:
        from db.snowflake_connector import SnowflakeManager
        
        manager = SnowflakeManager()
        
        # Test station count
        count = manager.get_station_count()
        print(f"✅ Station count: {count}")
        
        # Test getting stations
        stations = manager.get_stations(limit=5)
        print(f"✅ Retrieved {len(stations)} sample stations")
        
        # Test location-based query
        if stations:
            sample_station = stations[0]
            lat, lon = sample_station['latitude'], sample_station['longitude']
            nearby = manager.get_stations_by_location(lat, lon, 10)
            print(f"✅ Location query: {len(nearby)} stations within 10km")
        
        return True
        
    except Exception as e:
        print(f"❌ Query functionality test failed: {e}")
        return False

def test_api_integration():
    """Test API integration."""
    print("\n🔍 Testing API integration...")
    
    try:
        from backend.api.stations import get_stations, get_station_count
        
        # Test getting stations via API
        stations = get_stations()
        print(f"✅ API stations endpoint: {len(stations)} stations")
        
        # Test station count via API
        count_info = get_station_count()
        print(f"✅ API count endpoint: {count_info}")
        
        return True
        
    except Exception as e:
        print(f"❌ API integration test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and provide summary."""
    print("🚗 EV User Intelligence - Snowflake Integration Test")
    print("=" * 50)
    
    # Check if .env file exists
    env_path = Path("backend/.env")
    if not env_path.exists():
        print("❌ No .env file found. Please run setup_snowflake_integration.py first.")
        return False
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv(env_path)
    
    tests = [
        ("Snowflake Connection", test_snowflake_connection),
        ("Table Creation", test_table_creation),
        ("Open Charge Map API", test_ocm_api),
        ("Data Ingestion", test_data_ingestion),
        ("Query Functionality", test_query_functionality),
        ("API Integration", test_api_integration)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results[test_name] = False
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your Snowflake integration is working correctly.")
        print("\nNext steps:")
        print("1. Start the backend: cd backend && python -m uvicorn app:app --reload")
        print("2. Start the frontend: cd frontend && npm start")
        print("3. Access the platform at: http://localhost:3000")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Verify your .env file configuration")
        print("2. Check your Snowflake credentials")
        print("3. Ensure your OCM API key is valid")
        print("4. Review the SNOWFLAKE_INTEGRATION.md guide")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1) 