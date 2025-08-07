from fastapi import APIRouter, Body, Query, HTTPException, Depends, Response, WebSocket, WebSocketDisconnect
from typing import List, Set
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from db.snowflake_connector import get_snowflake_manager
from models.schemas import UserLocationIn, UserLocationOut, EVStoreOut, FloatingServiceOut

router = APIRouter(prefix="/map", tags=["MapFeatures"])

# In-memory set of connected WebSocket clients
active_connections: Set[WebSocket] = set()

@router.post("/user-location", response_model=dict)
def update_user_location(payload: UserLocationIn, response: Response):
    manager = get_snowflake_manager()
    if not manager:
        raise HTTPException(status_code=503, detail="Snowflake not available")
    manager.upsert_user_location(
        user_id=payload.user_id,
        latitude=payload.latitude,
        longitude=payload.longitude,
        status=payload.status,
        message=payload.message,
        contact_method=payload.contact_method
    )
    return {"success": True}

@router.get("/nearby-users", response_model=List[UserLocationOut])
def get_nearby_users(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(10, gt=0, le=100)
):
    manager = get_snowflake_manager()
    if not manager:
        raise HTTPException(status_code=503, detail="Snowflake not available")
    users = manager.get_nearby_users(latitude, longitude, radius_km)
    return [UserLocationOut(**u) for u in users]

@router.get("/nearby-ev-stores", response_model=List[EVStoreOut])
def get_nearby_ev_stores(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(10, gt=0, le=100)
):
    manager = get_snowflake_manager()
    if not manager:
        raise HTTPException(status_code=503, detail="Snowflake not available")
    stores = manager.get_nearby_ev_stores(latitude, longitude, radius_km)
    return [EVStoreOut(**s) for s in stores]

@router.get("/nearby-floating-services", response_model=List[FloatingServiceOut])
def get_nearby_floating_services(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(10, gt=0, le=100)
):
    manager = get_snowflake_manager()
    if not manager:
        raise HTTPException(status_code=503, detail="Snowflake not available")
    services = manager.get_nearby_floating_services(latitude, longitude, radius_km)
    return [FloatingServiceOut(**s) for s in services]

@router.websocket("/ws/user-locations")
async def websocket_user_locations(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            # Broadcast received data to all clients
            for conn in list(active_connections):
                try:
                    await conn.send_json(data)
                except Exception:
                    pass
    except WebSocketDisconnect:
        active_connections.remove(websocket)
    except Exception:
        active_connections.remove(websocket)