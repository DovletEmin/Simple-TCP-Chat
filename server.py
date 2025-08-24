from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI(title="Chat Microservice")

class ConnectionManager:
    def __init__(self):
        self.active: set[WebSocket] = set()

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.add(ws)
        print(f"Client connected. Online: {len(self.active)}")

    def disconnect(self, ws: WebSocket):
        if ws in self.active:
            self.active.remove(ws)
        print(f"Client disconnected. Online: {len(self.active)}")

    async def broadcast(self, message: str, sender: WebSocket):
        for ws in list(self.active):
            if ws is not sender:  # исключаем отправителя
                try:
                    await ws.send_text(message)
                except Exception:
                    self.disconnect(ws)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            data = await ws.receive_text()
            await manager.broadcast(data, ws)
    except WebSocketDisconnect:
        manager.disconnect(ws)
