from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import FileResponse, Http404, HttpResponse
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import (
    UserSerializer,
    UserSettingSerializer,
    UserSettingUpdateSerializer,
    UserUpdateSerializer,
)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        serialized_user = UserSerializer(user)
        if user is not None:
            login(request, user)
            return Response(serialized_user.data)
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"detail": "Logged out"})


class MeView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        user_serializer = UserSerializer(request.user, context={"request": request})
        user_settings_serializer = UserSettingSerializer(request.user.settings)

        return Response(
            {
                "user": user_serializer.data,
                "settings": user_settings_serializer.data,
            }
        )

    def patch(self, request):
        serializer = UserUpdateSerializer(
            request.user, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"user": UserSerializer(request.user, context={"request": request}).data})


class UpdateUserSettingsView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = UserSettingUpdateSerializer(
            request.user.settings, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"settings": UserSettingSerializer(request.user.settings).data})


class UserAvatarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404("User not found") from None

        if not user.avatar:
            raise Http404("Avatar not found")

        if settings.DEBUG:
            # In DEBUG mode just return the image file
            return FileResponse(user.avatar, content_type="image/jpeg")
        else:
            # In Production return header X-Accel-Redirect for Nginx
            response = HttpResponse()
            response["Content-Type"] = "image/jpeg"
            response["X-Accel-Redirect"] = f"/protected_media/{user.avatar.name}"
            return response
