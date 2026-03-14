import asyncio
from contextlib import asynccontextmanager

from fastapi import Cookie, FastAPI, WebSocket, WebSocketDisconnect

import api
import redis_listener
from config import HOST, PORT
from connection_manager import manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(redis_listener.redis_listener())
    yield
    task.cancel()
    await asyncio.gather(task, return_exceptions=True)


app = FastAPI(title="Chatodon", lifespan=lifespan)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, sessionid: str | None = Cookie(default=None)):
    if not sessionid:
        await websocket.close(code=1008)
        return

    user = await api.get_user_from_session(sessionid)
    if not user or not user.get("user"):
        await websocket.close(code=1008)
        return

    await websocket.accept()

    room_ids = await api.get_user_rooms(sessionid)
    for room_id in room_ids:
        manager.add_to_room(room_id, websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
