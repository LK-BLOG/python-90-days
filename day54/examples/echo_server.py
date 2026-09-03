\"\"\"WebSocket Echo服务器\"\"\"

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


@app.websocket(\"/ws/echo\")
async def echo_websocket(websocket: WebSocket):
    await websocket.accept()
    print(\"Client connected\")
    try:
        while True:
            data = await websocket.receive_text()
            print(f\"Received: {data}\")
            await websocket.send_text(f\"Echo: {data}\")
    except WebSocketDisconnect:
        print(\"Client disconnected\")


@app.websocket(\"/ws/info\")
async def info_websocket(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({
        \"type\": \"connected\",
        \"message\": \"Welcome to the WebSocket server!\"
    })
    await websocket.close()
