"""Subscription domain models."""

from decimal import Decimal
from math import ceil
from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Subscription(models.Model):
    """Customer subscription for a product."""

    class StatusChoices(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        PAUSED = "PAUSED", "Paused"
        CANCELLED = "CANCELLED", "Cancelled"
        COMPLETED = "COMPLETED", "Completed"

    class FrequencyChoices(models.TextChoices):
        DAILY = "DAILY", "Daily"
        WEEKLY = "WEEKLY", "Weekly"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="subscriptions",
    )
    quantity = models.PositiveIntegerField(default=1)
    frequency = models.CharField(
        max_length=20,
        choices=FrequencyChoices.choices,
        default=FrequencyChoices.DAILY,
        db_index=True,
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
        db_index=True,
    )
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["product", "status"]),
            models.Index(fields=["start_date", "end_date"]),
            models.Index(fields=["frequency", "status"]),
        ]

    def clean(self):
        if self.quantity < 1:
            raise ValidationError("Quantity must be at least 1.")
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date.")
        if not self.product.is_available or self.product.stock_quantity < 1:
            raise ValidationError("This product is currently unavailable for subscription.")
        if self.user.role != self.user.Roles.CUSTOMER and not self.user.is_superuser:
            raise ValidationError("Only customers can create subscriptions.")

    @property
    def effective_end_date(self):
        """Estimated end date when end_date is not provided (30-day plan)."""
        return self.end_date or (self.start_date + timedelta(days=29))

    def calculate_total_price(self):
        """Calculate total price based on date range, quantity, and product price."""
        effective_end_date = self.effective_end_date
        duration_days = (effective_end_date - self.start_date).days + 1
        if self.frequency == self.FrequencyChoices.WEEKLY:
            delivery_count = ceil(duration_days / 7)
        else:
            delivery_count = duration_days
        self.total_price = self.product.price * self.quantity * delivery_count

    def save(self, *args, **kwargs):
        self.full_clean()
        self.calculate_total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} - {self.product.name} ({self.status})"


class SubscriptionHistory(models.Model):
    """Status transition log for subscriptions."""

    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name="history",
    )
    changed_at = models.DateTimeField(auto_now_add=True)
    old_status = models.CharField(
        max_length=20,
        choices=Subscription.StatusChoices.choices,
        null=True,
        blank=True,
    )
    new_status = models.CharField(
        max_length=20,
        choices=Subscription.StatusChoices.choices,
    )

    class Meta:
        ordering = ("-changed_at",)
        indexes = [models.Index(fields=["subscription", "changed_at"])]

    def __str__(self):
        return f"{self.subscription_id}: {self.old_status} -> {self.new_status}"
