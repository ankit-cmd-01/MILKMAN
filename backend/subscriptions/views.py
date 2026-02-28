"""Views for subscription management."""

from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from users.permissions import IsAdminRole

from .models import Subscription
from .permissions import IsSubscriptionOwnerOrAdmin
from .serializers import (
    BulkSubscriptionSerializer,
    SubscriptionHistorySerializer,
    SubscriptionSerializer,
)


class SubscriptionViewSet(viewsets.ModelViewSet):
    """Manage subscriptions for customers and admins."""

    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Subscription.objects.select_related("user", "product").all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["status", "product", "frequency", "start_date", "end_date"]
    ordering_fields = ["created_at", "start_date", "end_date", "total_price", "frequency"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if user.is_superuser or user.role == user.Roles.ADMIN:
            return queryset
        return queryset.filter(user=user)

    def perform_create(self, serializer):
        if self.request.user.is_superuser or self.request.user.role == self.request.user.Roles.ADMIN:
            raise PermissionDenied("Admin users cannot create customer subscriptions directly.")
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action == "admin_overview":
            return [IsAdminRole()]
        if self.action in {"pause", "resume", "cancel"}:
            return [IsAuthenticated(), IsSubscriptionOwnerOrAdmin()]
        if self.action in {"retrieve", "update", "partial_update", "destroy", "history"}:
            return [IsAuthenticated(), IsSubscriptionOwnerOrAdmin()]
        return [IsAuthenticated()]

    @action(detail=True, methods=["get"])
    def history(self, request, pk=None):
        """Return status transition history for a subscription."""
        subscription = self.get_object()
        serializer = SubscriptionHistorySerializer(subscription.history.all(), many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[IsAdminRole])
    def admin_overview(self, request):
        """Admin summary for subscription counts."""
        queryset = Subscription.objects.all()
        data = {
            "total_subscriptions": queryset.count(),
            "active_subscriptions": queryset.filter(status=Subscription.StatusChoices.ACTIVE).count(),
            "paused_subscriptions": queryset.filter(status=Subscription.StatusChoices.PAUSED).count(),
            "cancelled_subscriptions": queryset.filter(status=Subscription.StatusChoices.CANCELLED).count(),
        }
        return Response(data)

    @action(detail=True, methods=["patch"])
    def pause(self, request, pk=None):
        subscription = self.get_object()
        subscription.status = Subscription.StatusChoices.PAUSED
        subscription.save(update_fields=["status", "total_price"])
        return Response(SubscriptionSerializer(subscription).data)

    @action(detail=True, methods=["patch"])
    def resume(self, request, pk=None):
        subscription = self.get_object()
        subscription.status = Subscription.StatusChoices.ACTIVE
        subscription.save(update_fields=["status", "total_price"])
        return Response(SubscriptionSerializer(subscription).data)

    @action(detail=True, methods=["patch"])
    def cancel(self, request, pk=None):
        subscription = self.get_object()
        subscription.status = Subscription.StatusChoices.CANCELLED
        subscription.save(update_fields=["status", "total_price"])
        return Response(SubscriptionSerializer(subscription).data)

    @action(detail=False, methods=["post"])
    def bulk_subscribe(self, request):
        """Create multiple subscriptions in a single request."""
        if request.user.is_superuser or request.user.role == request.user.Roles.ADMIN:
            raise PermissionDenied("Admin users cannot create customer subscriptions directly.")

        input_serializer = BulkSubscriptionSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        created = []
        with transaction.atomic():
            for item in input_serializer.validated_data["items"]:
                serializer = SubscriptionSerializer(
                    data={
                        "product": item["product"].id,
                        "quantity": item["quantity"],
                        "frequency": item["frequency"],
                        "start_date": item["start_date"],
                        "end_date": item.get("end_date"),
                    }
                )
                serializer.is_valid(raise_exception=True)
                subscription = serializer.save(user=request.user)
                created.append(subscription)

        return Response(
            SubscriptionSerializer(created, many=True).data,
            status=status.HTTP_201_CREATED,
        )
