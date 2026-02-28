"""Product app views."""

from decimal import Decimal, InvalidOperation

from django.db.models import F
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from users.permissions import IsAdminRole

from .models import Category, Product
from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """CRUD endpoints for categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]


class ProductViewSet(viewsets.ModelViewSet):
    """CRUD/list endpoints for products with filter/search support."""

    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "is_available", "unit"]
    search_fields = ["name"]
    ordering_fields = ["name", "price", "created_at", "demand_count"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.action in {"list", "retrieve"}:
            return [IsAuthenticatedOrReadOnly()]
        return [IsAdminRole()]

    @action(detail=True, methods=["patch"], permission_classes=[IsAdminRole])
    def increase_price(self, request, pk=None):
        """Increase product price by a fixed amount (admin only)."""

        product = get_object_or_404(Product, pk=pk)
        amount_raw = request.data.get("amount")
        if amount_raw is None:
            return Response(
                {"detail": "amount is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            amount = Decimal(str(amount_raw))
        except (InvalidOperation, TypeError):
            return Response(
                {"detail": "amount must be a valid decimal."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if amount <= 0:
            return Response(
                {"detail": "amount must be greater than zero."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Product.objects.filter(pk=product.pk).update(price=F("price") + amount)
        product.refresh_from_db()
        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
