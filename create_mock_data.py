#!/usr/bin/env python3
"""
Create mock data for testing the EV User Intelligence
"""

import json
import os
from datetime import datetime, timedelta
import random

def create_mock_stations():
    """Create mock station data."""
    stations = [
        {
            "id": 1,
            "name": "Downtown Charging Station",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "energy_type": "Level 2",
            "available": True
        },
        {
            "id": 2,
            "name": "Mall Parking Garage",
            "latitude": 37.7849,
            "longitude": -122.4094,
            "energy_type": "DC Fast",
            "available": False
        },
        {
            "id": 3,
            "name": "Airport Terminal A",
            "latitude": 37.7949,
            "longitude": -122.3994,
            "energy_type": "Level 2",
            "available": True
        },
        {
            "id": 4,
            "name": "Shopping Center",
            "latitude": 37.8049,
            "longitude": -122.3894,
            "energy_type": "Level 1",
            "available": True
        },
        {
            "id": 5,
            "name": "Office Building",
            "latitude": 37.8149,
            "longitude": -122.3794,
            "energy_type": "DC Fast",
            "available": True
        },
        {
            "id": 6,
            "name": "University Campus",
            "latitude": 37.8249,
            "longitude": -122.3694,
            "energy_type": "Level 2",
            "available": True
        },
        {
            "id": 7,
            "name": "Hospital Parking",
            "latitude": 37.8349,
            "longitude": -122.3594,
            "energy_type": "Level 2",
            "available": False
        },
        {
            "id": 8,
            "name": "Public Library",
            "latitude": 37.8449,
            "longitude": -122.3494,
            "energy_type": "Level 1",
            "available": True
        }
    ]
    
    os.makedirs('mock_data', exist_ok=True)
    with open('mock_data/stations.json', 'w') as f:
        json.dump(stations, f, indent=2)
    
    print(f"✅ Created {len(stations)} mock stations")
    return stations

def create_mock_users():
    """Create mock user data."""
    users = [
        {
            "id": 1,
            "email": "user1@example.com",
            "password_hash": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",  # "123"
            "eco_score": 85.5
        },
        {
            "id": 2,
            "email": "user2@example.com",
            "password_hash": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",  # "123"
            "eco_score": 72.3
        },
        {
            "id": 3,
            "email": "admin@example.com",
            "password_hash": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",  # "123"
            "eco_score": 90.0
        }
    ]
    
    with open('mock_data/users.json', 'w') as f:
        json.dump(users, f, indent=2)
    
    print(f"✅ Created {len(users)} mock users")
    return users

def create_mock_sessions():
    """Create mock session data."""
    sessions = []
    base_date = datetime.now() - timedelta(days=30)
    
    for i in range(20):
        session = {
            "id": i + 1,
            "user_id": random.randint(1, 3),
            "station_id": random.randint(1, 8),
            "timestamp": (base_date + timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))).isoformat()
        }
        sessions.append(session)
    
    with open('mock_data/sessions.json', 'w') as f:
        json.dump(sessions, f, indent=2)
    
    print(f"✅ Created {len(sessions)} mock sessions")
    return sessions

def main():
    print("📊 Creating Mock Data for EV User Intelligence")
    print("=" * 50)
    
    create_mock_stations()
    create_mock_users()
    create_mock_sessions()
    
    print("\n🎉 All mock data created successfully!")
    print("📁 Data saved in mock_data/ directory")

if __name__ == "__main__":
    main() 