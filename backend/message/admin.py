from django.contrib import admin

from .models import Message, MessageAttachment


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "sender", "created_at", "is_edited", "is_deleted")
    list_filter = ("room", "is_edited", "is_deleted", "created_at")
    search_fields = ("content", "sender__username", "room__name")
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("room", "sender", "reply_to")
    ordering = ("-created_at",)
    autocomplete_fields = ("reply_to",)


@admin.register(MessageAttachment)
class MessageAttachmentAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "file", "file_type", "file_size", "created_at")
    list_filter = ("file_type", "created_at")
    search_fields = ("message__content",)
    readonly_fields = ("created_at",)
    raw_id_fields = ("message",)
