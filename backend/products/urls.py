"""URL routes for products app."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ProductViewSet


router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("items", ProductViewSet, basename="product")

urlpatterns = [
    path("", include(router.urls)),
]

