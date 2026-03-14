import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from validators.account import username_validator


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    username = models.CharField(max_length=32, unique=True, validators=[username_validator])
    name = models.CharField(max_length=32)
    email = models.EmailField(blank=True)

    avatar = models.ImageField(upload_to="user_avatars/", null=True, blank=True)
    bio = models.TextField(blank=True)

    verified = models.BooleanField(default=True)
    official = models.BooleanField(default=True)
    banned = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class UserSetting(models.Model):
    class PrivacyLevel(models.TextChoices):
        EVERYONE = "everyone", "Everyone"
        FRIENDS = "friends", "Friends only"
        NOBODY = "nobody", "Nobody"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="settings",
    )

    # Privacy

    is_profile_public = models.BooleanField(default=True)

    allow_direct_messages = models.BooleanField(default=True)

    who_can_invite_to_room = models.CharField(
        max_length=20,
        choices=PrivacyLevel.choices,
        default=PrivacyLevel.EVERYONE,
    )

    last_seen_visibility = models.CharField(
        max_length=20,
        choices=PrivacyLevel.choices,
        default=PrivacyLevel.EVERYONE,
    )

    show_online_status = models.BooleanField(default=True)

    # Notifications

    notify_on_direct_message = models.BooleanField(default=True)
    notify_on_room_message = models.BooleanField(default=True)
    notify_on_mentions = models.BooleanField(default=True)
    notify_on_room_invite = models.BooleanField(default=True)

    # UI / Client

    language = models.CharField(
        max_length=8,
        default="en",
    )

    # Technical

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Settings for {self.user.username}"


class UserBan(models.Model):
    class BanType(models.TextChoices):
        TEMPORARY = "temporary", "Temporary"
        PERMANENT = "permanent", "Permanent"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bans",
    )

    banned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="issued_bans",
    )

    ban_type = models.CharField(
        max_length=16,
        choices=BanType.choices,
    )

    reason = models.TextField(blank=True)

    starts_at = models.DateTimeField(default=timezone.now)
    ends_at = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Ban for {self.user.username} ({self.ban_type})"

    def is_expired(self):
        if self.ban_type == self.BanType.PERMANENT:
            return False
        if self.ends_at:
            return timezone.now() > self.ends_at
        return False
