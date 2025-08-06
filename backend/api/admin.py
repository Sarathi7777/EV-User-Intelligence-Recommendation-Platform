from fastapi import APIRouter, HTTPException
import json
import os
# from backend.models.schemas import Station, UserResponse
from models.schemas import Station, UserResponse
from db.snowflake_connector import get_snowflake_manager
from datetime import datetime, timedelta

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users", response_model=list[UserResponse])
def get_users():
    """Get all users from mock data."""
    try:
        mock_data_path = "mock_data/users.json"
        if os.path.exists(mock_data_path):
            with open(mock_data_path, 'r') as f:
                users_data = json.load(f)
            
            return [UserResponse(
                id=user["id"],
                email=user["email"],
                eco_score=user["eco_score"]
            ) for user in users_data]
        else:
            # Return sample users if mock data doesn't exist
            return [
                UserResponse(id=1, email="user1@example.com", eco_score=85.5),
                UserResponse(id=2, email="user2@example.com", eco_score=72.3),
                UserResponse(id=3, email="admin@example.com", eco_score=90.0)
            ]
    except Exception as e:
        print(f"Error loading users: {e}")
        raise HTTPException(status_code=500, detail="Failed to load users")

@router.post("/stations")
def create_station(station: Station):
    """Create a new station in mock data."""
    try:
        mock_data_path = "mock_data/stations.json"
        stations = []
        if os.path.exists(mock_data_path):
            with open(mock_data_path, 'r') as f:
                stations = json.load(f)
        
        # Add new station
        new_station = {
            "id": station.id,
            "name": station.name,
            "latitude": station.latitude,
            "longitude": station.longitude,
            "energy_type": station.energy_type,
            "available": station.available
        }
        stations.append(new_station)
        
        # Save updated stations
        with open(mock_data_path, 'w') as f:
            json.dump(stations, f, indent=2)
        
        return {"status": "success", "message": "Station created"}
    except Exception as e:
        print(f"Error creating station: {e}")
        raise HTTPException(status_code=500, detail="Failed to create station")

@router.delete("/stations/{station_id}")
def delete_station(station_id: int):
    """Delete a station from mock data."""
    try:
        mock_data_path = "mock_data/stations.json"
        if os.path.exists(mock_data_path):
            with open(mock_data_path, 'r') as f:
                stations = json.load(f)
            
            # Remove station with matching ID
            stations = [s for s in stations if s["id"] != station_id]
            
            # Save updated stations
            with open(mock_data_path, 'w') as f:
                json.dump(stations, f, indent=2)
        
        return {"status": "success", "message": "Station deleted"}
    except Exception as e:
        print(f"Error deleting station: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete station") 

@router.get("/analytics/user-growth")
def user_growth(days: int = 30):
    """Return user registration count per day for the last N days."""
    manager = get_snowflake_manager()
    if not manager:
        raise HTTPException(status_code=503, detail="Snowflake not available")
    query = f'''
        SELECT TO_DATE(created_at) as date, COUNT(*) as count
        FROM users
        WHERE created_at >= DATEADD(day, -{days}, CURRENT_DATE())
        GROUP BY date
        ORDER BY date
    '''
    return manager.execute_query(query)

@router.get("/analytics/session-stats")
def session_stats(days: int = 30):
    """Return session count and total energy per day for the last N days."""
    manager = get_snowflake_manager()
    if not manager:
        raise HTTPException(status_code=503, detail="Snowflake not available")
    query = f'''
        SELECT TO_DATE(start_time) as date, COUNT(*) as sessions, SUM(energy_consumed_kwh) as total_energy
        FROM sessions
        WHERE start_time >= DATEADD(day, -{days}, CURRENT_DATE())
        GROUP BY date
        ORDER BY date
    '''
    return manager.execute_query(query)

@router.get("/analytics/station-usage")
def station_usage(top: int = 5):
    """Return top N stations by total sessions."""
    manager = get_snowflake_manager()
    if not manager:
        raise HTTPException(status_code=503, detail="Snowflake not available")
    query = f'''
        SELECT s.id, s.name, COUNT(sess.id) as total_sessions
        FROM stations s
        LEFT JOIN sessions sess ON s.id = sess.station_id
        GROUP BY s.id, s.name
        ORDER BY total_sessions DESC
        LIMIT {top}
    '''
    return manager.execute_query(query) 