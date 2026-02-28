"""Cart app permissions."""

from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    """Allow access to customer users."""

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.role == user.Roles.CUSTOMER
            and not user.is_superuser
        )

