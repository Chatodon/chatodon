from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginView, MeView, UpdateUserSettingsView, UserAvatarView

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("me/", MeView.as_view(), name="me"),
    path("me/", MeView.as_view(), name="me_update"),
    path("settings/", UpdateUserSettingsView.as_view(), name="me_update"),
    path("avatar/<uuid:user_id>/", UserAvatarView.as_view(), name="user-avatar"),
]
