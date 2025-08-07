#!/usr/bin/env python3
"""
Test script for the EV User Intelligence
"""

import requests
import json
import time

def test_backend():
    """Test the backend API endpoints."""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing EV User Intelligence Backend")
    print("=" * 50)
    
    # Test 1: Get stations
    try:
        response = requests.get(f"{base_url}/stations")
        if response.status_code == 200:
            stations = response.json()
            print(f"✅ Stations API: {len(stations)} stations loaded")
            for station in stations[:3]:  # Show first 3 stations
                print(f"   - {station['name']} ({station['energy_type']})")
        else:
            print(f"❌ Stations API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Stations API error: {e}")
    
    # Test 2: User login
    try:
        login_data = {"email": "user1@example.com", "password": "123"}
        response = requests.post(f"{base_url}/login", json=login_data)
        if response.status_code == 200:
            user = response.json()
            print(f"✅ Login API: User {user['email']} logged in (Eco Score: {user['eco_score']})")
        else:
            print(f"❌ Login API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Login API error: {e}")
    
    # Test 3: Get recommendations
    try:
        response = requests.post(f"{base_url}/recommendations?user_id=1")
        if response.status_code == 200:
            recs = response.json()
            print(f"✅ Recommendations API: {len(recs['recommended_station_ids'])} recommendations")
        else:
            print(f"❌ Recommendations API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Recommendations API error: {e}")
    
    # Test 4: Get forecast
    try:
        response = requests.get(f"{base_url}/forecast/energy-demand?days=7")
        if response.status_code == 200:
            forecast = response.json()
            print(f"✅ Forecast API: {len(forecast['predicted_demand_kwh'])} days forecast")
        else:
            print(f"❌ Forecast API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Forecast API error: {e}")
    
    # Test 5: Admin users
    try:
        response = requests.get(f"{base_url}/admin/users")
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Admin Users API: {len(users)} users loaded")
        else:
            print(f"❌ Admin Users API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Admin Users API error: {e}")

def test_frontend():
    """Test if frontend is accessible."""
    print("\n🌐 Testing Frontend")
    print("=" * 30)
    
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is accessible at http://localhost:3000")
        else:
            print(f"❌ Frontend returned status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Frontend not accessible - make sure to run 'npm start' in frontend/")
    except Exception as e:
        print(f"❌ Frontend test error: {e}")

def main():
    print("🚗 EV User Intelligence Testing Suite")
    print("=" * 60)
    
    # Wait a moment for backend to start
    print("⏳ Waiting for backend to start...")
    time.sleep(3)
    
    # Test backend
    test_backend()
    
    # Test frontend
    test_frontend()
    
    print("\n🎉 Testing Complete!")
    print("\n📋 Next Steps:")
    print("1. Open http://localhost:3000 in your browser")
    print("2. Login with: user1@example.com / 123")
    print("3. Explore the interactive map and features")
    print("4. Check API docs at: http://localhost:8000/docs")

if __name__ == "__main__":
    main() 