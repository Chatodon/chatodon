from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, set[WebSocket]] = {}

    def add_to_room(self, room_id: int, websocket: WebSocket):
        self.active_connections.setdefault(room_id, set()).add(websocket)

    def disconnect(self, websocket: WebSocket):
        for room_id in list(self.active_connections.keys()):
            self.active_connections[room_id].discard(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def broadcast(self, room_id: int, message: dict):
        for connection in self.active_connections.get(room_id, []):
            await connection.send_json(message)


manager = ConnectionManager()
