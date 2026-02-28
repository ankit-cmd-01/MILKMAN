"""Serializers for authentication and profile operations."""

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """Register serializer for customer signups."""

    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "address",
            "password",
            "confirm_password",
        )
        read_only_fields = ("id",)

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer for read/update actions."""

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "address",
            "role",
            "is_active",
            "date_joined",
        )
        read_only_fields = ("id", "email", "role", "is_active", "date_joined")


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """JWT serializer including role and frontend redirect hint."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["role"] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        redirect_to = "/admin-dashboard" if user.is_superuser else "/customer-dashboard"
        data.update(
            {
                "user": UserProfileSerializer(user).data,
                "redirect_to": redirect_to,
            }
        )
        return data
