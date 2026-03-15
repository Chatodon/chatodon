import uuid

from django.conf import settings
from django.db import models

from validators.account import username_validator


class Room(models.Model):
    class RoomType(models.TextChoices):
        PRIVATE = "private", "Private room"  # one-to-one room
        GROUP = "group", "Group room"  # multi-user room
        CHANNEL = "channel", "Channel room"  # broadcast room

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255)
    username = models.CharField(
        max_length=32, unique=True, null=True, blank=True, validators=[username_validator]
    )
    description = models.TextField(blank=True)

    avatar = models.ImageField(upload_to="room_avatars/", blank=True, null=True)

    room_type = models.CharField(
        max_length=20, choices=RoomType.choices, default=RoomType.PRIVATE, db_index=True
    )
    is_public = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_rooms"
    )

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="RoomMember", related_name="rooms"
    )

    participants_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["username"]),
            models.Index(fields=["created_at"]),
        ]

    def save(self, *args, **kwargs):
        if self.is_public and not self.username:
            self.username = str(uuid.uuid4())[:32]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class RoomMember(models.Model):
    ROLE_CHOICES = (
        ("owner", "Owner"),
        ("admin", "Admin"),
        ("member", "Member"),
    )

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="members")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="room_memberships"
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")

    is_muted = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    invitation_accepted = models.BooleanField(default=False)

    last_read_message = models.ForeignKey(
        "message.Message", null=True, blank=True, on_delete=models.CASCADE
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("room", "user")
        indexes = [
            models.Index(fields=["room", "user"]),
        ]

    def __str__(self):
        return f"{self.user} in {self.room}"


class RoomBan(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bans")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    banned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="issued_bans_in_room",
    )

    reason = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("room", "user")
