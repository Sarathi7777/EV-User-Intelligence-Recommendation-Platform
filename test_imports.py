#!/usr/bin/env python3
"""
Quick test script to verify imports work correctly
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(__file__))

def test_snowflake_import():
    """Test importing SnowflakeManager"""
    try:
        from db.snowflake_connector import SnowflakeManager
        print("✅ Successfully imported SnowflakeManager from db.snowflake_connector")
        return True
    except ImportError as e:
        print(f"❌ Failed to import SnowflakeManager: {e}")
        return False

def test_stations_api_import():
    """Test importing the stations API"""
    try:
        # Change to backend directory context
        backend_path = os.path.join(os.path.dirname(__file__), 'backend')
        sys.path.insert(0, backend_path)
        
        from api import stations
        print("✅ Successfully imported stations API module")
        return True
    except ImportError as e:
        print(f"❌ Failed to import stations API: {e}")
        return False

def test_ocm_fetcher_import():
    """Test importing the OCM fetcher"""
    try:
        from db.fetch_and_store_ocm import OpenChargeMapFetcher
        print("✅ Successfully imported OpenChargeMapFetcher")
        return True
    except ImportError as e:
        print(f"❌ Failed to import OpenChargeMapFetcher: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing imports...")
    print("=" * 50)
    
    tests = [
        test_snowflake_import,
        test_ocm_fetcher_import,
        test_stations_api_import
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All imports working correctly!")
    else:
        print("⚠️ Some imports failed. Check the errors above.")