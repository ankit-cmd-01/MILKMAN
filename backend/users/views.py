"""User app views."""

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import User
from .serializers import (
    CustomTokenObtainPairSerializer,
    RegisterSerializer,
    UserProfileSerializer,
)


class RegisterAPIView(generics.CreateAPIView):
    """Create a new customer account."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginAPIView(TokenObtainPairView):
    """Issue JWT token pair and role-aware redirect hint."""

    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


class RefreshTokenAPIView(TokenRefreshView):
    """Refresh JWT access token."""

    permission_classes = [AllowAny]


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    """Retrieve and update the authenticated user profile."""

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
