from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List

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
    email: EmailStr
    password: str = Field(..., min_length=3, max_length=128)

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    eco_score: float
    access_token: Optional[str] = None

class RecommendationResponse(BaseModel):
    user_id: int
    recommended_station_ids: List[int]

# --- New Models for Advanced Features ---
class UserLocationIn(BaseModel):
    user_id: int
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    status: Optional[str] = Field('active', pattern='^(active|hidden|offline)$')
    message: Optional[str] = Field(None, max_length=200)
    contact_method: Optional[str] = Field(None, max_length=100)

class UserLocationOut(UserLocationIn):
    last_updated: str
    email: Optional[EmailStr] = None
    eco_score: Optional[float] = None

class EVStoreIn(BaseModel):
    name: str
    store_type: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    address: Optional[str]
    contact: Optional[str]
    hours: Optional[str]
    services: Optional[str]
    website: Optional[str]

class EVStoreOut(EVStoreIn):
    id: int
    created_at: str
    distance_km: Optional[float] = None

class FloatingServiceIn(BaseModel):
    name: str
    service_type: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    contact: Optional[str]
    hours: Optional[str]
    description: Optional[str]
    website: Optional[str]

class FloatingServiceOut(FloatingServiceIn):
    id: int
    created_at: str
    distance_km: Optional[float] = None