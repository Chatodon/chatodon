import asyncio
import json

import redis.asyncio as redis

from config import REDIS_URL
from connection_manager import manager


async def redis_listener():
    redis_client = redis.from_url(REDIS_URL)
    pubsub = redis_client.pubsub()
    await pubsub.psubscribe("room:*")

    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message is None:
                await asyncio.sleep(0.01)
                continue

            if message["type"] != "pmessage":
                continue

            data = json.loads(message["data"])
            room_id = data["room_id"]
            await manager.broadcast(room_id, data)
    except asyncio.CancelledError:
        pass
    finally:
        await pubsub.unsubscribe()
        await pubsub.aclose()
        await redis_client.aclose()
