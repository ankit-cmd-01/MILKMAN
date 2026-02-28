"""Payment domain models."""

from django.conf import settings
from django.db import models
from django.utils import timezone


class Payment(models.Model):
    """Payment record linked to user and subscription."""

    class PaymentMethodChoices(models.TextChoices):
        CARD = "CARD", "Card"
        UPI = "UPI", "UPI"
        NET_BANKING = "NET_BANKING", "Net Banking"
        CASH = "CASH", "Cash"

    class StatusChoices(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
    )
    subscription = models.ForeignKey(
        "subscriptions.Subscription",
        on_delete=models.PROTECT,
        related_name="payments",
        null=True,
        blank=True,
    )
    one_time_order = models.ForeignKey(
        "cart.OneTimeOrder",
        on_delete=models.PROTECT,
        related_name="payments",
        null=True,
        blank=True,
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PaymentMethodChoices.choices)
    transaction_id = models.CharField(max_length=100, unique=True, db_index=True)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        db_index=True,
    )
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["subscription", "status"]),
            models.Index(fields=["paid_at"]),
        ]

    def save(self, *args, **kwargs):
        if self.subscription is None and self.one_time_order is None:
            raise ValueError("Payment must be linked to a subscription or one-time order.")
        if self.status == self.StatusChoices.SUCCESS and self.paid_at is None:
            self.paid_at = timezone.now()
        if self.one_time_order and self.amount != self.one_time_order.total_amount:
            self.amount = self.one_time_order.total_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_id} ({self.status})"
