"""Admin config for payments app."""

from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "subscription",
        "one_time_order",
        "amount",
        "payment_method",
        "transaction_id",
        "status",
        "paid_at",
        "created_at",
    )
    list_filter = ("status", "payment_method", "created_at")
    search_fields = ("transaction_id", "user__email", "subscription__product__name")
    ordering = ("-created_at",)
