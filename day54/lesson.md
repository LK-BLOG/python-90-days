# Day 54 课程：WebSocket & 实时通信

## 第一部分：WebSocket基础

### 1.1 HTTP vs WebSocket
`
HTTP:   客户端请求 → 服务器响应（单向，无状态）
WebSocket: 双向持久连接（全双工，有状态）
`

### 1.2 握手过程
`
1. 客户端发送HTTP Upgrade请求
2. 服务器返回101 Switching Protocols
3. 升级为WebSocket协议
4. 双向数据传输
`

---

## 第二部分：FastAPI WebSocket

### 2.1 基本WebSocket
`python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
`

### 2.2 消息广播
`python
class ConnectionManager:
    def __init__(self):
        self.connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def broadcast(self, message: str, exclude: WebSocket = None):
        for conn in self.connections:
            if conn != exclude:
                await conn.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"User says: {data}", exclude=websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
`

### 2.3 房间管理
`python
class RoomManager:
    def __init__(self):
        self.rooms: dict[str, list[WebSocket]] = {}

    async def join(self, room: str, websocket: WebSocket):
        await websocket.accept()
        if room not in self.rooms:
            self.rooms[room] = []
        self.rooms[room].append(websocket)

    def leave(self, room: str, websocket: WebSocket):
        if room in self.rooms:
            self.rooms[room].remove(websocket)
            if not self.rooms[room]:
                del self.rooms[room]

    async def broadcast(self, room: str, message: str, exclude: WebSocket = None):
        if room in self.rooms:
            for conn in self.rooms[room]:
                if conn != exclude:
                    await conn.send_text(message)

room_manager = RoomManager()

@app.websocket("/ws/{room}")
async def room_endpoint(websocket: WebSocket, room: str):
    await room_manager.join(room, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await room_manager.broadcast(room, f"[{room}] {data}", exclude=websocket)
    except WebSocketDisconnect:
        room_manager.leave(room, websocket)
`

---

## 第三部分：实时应用模式

### 3.1 在线状态
`python
class PresenceManager:
    def __init__(self):
        self.online: dict[str, WebSocket] = {}

    async def user_online(self, user_id: str, ws: WebSocket):
        self.online[user_id] = ws
        await self.broadcast_presence()

    async def user_offline(self, user_id: str):
        self.online.pop(user_id, None)
        await self.broadcast_presence()

    async def broadcast_presence(self):
        users = list(self.online.keys())
        for ws in self.online.values():
            await ws.send_json({"type": "presence", "users": users})
`

### 3.2 实时通知
`python
@app.websocket("/ws/notifications/{user_id}")
async def notifications(websocket: WebSocket, user_id: str):
    await websocket.accept()
    # 订阅用户的通知队列
    pubsub = redis.pubsub()
    await pubsub.subscribe(f"notifications:{user_id}")
    try:
        while True:
            message = await pubsub.get_message()
            if message and message["type"] == "message":
                await websocket.send_text(message["data"].decode())
    except WebSocketDisconnect:
        await pubsub.unsubscribe()
`

---

## 本课总结

| 概念 | 说明 |
|------|------|
| WebSocket | 全双工持久连接 |
| ConnectionManager | 管理连接生命周期 |
| 房间 | 消息分组广播 |
| Redis Pub/Sub | 跨进程消息分发 |
