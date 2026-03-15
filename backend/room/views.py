from rest_framework import generics, permissions, status
from rest_framework.response import Response

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
            is_public=True, room_type__in=["group", "channel"], is_active=True
        ).order_by("-updated_at")


# Create room
class RoomCreateView(generics.CreateAPIView):
    serializer_class = RoomCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        room = serializer.save(owner=request.user)
        RoomMember.objects.create(room=room, user=request.user, role="owner")
        room.save()
        return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)


# Update room
class RoomUpdateView(generics.UpdateAPIView):
    serializer_class = RoomCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return Room.objects.filter(owner=self.request.user)
