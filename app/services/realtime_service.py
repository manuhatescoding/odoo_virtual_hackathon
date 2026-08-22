import asyncio
from typing import Set

from fastapi import WebSocket


class RealtimeManager:
    def __init__(self):
        self.connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.connections.discard(websocket)

    async def broadcast(self, event: str):
        stale = set()
        for websocket in self.connections:
            try:
                await websocket.send_json({"event": event})
            except Exception:
                stale.add(websocket)
        self.connections -= stale


manager = RealtimeManager()


async def heartbeat(websocket: WebSocket):
    while True:
        await asyncio.sleep(20)
        await websocket.send_json({"event": "heartbeat"})
