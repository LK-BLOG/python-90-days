# Day 34 WebSocket 骨架 - TODO: 实现
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        # TODO: 初始化连接列表
        pass

    async def connect(self, websocket: WebSocket):
        # TODO: 接受连接并添加到列表
        pass

    def disconnect(self, websocket: WebSocket):
        # TODO: 移除连接
        pass

    async def broadcast(self, message: str):
        # TODO: 广播消息到所有连接
        pass

# TODO: 创建 manager 实例
# TODO: 实现 /ws/{client_id} 端点
