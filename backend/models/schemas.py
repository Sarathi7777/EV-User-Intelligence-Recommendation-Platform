from pydantic import BaseModel

class Station(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    energy_type: str
    available: bool

class NearbyStation(BaseModel):
    id: str
    name: str
    latitude: float
    longitude: float
    energy_type: str
    available: bool
    distance_km: float
    travel_time_minutes: int
    source: str  # "mock" or "ocm"

class UserSession(BaseModel):
    user_id: int
    station_id: int
    timestamp: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    eco_score: float

class RecommendationResponse(BaseModel):
    user_id: int
    recommended_station_ids: list[int]