from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User, UserBan, UserSetting


def get_avatar(user: User) -> str | None:
    if user.avatar:
        return f"/api/account/avatar/{user.id}/"
    return None


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data["username"],
            password=data["password"],
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        if user.banned:
            raise serializers.ValidationError("User is banned")

        data["user"] = user
        return data


class UserSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSetting
        fields = [
            "is_profile_public",
            "allow_direct_messages",
            "who_can_invite_to_room",
            "last_seen_visibility",
            "show_online_status",
            "notify_on_direct_message",
            "notify_on_room_message",
            "notify_on_mentions",
            "notify_on_room_invite",
            "language",
            "updated_at",
        ]


class ActiveBanSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBan
        fields = [
            "ban_type",
            "reason",
            "starts_at",
            "ends_at",
            "is_active",
        ]


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "name",
            "email",
            "avatar",
            "bio",
            "verified",
            "banned",
            "created_at",
            "updated_at",
        ]

    def get_avatar(self, obj):
        return get_avatar(obj)


class UserBriefSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "name",
            "avatar",
        ]

    def get_avatar(self, obj):
        return get_avatar(obj)


class UserUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            "name",
            "username",
            "email",
            "bio",
            "avatar",
        )

    def update(self, instance, validated_data):
        avatar = validated_data.get("avatar")

        # If a new avatar is uploaded, delete the old file
        if avatar and instance.avatar:
            instance.avatar.delete(save=False)

        return super().update(instance, validated_data)


class UserSettingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSetting
        exclude = (
            "id",
            "user",
            "updated_at",
        )
