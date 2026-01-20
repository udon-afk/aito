from fastapi import FastAPI, WebSocket
import asyncio
import logging
from ..config import WS_HOST, WS_PORT

logger = logging.getLogger(__name__)

app = FastAPI()
active_connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            # Keep alive / listen for client messages
            data = await websocket.receive_text()
            # Echo or process commands from frontend
            await websocket.send_text(f"Message received: {data}")
    except Exception:
        active_connections.remove(websocket)

class WebSocketServer:
    def __init__(self):
        pass
    
    async def broadcast(self, message: dict):
        """
        Broadcast a JSON message to all connected clients.
        """
        if not active_connections:
            return
            
        for connection in active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass

def run_server():
    import uvicorn
    uvicorn.run(app, host=WS_HOST, port=WS_PORT, log_level="warning")
