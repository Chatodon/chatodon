from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html

from .models import Room, RoomBan, RoomMember
from .services.participants import recount_room_participants


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "username",
        "owner",
        "participants_count",
        "is_public",
        "room_type",
        "is_active",
        "created_at",
    )
    list_filter = ("is_public", "room_type", "is_active", "created_at")
    search_fields = ("name", "username", "owner__username")
    readonly_fields = (
        "participants_count",
        "created_at",
        "updated_at",
        "recount_button",
    )
    prepopulated_fields = {"username": ("name",)}
    ordering = ("-created_at",)

    # Recount button
    def recount_button(self, obj):
        if not obj.pk:
            return "-"

        url = reverse(
            "admin:room_room_recount",
            args=[obj.pk],
        )

        return format_html(
            '<a class="button" href="{}">Recount participants</a>',
            url,
        )

    recount_button.short_description = "Force recount"

    # Recount URL
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<uuid:room_id>/recount/",
                self.admin_site.admin_view(self.recount_view),
                name="room_room_recount",
            ),
        ]
        return custom_urls + urls

    # Recount view
    def recount_view(self, request, room_id):
        room = self.get_object(request, room_id)

        if room is None:
            self.message_user(
                request,
                "Room not found.",
                level=messages.ERROR,
            )
            return HttpResponseRedirect("../")

        new_value = recount_room_participants(room)

        self.message_user(
            request,
            f"participants_count updated: {new_value}",
            level=messages.SUCCESS,
        )

        return HttpResponseRedirect(reverse("admin:room_room_change", args=[room.pk]))


@admin.register(RoomMember)
class RoomMemberAdmin(admin.ModelAdmin):
    list_display = ("user", "room", "role", "is_muted", "is_banned", "joined_at")
    list_filter = ("role", "is_muted", "is_banned", "joined_at")
    search_fields = ("user__username", "room__name")
    readonly_fields = ("joined_at",)
    ordering = ("-joined_at",)


@admin.register(RoomBan)
class RoomBanAdmin(admin.ModelAdmin):
    list_display = ("user", "room", "banned_by", "created_at", "expires_at", "reason")
    list_filter = ("created_at", "expires_at")
    search_fields = (
        "user__username",
        "room__name",
        "banned_by__username",
        "reason",
    )
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
