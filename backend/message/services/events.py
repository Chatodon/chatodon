import json
from uuid import UUID

import redis
from django.conf import settings
from django.db import transaction

from message.models import Message
from message.serializers import MessageSerializer

redis_client = redis.Redis.from_url(settings.REDIS_URL)


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def publish_message_created(message: Message):
    serialized_message = MessageSerializer(message).data

    payload = {
        "type": "message.created",
        "room_id": message.room_id,
        "message": serialized_message,
    }

    def _publish():
        redis_client.publish(
            f"room:{message.room_id}",
            json.dumps(payload, cls=UUIDEncoder),
        )

    transaction.on_commit(_publish)


def publish_message_updated(message: Message):
    serialized_message = MessageSerializer(message).data

    payload = {
        "type": "message.updated",
        "room_id": message.room_id,
        "message": serialized_message,
    }

    def _publish():
        redis_client.publish(
            f"room:{message.room_id}",
            json.dumps(payload, cls=UUIDEncoder),
        )

    transaction.on_commit(_publish)
