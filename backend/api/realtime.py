from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json
from core.config import settings

try:
    from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
except Exception:
    AIOKafkaProducer = None
    AIOKafkaConsumer = None

router = APIRouter(prefix="/realtime", tags=["Realtime"])


class ConnectionManager:
    def __init__(self):
        self.active_home: Set[WebSocket] = set()
        self.active_map: Dict[str, WebSocket] = {}

    async def connect_home(self, websocket: WebSocket):
        await websocket.accept()
        self.active_home.add(websocket)

    def disconnect_home(self, websocket: WebSocket):
        self.active_home.discard(websocket)

    async def broadcast_home(self, message: dict):
        data = json.dumps(message)
        dead = []
        for ws in list(self.active_home):
            try:
                await ws.send_text(data)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect_home(ws)

    async def connect_map(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_map[user_id] = websocket

    def disconnect_map(self, user_id: str):
        if user_id in self.active_map:
            del self.active_map[user_id]

    async def broadcast_map(self, message: dict):
        data = json.dumps(message)
        dead_keys = []
        for uid, ws in list(self.active_map.items()):
            try:
                await ws.send_text(data)
            except Exception:
                dead_keys.append(uid)
        for uid in dead_keys:
            self.disconnect_map(uid)


manager = ConnectionManager()


@router.websocket("/home")
async def ws_home(websocket: WebSocket):
    await manager.connect_home(websocket)
    try:
        while True:
            # Home clients don't need to send; keep alive/read pings
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect_home(websocket)


@router.websocket("/map/{user_id}")
async def ws_map(websocket: WebSocket, user_id: str):
    await manager.connect_map(websocket, user_id)
    try:
        while True:
            # Expect location payloads from client
            raw = await websocket.receive_text()
            try:
                payload = json.loads(raw)
            except Exception:
                continue
            # Re-broadcast to all listeners (including dashboards)
            await manager.broadcast_map({
                "type": "location_update",
                "user_id": user_id,
                "location": payload.get("location"),
                "name": payload.get("name"),
                "timestamp": payload.get("timestamp")
            })
    except WebSocketDisconnect:
        manager.disconnect_map(user_id)


# Optional Kafka consumer tasks (to be started from app startup) to fan-out to websockets
async def start_kafka_home_consumer():
    if not AIOKafkaConsumer:
        return None
    consumer = AIOKafkaConsumer(
        settings.KAFKA_HOME_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        enable_auto_commit=True,
        value_deserializer=lambda v: v
    )
    await consumer.start()

    async def _run():
        try:
            async for msg in consumer:
                try:
                    data = json.loads(msg.value.decode("utf-8"))
                except Exception:
                    continue
                await manager.broadcast_home(data)
        finally:
            await consumer.stop()
    return _run


async def start_kafka_location_consumer():
    if not AIOKafkaConsumer:
        return None
    consumer = AIOKafkaConsumer(
        settings.KAFKA_LOCATION_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        enable_auto_commit=True,
        value_deserializer=lambda v: v
    )
    await consumer.start()

    async def _run():
        try:
            async for msg in consumer:
                try:
                    data = json.loads(msg.value.decode("utf-8"))
                except Exception:
                    continue
                await manager.broadcast_map(data)
        finally:
            await consumer.stop()
    return _run


