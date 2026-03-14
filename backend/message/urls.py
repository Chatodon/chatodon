from django.urls import path

from .views import (
    AttachmentDownloadView,
    MessageCreateView,
    MessageDeleteView,
    MessageDetailView,
    MessageUpdateView,
    RoomMessageListView,
)

urlpatterns = [
    path("<uuid:room_id>/", RoomMessageListView.as_view(), name="room-messages"),
    path("", MessageCreateView.as_view(), name="message-create"),
    path("<uuid:pk>/", MessageDetailView.as_view(), name="message-detail"),
    path("<uuid:pk>/update/", MessageUpdateView.as_view(), name="message-update"),
    path("<int:pk>/delete/", MessageDeleteView.as_view(), name="message-delete"),
    path("attachments/<uuid:pk>/", AttachmentDownloadView.as_view(), name="attachment-download"),
]
