from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistrationSerializer


class RegistrationView(APIView):
    """Creates a new user and returns an auth token."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return self._build_auth_response(user, status.HTTP_201_CREATED)

    def _build_auth_response(self, user, response_status):
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            self._get_auth_data(user, token),
            status=response_status,
        )

    def _get_auth_data(self, user, token):
        return {
            "token": token.key,
            "username": user.username,
            "email": user.email,
            "user_id": user.id,
        }


class LoginView(APIView):
    """Authenticates a user and returns an auth token."""

    permission_classes = [AllowAny]

    def post(self, request):
        user = self._authenticate_user(request)
        if not user:
            return self._get_invalid_credentials_response()
        return self._build_auth_response(user)

    def _authenticate_user(self, request):
        return authenticate(
            username=request.data.get("username"),
            password=request.data.get("password"),
        )

    def _get_invalid_credentials_response(self):
        return Response(
            {"detail": "Invalid credentials."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def _build_auth_response(self, user):
        token, _ = Token.objects.get_or_create(user=user)
        return Response(self._get_auth_data(user, token))

    def _get_auth_data(self, user, token):
        return {
            "token": token.key,
            "username": user.username,
            "email": user.email,
            "user_id": user.id,
        }