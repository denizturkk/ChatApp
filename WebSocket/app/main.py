from fastapi import FastAPI, WebSocket
from app.websocket_app.websocket_route import websocket_endpoint

app = FastAPI()

@app.websocket("/ws/{user_id}")
async def websocket_endpoint_wrapper(websocket: WebSocket, user_id: int):
    await websocket_endpoint(websocket, user_id)
