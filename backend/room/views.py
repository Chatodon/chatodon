from rest_framework import generics, permissions

from .models import Room, RoomMember
from .pagination import RoomPagination
from .serializers import RoomCreateUpdateSerializer, RoomListSerializer, RoomSerializer


class RoomDetailView(generics.RetrieveAPIView):
    queryset = Room.objects.filter(is_active=True)
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"


# User's rooms list
class MyRoomListView(generics.ListAPIView):
    serializer_class = RoomListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = RoomPagination

    def get_queryset(self):
        return Room.objects.filter(participants=self.request.user, is_active=True).order_by(
            "-updated_at"
        )


class PublicRoomListView(generics.ListAPIView):
    serializer_class = RoomListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = RoomPagination

    def get_queryset(self):
        return Room.objects.filter(
            is_private=False, room_type__in=["group", "channel"], is_active=True
        ).order_by("-updated_at")


# Create room
class RoomCreateView(generics.CreateAPIView):
    serializer_class = RoomCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        room = serializer.save(owner=self.request.user)
        RoomMember.objects.create(room=room, user=self.request.user, role="owner")
        room.save()


# Update room
class RoomUpdateView(generics.UpdateAPIView):
    serializer_class = RoomCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return Room.objects.filter(owner=self.request.user)
