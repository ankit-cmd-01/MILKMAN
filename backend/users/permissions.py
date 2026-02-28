"""Shared permission classes."""

from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):
    """Allow access to admin role users only."""

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (user.is_superuser or user.role == user.Roles.ADMIN)
        )


class IsCustomerRole(BasePermission):
    """Allow access to customer role users only."""

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.role == user.Roles.CUSTOMER
            and not user.is_superuser
        )


class IsOwnerOrAdmin(BasePermission):
    """Object-level access for owners or admin users."""

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser or user.role == user.Roles.ADMIN:
            return True
        owner = getattr(obj, "user", None)
        return owner == user
