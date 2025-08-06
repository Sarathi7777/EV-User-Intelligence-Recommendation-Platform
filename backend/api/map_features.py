from fastapi import APIRouter, Body, Query, HTTPException
from typing import List, Optional
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from db.snowflake_connector import get_snowflake_manager

router = APIRouter(prefix="/map", tags=["MapFeatures"])

@router.post("/user-location")
def update_user_location(
    user_id: int = Body(...),
    latitude: float = Body(...),
    longitude: float = Body(...),
    status: str = Body('active'),
    message: Optional[str] = Body(None),
    contact_method: Optional[str] = Body(None)
):
    """Update or insert the current user's location."""
    manager = get_snowflake_manager()
    if not manager:
        raise HTTPException(status_code=503, detail="Snowflake not available")
    manager.upsert_user_location(user_id, latitude, longitude, status, message, contact_method)
    return {"success": True}

@router.get("/nearby-users")
def get_nearby_users(
    latitude: float = Query(...),
    longitude: float = Query(...),
    radius_km: float = Query(10)
):
    """Get users within a radius (km) of a location."""
    manager = get_snowflake_manager()
    if not manager:
        raise HTTPException(status_code=503, detail="Snowflake not available")
    users = manager.get_nearby_users(latitude, longitude, radius_km)
    return {"users": users}

@router.get("/nearby-ev-stores")
def get_nearby_ev_stores(
    latitude: float = Query(...),
    longitude: float = Query(...),
    radius_km: float = Query(10)
):
    """Get EV stores within a radius (km) of a location."""
    manager = get_snowflake_manager()
    if not manager:
        raise HTTPException(status_code=503, detail="Snowflake not available")
    stores = manager.get_nearby_ev_stores(latitude, longitude, radius_km)
    return {"ev_stores": stores}

@router.get("/nearby-floating-services")
def get_nearby_floating_services(
    latitude: float = Query(...),
    longitude: float = Query(...),
    radius_km: float = Query(10)
):
    """Get floating services within a radius (km) of a location."""
    manager = get_snowflake_manager()
    if not manager:
        raise HTTPException(status_code=503, detail="Snowflake not available")
    services = manager.get_nearby_floating_services(latitude, longitude, radius_km)
    return {"floating_services": services}