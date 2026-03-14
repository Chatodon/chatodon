from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Message, MessageAttachment
from .paginations import MessagePagination
from .serializers import (
    MessageCreateSerializer,
    MessageSerializer,
    MessageUpdateSerializer,
)
from .services import events as evs


class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        evs.publish_message_created(message)

        # serializing full message via MessageSerializer
        full_serializer = MessageSerializer(message, context={"request": request})
        return Response(full_serializer.data, status=status.HTTP_201_CREATED)


class MessageDetailView(generics.RetrieveAPIView):
    queryset = Message.objects.select_related("sender").prefetch_related("attachments")
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]


class RoomMessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = MessagePagination

    def get_queryset(self):
        room_id = self.kwargs["room_id"]

        return (
            Message.objects.filter(room_id=room_id)
            .select_related("sender")
            .prefetch_related("attachments")
            .order_by("-created_at")
        )


class MessageDeleteView(generics.DestroyAPIView):
    queryset = Message.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        message = self.get_object()

        if message.sender != request.user:
            raise PermissionDenied("You cannot delete this message.")

        message.is_deleted = True
        message.content = None
        message.save(update_fields=["is_deleted", "content", "updated_at"])

        evs.publish_message_updated(message)

        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageUpdateView(generics.UpdateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        message = self.get_object()

        if message.sender != self.request.user:
            raise PermissionDenied("You cannot edit this message.")

        serializer.save()


class AttachmentDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        attachment = get_object_or_404(
            MessageAttachment.objects.select_related("message__room"), pk=pk
        )

        room = attachment.message.room

        if not room.participants.filter(id=request.user.id).exists():
            raise PermissionDenied("Access denied.")

        #  if DEV: return file
        if settings.DEBUG:
            return FileResponse(attachment.file.open("rb"), as_attachment=False)

        #  if PROD: return a link to the file that nginx should send
        response = HttpResponse()
        response["Content-Type"] = ""
        response["X-Accel-Redirect"] = f"{settings.PROTECTED_MEDIA_URL}{attachment.file.name}"
        return response
