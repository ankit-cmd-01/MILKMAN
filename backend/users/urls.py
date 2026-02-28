"""User app URL routes."""

from django.urls import path

from .views import LoginAPIView, ProfileAPIView, RefreshTokenAPIView, RegisterAPIView


urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("token/refresh/", RefreshTokenAPIView.as_view(), name="token-refresh"),
    path("profile/", ProfileAPIView.as_view(), name="profile"),
]
