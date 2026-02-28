"""Permissions for analytics endpoints."""

from users.permissions import IsAdminRole


class IsAnalyticsAdmin(IsAdminRole):
    """Alias permission to make analytics intent explicit."""

