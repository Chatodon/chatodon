import uuid

from django.conf import settings
from django.db import models


# LEGACY. USES IN MIGRATION FILES ONLY
def message_attachment_upload_to(instance, filename): ...


class Message(models.Model):
    class MessageType(models.TextChoices):
        USER = "user", "User message"
        SYSTEM = "system", "System message"

    id = models.BigAutoField(primary_key=True)

    room = models.ForeignKey(
        "room.Room", on_delete=models.CASCADE, related_name="messages", db_index=True
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sent_messages",
        db_index=True,
    )

    content = models.TextField(null=True, blank=True)

    message_type = models.CharField(
        max_length=20, choices=MessageType.choices, default=MessageType.USER, db_index=True
    )
    payload = models.JSONField(null=True, blank=True)  # For system messages

    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    reply_to = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="replies"
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.content:
            return self.content[0:12]
        else:
            return f"{self.sender}: {self.message_type} at {self.created_at}"

    class Meta:
        indexes = [
            models.Index(fields=["room", "-created_at"]),
            models.Index(fields=["room", "id"]),
            models.Index(fields=["room", "message_type"]),
        ]


class MessageAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="attachments")

    file = models.FileField(upload_to="attachments/%Y/%m/%d/")

    file_type = models.CharField(max_length=50)
    file_size = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
