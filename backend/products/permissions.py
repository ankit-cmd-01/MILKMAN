"""Product app permission helpers."""

from rest_framework.permissions import SAFE_METHODS, BasePermission

from users.permissions import IsAdminRole


class IsAdminOrReadOnly(BasePermission):
    """Allow read for all authenticated/anonymous and write for admins."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return IsAdminRole().has_permission(request, view)

