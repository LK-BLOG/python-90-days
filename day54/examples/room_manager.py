\"\"\"房间管理\"\"\"

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from datetime import datetime

app = FastAPI()


class Room:
    def __init__(self, name: str):
        self.name = name
        self.connections: list[WebSocket] = []
        self.created_at = datetime.now()

    async def join(self, ws: WebSocket, nickname: str):
        await ws.accept()
        self.connections.append(ws)
        await self.broadcast(f\"{nickname} joined the room\")

    def leave(self, ws: WebSocket, nickname: str):
        self.connections.remove(ws)

    async def broadcast(self, message: str, sender: WebSocket = None):
        for conn in self.connections:
            if conn != sender:
                await conn.send_text(message)


class RoomManager:
    def __init__(self):
        self.rooms: dict[str, Room] = {}

    def get_or_create(self, name: str) -> Room:
        if name not in self.rooms:
            self.rooms[name] = Room(name)
        return self.rooms[name]

    def list_rooms(self) -> list[dict]:
        return [
            {\"name\": r.name, \"users\": len(r.connections), \"created\": r.created_at.isoformat()}
            for r in self.rooms.values()
        ]


room_mgr = RoomManager()


@app.websocket(\"/ws/room/{room_name}\")
async def room_websocket(websocket: WebSocket, room_name: str):
    room = room_mgr.get_or_create(room_name)
    nickname = websocket.query_params.get(\"nickname\", \"Anonymous\")

    await room.join(websocket, nickname)
    try:
        while True:
            data = await websocket.receive_text()
            await room.broadcast(f\"[{room_name}] {nickname}: {data}\", sender=websocket)
    except WebSocketDisconnect:
        room.leave(websocket, nickname)
        await room.broadcast(f\"{nickname} left the room\")


@app.get(\"/rooms\")
async def list_rooms():
    return room_mgr.list_rooms()
