\"\"\"完整聊天应用\"\"\"

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from pydantic import BaseModel
from datetime import datetime
from collections import defaultdict
import json

app = FastAPI()


class ChatMessage(BaseModel):
    type: str  # \"message\", \"join\", \"leave\", \"private\"
    room: str = \"general\"
    sender: str = \"\"
    content: str = \"\"
    target: str = \"\"  # 私聊目标
    timestamp: str = \"\"


class ChatServer:
    def __init__(self):
        self.connections: dict[str, WebSocket] = {}  # nickname -> ws
        self.rooms: dict[str, set[str]] = defaultdict(set)  # room -> nicknames
        self.message_history: dict[str, list[dict]] = defaultdict(list)

    async def connect(self, ws: WebSocket, nickname: str):
        await ws.accept()
        self.connections[nickname] = ws
        self.rooms[\"general\"].add(nickname)
        await self.broadcast(ChatMessage(
            type=\"join\", room=\"general\", sender=nickname,
            content=f\"{nickname} joined\", timestamp=datetime.now().isoformat()
        ))
        await ws.send_json({\"type\": \"connected\", \"nickname\": nickname})

    async def disconnect(self, nickname: str):
        ws = self.connections.pop(nickname, None)
        for room_name in list(self.rooms.keys()):
            self.rooms[room_name].discard(nickname)
            await self.broadcast(ChatMessage(
                type=\"leave\", room=room_name, sender=nickname,
                content=f\"{nickname} left\", timestamp=datetime.now().isoformat()
            ), room=room_name)

    async def handle_message(self, nickname: str, msg: ChatMessage):
        msg.sender = nickname
        msg.timestamp = datetime.now().isoformat()

        if msg.type == \"message\":
            self.message_history[msg.room].append(msg.model_dump())
            await self.broadcast(msg, room=msg.room)
        elif msg.type == \"private\" and msg.target:
            await self.send_to(msg.target, msg)
            await self.send_to(nickname, msg)

    async def broadcast(self, msg: ChatMessage, room: str = None, exclude: str = None):
        targets = self.rooms.get(room or msg.room, set()) if room else set(self.connections.keys())
        for nickname in targets:
            if nickname != exclude and nickname in self.connections:
                await self.connections[nickname].send_json(msg.model_dump())

    async def send_to(self, nickname: str, msg: ChatMessage):
        ws = self.connections.get(nickname)
        if ws:
            await ws.send_json(msg.model_dump())

    def get_online_users(self) -> list[str]:
        return list(self.connections.keys())

    def get_room_users(self, room: str) -> list[str]:
        return list(self.rooms.get(room, set()))


chat = ChatServer()


@app.websocket(\"/ws/chat\")
async def chat_endpoint(
    websocket: WebSocket,
    nickname: str = Query(...),
):
    await chat.connect(websocket, nickname)
    try:
        while True:
            data = await websocket.receive_json()
            msg = ChatMessage(**data)
            await chat.handle_message(nickname, msg)
    except WebSocketDisconnect:
        await chat.disconnect(nickname)


@app.get(\"/api/online\")
async def online_users():
    return {\"users\": chat.get_online_users()}


@app.get(\"/api/rooms/{room}/users\")
async def room_users(room: str):
    return {\"room\": room, \"users\": chat.get_room_users(room)}


@app.get(\"/api/rooms/{room}/history\")
async def room_history(room: str, limit: int = 50):
    return {\"room\": room, \"messages\": chat.message_history[room][-limit:]}
