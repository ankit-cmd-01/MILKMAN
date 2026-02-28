"""Payment app permissions."""

from rest_framework.permissions import BasePermission


class IsPaymentOwnerOrAdmin(BasePermission):
    """Allow payment owner or admin users."""

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser or user.role == user.Roles.ADMIN:
            return True
        return obj.user_id == user.id

