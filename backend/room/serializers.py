from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Room, RoomBan, RoomMember

User = get_user_model()


class UserBasicSerializer(serializers.ModelSerializer):
    """
    Basic user information for display in a room.
    """

    class Meta:
        model = User
        fields = ["id", "username", "name", "avatar"]


class RoomSerializer(serializers.ModelSerializer):
    """
    Full room information for retrieve.
    """

    owner = UserBasicSerializer(read_only=True)
    participants = UserBasicSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = [
            "id",
            "name",
            "username",
            "description",
            "avatar",
            "room_type",
            "is_active",
            "owner",
            "participants_count",
            "participants",
            "created_at",
            "updated_at",
        ]


class RoomListSerializer(serializers.ModelSerializer):
    """
    Room list with minimal information.
    """

    owner = UserBasicSerializer(read_only=True)

    class Meta:
        model = Room
        fields = [
            "id",
            "name",
            "username",
            "avatar",
            "participants_count",
            "owner",
            "created_at",
            "updated_at",
        ]


class RoomCreateUpdateSerializer(serializers.ModelSerializer):
    """
    For creating and updating rooms.
    Only fields that the user is allowed to change.
    """

    class Meta:
        model = Room
        fields = ["name", "description", "avatar", "room_type", "is_active"]

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Room name is required")
        return value

    def validate_description(self, value):
        if value and len(value) > 1024:
            raise serializers.ValidationError("The maximum description length is 1024")
        return value

    def validate(self, attrs):
        return attrs


class RoomMemberSerializer(serializers.ModelSerializer):
    """
    Serializer for room members.
    """

    user = UserBasicSerializer(read_only=True)

    class Meta:
        model = RoomMember
        fields = ["id", "user", "role", "is_muted", "is_banned", "joined_at"]


class RoomBanSerializer(serializers.ModelSerializer):
    """
    Serializer for banned users.
    """

    user = UserBasicSerializer(read_only=True)
    banned_by = UserBasicSerializer(read_only=True)

    class Meta:
        model = RoomBan
        fields = ["id", "user", "banned_by", "reason", "created_at", "expires_at"]
