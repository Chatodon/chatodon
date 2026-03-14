from django.urls import path

from .views import (
    MyRoomListView,
    PublicRoomListView,
    RoomCreateView,
    RoomDetailView,
    RoomUpdateView,
)

urlpatterns = [
    path("<uuid:id>/", RoomDetailView.as_view(), name="room-detail"),
    path("my/", MyRoomListView.as_view(), name="user-rooms"),
    path("public/", PublicRoomListView.as_view(), name="public-rooms"),
    path("create/", RoomCreateView.as_view(), name="room-create"),
    path("<uuid:id>/update/", RoomUpdateView.as_view(), name="room-update"),
]
