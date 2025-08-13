from fastapi import APIRouter, Query, HTTPException
import json
import os
import sys
import requests
import math
from typing import List, Optional
from models.schemas import Station, NearbyStation
# from backend.models.schemas import Station, NearbyStation

# Add parent directory to path to access db module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
router = APIRouter(prefix="/stations", tags=["Stations"])

# Lazy import and initialization of Snowflake manager
def get_snowflake_manager():
    """Get SnowflakeManager instance with lazy initialization."""
    try:
        from db.snowflake_connector import SnowflakeManager
        return SnowflakeManager()
    except Exception as e:
        print(f"Snowflake not available: {e}")
        return None

def is_snowflake_available():
    """Check if Snowflake is available."""
    try:
        manager = get_snowflake_manager()
        return manager is not None
    except:
        return False

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points using Haversine formula."""
    R = 6371  # Earth's radius in kilometers
    
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

def estimate_travel_time(distance_km: float, avg_speed_kmh: float = 30) -> int:
    """Estimate travel time in minutes."""
    return int((distance_km / avg_speed_kmh) * 60)

def fetch_ocm_stations(lat: float, lon: float, radius: float = 10) -> List[dict]:
    """Fetch stations from Open Charge Map API."""
    try:
        ocm_api_key = os.getenv("OCM_API_KEY", "")
        if not ocm_api_key:
            return []
        
        url = "https://api.openchargemap.io/v3/poi"
        params = {
            "key": ocm_api_key,
            "latitude": lat,
            "longitude": lon,
            "distance": radius,
            "distanceunit": "km",
            "maxresults": 50,
            "compact": True,
            "verbose": False
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"OCM API error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching OCM stations: {e}")
        return []

def get_stations_from_snowflake() -> List[Station]:
    """Get stations from Snowflake database."""
    try:
        snowflake_manager = get_snowflake_manager()
        if not snowflake_manager:
            return []
        
        # Get stations from Snowflake
        stations_data = snowflake_manager.get_stations(limit=1000)
        
        stations = []
        for station in stations_data:
            stations.append(Station(
                id=station["id"],
                name=station["name"],
                latitude=station["latitude"],
                longitude=station["longitude"],
                energy_type=station["energy_type"],
                available=station["available"]
            ))
        
        return stations
        
    except Exception as e:
        print(f"Error getting stations from Snowflake: {e}")
        return []

def get_stations_from_mock() -> List[Station]:
    """Get stations from mock data (fallback)."""
    try:
        mock_data_path = "mock_data/stations.json"
        if os.path.exists(mock_data_path):
            with open(mock_data_path, 'r') as f:
                stations_data = json.load(f)
            return [Station(
                id=station["id"],
                name=station["name"],
                latitude=station["latitude"],
                longitude=station["longitude"],
                energy_type=station["energy_type"],
                available=station["available"]
            ) for station in stations_data]
        else:
            return [
                Station(id=1, name="Downtown Station", latitude=10.877185, longitude=77.005055, energy_type="Level 2", available=True),
                Station(id=2, name="Mall Station", latitude=10.902898, longitude=76.998908, energy_type="DC Fast", available=False),
                # Station(id=3, name="Airport Station", latitude=10.877185, longitude=77.005055, energy_type="Level 2", available=True)
                Station(id=3, name="Airport Station", latitude=11.006018, longitude=76.977751, energy_type="Level 2", available=True),
                Station(id=3, name="Airport Station", latitude=10.955346, longitude=76.969398, energy_type="Level 2", available=True),
                # Station(id=3, name="Airport Station", latitude=10.877185, longitude=77.005055, energy_type="Level 2", available=True)
            ]
    except Exception as e:
        print(f"Error loading mock stations: {e}")
        return [
            Station(id=1, name="Downtown Station", latitude=10.877185, longitude=77.005055, energy_type="Level 2", available=True),
            Station(id=2, name="Mall Station", latitude=10.902898, longitude=76.998908, energy_type="DC Fast", available=False),
            # Station(id=3, name="Airport Station", latitude=10.877185, longitude=77.005055, energy_type="Level 2", available=True)
            Station(id=3, name="Airport Station", latitude=11.006018, longitude=76.977751, energy_type="Level 2", available=True),
            Station(id=3, name="Airport Station", latitude=10.955346, longitude=76.969398, energy_type="Level 2", available=True),
        ]

@router.get("/", response_model=List[Station])
def get_stations():
    """Fetch all charging stations from Snowflake or mock data."""
    try:
        # Try to get stations from Snowflake first
        if is_snowflake_available():
            stations = get_stations_from_snowflake()
            if stations:
                return stations
        
        # Fallback to mock data
        return get_stations_from_mock()
        
    except Exception as e:
        print(f"Error loading stations: {e}")
        return get_stations_from_mock()

@router.get("/nearby", response_model=List[NearbyStation])
def get_nearby_stations(
    lat: float = Query(..., description="User's latitude"),
    lon: float = Query(..., description="User's longitude"),
    radius: float = Query(10, description="Search radius in kilometers"),
    use_ocm: bool = Query(True, description="Use Open Charge Map API"),
    use_snowflake: bool = Query(True, description="Use Snowflake database"),
    limit: int = Query(5, description="Number of nearest stations to return")
):
    """Get nearby charging stations with distance and time calculations."""
    try:
        nearby_stations = []
        
        # Get stations from Snowflake if available
        if use_snowflake and is_snowflake_available():
            try:
                snowflake_manager = get_snowflake_manager()
                snowflake_stations = snowflake_manager.get_stations_by_location(lat, lon, radius)
                
                for station in snowflake_stations:
                    distance = station.get('distance_km', 0)
                    if distance <= radius:
                        travel_time = estimate_travel_time(distance)
                        nearby_stations.append(NearbyStation(
                            id=str(station["id"]),
                            name=station["name"],
                            latitude=station["latitude"],
                            longitude=station["longitude"],
                            energy_type=station["energy_type"],
                            available=station["available"],
                            distance_km=round(distance, 2),
                            travel_time_minutes=travel_time,
                            source="snowflake"
                        ))
            except Exception as e:
                print(f"Error getting stations from Snowflake: {e}")
        
        # Get mock stations if Snowflake is not available or empty
        if not nearby_stations:
            mock_data_path = "mock_data/stations.json"
            mock_stations = []
            if os.path.exists(mock_data_path):
                with open(mock_data_path, 'r') as f:
                    mock_stations = json.load(f)
            
            # Calculate distances for mock stations
            for station in mock_stations:
                distance = calculate_distance(lat, lon, station["latitude"], station["longitude"])
                if distance <= radius:
                    travel_time = estimate_travel_time(distance)
                    nearby_stations.append(NearbyStation(
                        id=str(station["id"]),
                        name=station["name"],
                        latitude=station["latitude"],
                        longitude=station["longitude"],
                        energy_type=station["energy_type"],
                        available=station["available"],
                        distance_km=round(distance, 2),
                        travel_time_minutes=travel_time,
                        source="mock"
                    ))
        
        # Fetch from Open Charge Map API if enabled
        if use_ocm:
            ocm_stations = fetch_ocm_stations(lat, lon, radius)
            for station in ocm_stations:
                try:
                    # Extract station data from OCM response
                    station_lat = station.get("AddressInfo", {}).get("Latitude", 0)
                    station_lon = station.get("AddressInfo", {}).get("Longitude", 0)
                    
                    if station_lat and station_lon:
                        distance = calculate_distance(lat, lon, station_lat, station_lon)
                        if distance <= radius:
                            travel_time = estimate_travel_time(distance)
                            
                            # Get station name
                            station_name = station.get("AddressInfo", {}).get("Title", "Unknown Station")
                            if not station_name or station_name == "Unknown Station":
                                station_name = f"Station at {station.get('AddressInfo', {}).get('AddressLine1', 'Unknown Location')}"
                            
                            # Get connection info
                            connections = station.get("Connections", [])
                            energy_types = []
                            for conn in connections:
                                connection_type = conn.get("ConnectionType", {}).get("Title", "Unknown")
                                if connection_type not in energy_types:
                                    energy_types.append(connection_type)
                            
                            energy_type = ", ".join(energy_types) if energy_types else "Unknown"
                            
                            nearby_stations.append(NearbyStation(
                                id=f"ocm_{station.get('ID', len(nearby_stations) + 1000)}",
                                name=station_name,
                                latitude=station_lat,
                                longitude=station_lon,
                                energy_type=energy_type,
                                available=True,  # OCM doesn't provide real-time availability
                                distance_km=round(distance, 2),
                                travel_time_minutes=travel_time,
                                source="ocm"
                            ))
                except Exception as e:
                    print(f"Error processing OCM station: {e}")
                    continue
        
        # Sort by distance
        nearby_stations.sort(key=lambda x: x.distance_km)
        
        return nearby_stations[:limit]  # Return top N nearest stations
        
    except Exception as e:
        print(f"Error getting nearby stations: {e}")
        return []

@router.get("/count")
def get_station_count():
    """Get total number of stations in the database."""
    try:
        snowflake_manager = get_snowflake_manager()
        if snowflake_manager:
            count = snowflake_manager.get_station_count()
            return {"count": count, "source": "snowflake"}
        else:
            # Count mock stations
            mock_stations = get_stations_from_mock()
            return {"count": len(mock_stations), "source": "mock"}
    except Exception as e:
        print(f"Error getting station count: {e}")
        return {"count": 0, "source": "error"}

@router.get("/statistics")
def get_station_statistics():
    """Get station statistics from Snowflake."""
    try:
        snowflake_manager = get_snowflake_manager()
        if not snowflake_manager:
            raise HTTPException(status_code=503, detail="Snowflake not available")
        
        # Get statistics from Snowflake
        query = """
            SELECT 
                COUNT(*) as total_stations,
                COUNT(DISTINCT country) as countries,
                COUNT(DISTINCT energy_type) as energy_types,
                AVG(CASE WHEN available THEN 1 ELSE 0 END) * 100 as availability_percentage
            FROM stations
        """
        
        result = snowflake_manager.execute_query(query)
        if result:
            return {
                "total_stations": result[0]["total_stations"],
                "countries": result[0]["countries"],
                "energy_types": result[0]["energy_types"],
                "availability_percentage": round(result[0]["availability_percentage"], 2)
            }
        else:
            return {"error": "No statistics available"}
            
    except Exception as e:
        print(f"Error getting statistics: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting statistics: {e}")