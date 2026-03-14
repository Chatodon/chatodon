from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, UserBan, UserSetting


class UserSettingsInline(admin.StackedInline):
    model = UserSetting
    can_delete = False
    extra = 0
    verbose_name = "Settings"
    verbose_name_plural = "Settings"


class UserBanInline(admin.TabularInline):
    model = UserBan
    fk_name = "user"
    extra = 0
    fields = (
        "ban_type",
        "is_active",
        "starts_at",
        "ends_at",
        "banned_by",
        "reason",
        "created_at",
    )
    readonly_fields = ("created_at",)
    show_change_link = True


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [UserSettingsInline, UserBanInline]

    list_display = (
        "username",
        "name",
        "email",
        "verified",
        "banned",
        "is_staff",
        "created_at",
    )

    list_filter = (
        "verified",
        "banned",
        "is_staff",
        "is_superuser",
        "is_active",
        "created_at",
    )

    search_fields = (
        "username",
        "name",
        "email",
    )

    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at", "updated_at")

    fieldsets = (
        ("Core", {"fields": ("id", "username", "password")}),
        ("Profile", {"fields": ("name", "email", "avatar", "bio")}),
        (
            "Status",
            {
                "fields": (
                    "verified",
                    "banned",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Dates", {"fields": ("last_login", "date_joined", "created_at", "updated_at")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "name",
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


@admin.register(UserSetting)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "is_profile_public",
        "allow_direct_messages",
        "language",
        "updated_at",
    )

    list_filter = (
        "is_profile_public",
        "allow_direct_messages",
        "language",
    )

    search_fields = (
        "user__username",
        "user__name",
    )

    readonly_fields = ("updated_at",)
    ordering = ("user__username",)


@admin.register(UserBan)
class UserBanAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "ban_type",
        "is_active",
        "starts_at",
        "ends_at",
        "banned_by",
        "created_at",
    )

    list_filter = (
        "ban_type",
        "is_active",
        "starts_at",
        "created_at",
    )

    search_fields = (
        "user__username",
        "banned_by__username",
        "reason",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)

    autocomplete_fields = ("user", "banned_by")
