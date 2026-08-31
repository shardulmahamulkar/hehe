from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.rooms: dict[int, list[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, room_id: int):
        await websocket.accept()
        if room_id not in self.rooms:
            self.rooms[room_id] = []
        self.rooms[room_id].append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: int):
        if websocket in self.rooms.get(room_id, []):
            self.rooms[room_id].remove(websocket)

    async def broadcast(self, message: str, room_id: int):
        for connection in self.rooms.get(room_id, []):
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/{room_id}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, client_id: str):
    await manager.connect(websocket, room_id)

    try:
        while True:
            data = await websocket.receive_text()

            await manager.broadcast(
                f"Client #{client_id}: {data}",
                room_id,
            )

    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)

        await manager.broadcast(
            f"Client #{client_id} left the chat",
            room_id,
        )
