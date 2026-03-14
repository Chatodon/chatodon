from django.db import transaction
from rest_framework import serializers

from account.serializers import UserBriefSerializer

from .models import Message, MessageAttachment


class MessageAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageAttachment
        fields = (
            "id",
            "file",
            "file_type",
            "file_size",
            "created_at",
        )
        read_only_fields = ("id", "created_at")


# serializers.py
class MessageCreateSerializer(serializers.ModelSerializer):
    attachments = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )

    class Meta:
        model = Message
        fields = (
            "id",
            "room",
            "content",
            "reply_to",
            "attachments",
            "created_at",
        )
        read_only_fields = ("id", "created_at")

    def validate(self, attrs):
        reply_to = attrs.get("reply_to")
        room = attrs.get("room")
        message_type = attrs.get("message_type", "user")
        content = attrs.get("content")

        if message_type == "system":
            raise serializers.ValidationError("System messages can only be generated automatically")

        if reply_to and reply_to.room_id != room.id:
            raise serializers.ValidationError("Reply message must belong to the same room.")

        if message_type == "user" and not content:
            raise serializers.ValidationError("Content cannot be empty.")

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        attachments = validated_data.pop("attachments", [])
        user = self.context["request"].user

        message = Message.objects.create(sender=user, **validated_data)

        for file in attachments:
            MessageAttachment.objects.create(
                message=message,
                file=file,
                file_type=getattr(file, "content_type", ""),
                file_size=file.size,
            )

        return message


class MessageUpdateSerializer(serializers.ModelSerializer):
    attachments = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )

    class Meta:
        model = Message
        fields = (
            "content",
            "attachments",
        )

    @transaction.atomic
    def update(self, instance, validated_data):
        attachments = validated_data.pop("attachments", None)

        instance.content = validated_data.get("content", instance.content)
        instance.is_edited = True
        instance.save()

        if attachments is not None:
            instance.attachments.all().delete()

            for file in attachments:
                MessageAttachment.objects.create(
                    message=instance,
                    file=file,
                    file_type=file.content_type if hasattr(file, "content_type") else "",
                    file_size=file.size,
                )

        return instance


class ReplyMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("id", "content", "is_deleted")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.is_deleted:
            data["content"] = ""
        return data


class MessageSerializer(serializers.ModelSerializer):
    attachments = MessageAttachmentSerializer(many=True, read_only=True)
    sender = UserBriefSerializer()
    reply_to = ReplyMessageSerializer()

    class Meta:
        model = Message
        fields = (
            "id",
            "room",
            "sender",
            "message_type",
            "content",
            "payload",
            "is_edited",
            "is_deleted",
            "reply_to",
            "attachments",
            "created_at",
            "updated_at",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if instance.message_type == Message.MessageType.USER:
            data.pop("payload", None)
        elif instance.message_type == Message.MessageType.SYSTEM:
            data.pop("content", None)
        if instance.is_deleted:
            data["content"] = ""

        return data

    def validate(self, attrs):
        message_type = attrs.get("message_type", Message.MessageType.USER)
        content = attrs.get("content")
        payload = attrs.get("payload")

        if message_type == Message.MessageType.USER:
            if not content:
                raise serializers.ValidationError("User message must contain content.")
            attrs["payload"] = None

        if message_type == Message.MessageType.SYSTEM:
            if not payload:
                raise serializers.ValidationError("System message must contain payload.")
            attrs["content"] = None

        return attrs
