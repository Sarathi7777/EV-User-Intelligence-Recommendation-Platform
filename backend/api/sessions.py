from fastapi import APIRouter
import json
import os
# from backend.models.schemas import UserSession
from models.schemas import UserSession

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.post("/")
def log_session(session: UserSession):
    """Log a user charging session to mock data."""
    try:
        mock_data_path = "mock_data/sessions.json"
        sessions = []
        if os.path.exists(mock_data_path):
            with open(mock_data_path, 'r') as f:
                sessions = json.load(f)
        
        # Add new session
        new_session = {
            "id": len(sessions) + 1,
            "user_id": session.user_id,
            "station_id": session.station_id,
            "timestamp": session.timestamp
        }
        sessions.append(new_session)
        
        # Save updated sessions
        with open(mock_data_path, 'w') as f:
            json.dump(sessions, f, indent=2)
        
        return {"status": "success", "message": "Session logged"}
    except Exception as e:
        print(f"Error logging session: {e}")
        return {"status": "error", "message": "Failed to log session"}