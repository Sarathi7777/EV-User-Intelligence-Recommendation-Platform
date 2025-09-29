from fastapi import APIRouter
import json
import os
# from backend.models.schemas import UserSession
from models.schemas import UserSession
from typing import List
from fastapi import HTTPException
from fastapi import WebSocket
from core.config import settings
from asyncio import create_task

try:
    from aiokafka import AIOKafkaProducer
except Exception:
    AIOKafkaProducer = None

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

        # Emit Kafka event for home realtime stream if Kafka is available
        if AIOKafkaProducer:
            try:
                import asyncio
                async def _send():
                    producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)
                    await producer.start()
                    try:
                        payload = json.dumps({
                            "type": "session_created",
                            "session": new_session
                        }).encode("utf-8")
                        await producer.send_and_wait(settings.KAFKA_HOME_TOPIC, payload)
                    finally:
                        await producer.stop()
                asyncio.get_event_loop().create_task(_send())
            except Exception as e:
                print(f"Warning: failed to emit Kafka event: {e}")

        # Also broadcast directly to WebSocket home clients (works without Kafka)
        try:
            from api.realtime import manager as realtime_manager
            async def _broadcast():
                await realtime_manager.broadcast_home({
                    "type": "session_created",
                    "session": new_session
                })
            create_task(_broadcast())
        except Exception as e:
            print(f"Warning: failed to broadcast home WS: {e}")

        return {"status": "success", "message": "Session logged", "id": new_session["id"]}
    except Exception as e:
        print(f"Error logging session: {e}")
        return {"status": "error", "message": "Failed to log session"}

@router.get("/")
def list_sessions() -> List[dict]:
    """List recent sessions for home page."""
    try:
        mock_data_path = "mock_data/sessions.json"
        if os.path.exists(mock_data_path):
            with open(mock_data_path, 'r') as f:
                sessions = json.load(f)
            # Return latest first
            sessions.sort(key=lambda s: s.get("timestamp", ""), reverse=True)
            return sessions
        return []
    except Exception as e:
        print(f"Error reading sessions: {e}")
        raise HTTPException(status_code=500, detail="Failed to read sessions")