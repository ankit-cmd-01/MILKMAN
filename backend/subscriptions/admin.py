"""Admin config for subscriptions app."""

from django.contrib import admin

from .models import Subscription, SubscriptionHistory


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "product",
        "quantity",
        "status",
        "start_date",
        "end_date",
        "total_price",
        "created_at",
    )
    list_filter = ("status", "start_date", "end_date")
    search_fields = ("user__email", "product__name")
    ordering = ("-created_at",)


@admin.register(SubscriptionHistory)
class SubscriptionHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "subscription", "old_status", "new_status", "changed_at")
    list_filter = ("old_status", "new_status")
    search_fields = ("subscription__user__email", "subscription__product__name")
    ordering = ("-changed_at",)

