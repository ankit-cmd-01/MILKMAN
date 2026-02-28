"""Views for payment APIs."""

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsAdminRole

from .models import Payment
from .permissions import IsPaymentOwnerOrAdmin
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """Create and manage payment records."""

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.select_related("user", "subscription", "subscription__product").all()
    filterset_fields = ["status", "payment_method", "subscription"]
    ordering_fields = ["created_at", "paid_at", "amount"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if user.is_superuser or user.role == user.Roles.ADMIN:
            return queryset
        return queryset.filter(user=user)

    def perform_create(self, serializer):
        subscription = serializer.validated_data.get("subscription")
        one_time_order = serializer.validated_data.get("one_time_order")
        user = self.request.user
        if not (user.is_superuser or user.role == user.Roles.ADMIN):
            if subscription and subscription.user_id != user.id:
                raise PermissionDenied("Customers can create payments only for their own subscriptions.")
            if one_time_order and one_time_order.user_id != user.id:
                raise PermissionDenied("Customers can create payments only for their own one time orders.")
        serializer.save(user=user)

    def get_permissions(self):
        if self.action in {"retrieve", "update", "partial_update", "destroy"}:
            return [IsAuthenticated(), IsPaymentOwnerOrAdmin()]
        return [IsAuthenticated()]

    @action(detail=True, methods=["patch"], permission_classes=[IsAdminRole])
    def update_status(self, request, pk=None):
        """Update payment status after external payment handling."""
        payment = self.get_object()
        status_value = request.data.get("status")
        valid_statuses = {
            Payment.StatusChoices.PENDING,
            Payment.StatusChoices.SUCCESS,
            Payment.StatusChoices.FAILED,
        }
        if status_value not in valid_statuses:
            return Response(
                {"detail": "Invalid status value."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment.status = status_value
        payment.save()
        if payment.one_time_order and status_value == Payment.StatusChoices.SUCCESS:
            payment.one_time_order.status = payment.one_time_order.StatusChoices.PAID
            payment.one_time_order.save(update_fields=["status", "updated_at"])
        return Response(PaymentSerializer(payment).data, status=status.HTTP_200_OK)
