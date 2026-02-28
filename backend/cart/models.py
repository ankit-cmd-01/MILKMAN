"""Cart domain models."""

from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import F, Sum


class Cart(models.Model):
    """Per-user cart."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["user"])]

    @property
    def total_value(self):
        total = self.items.aggregate(
            total=Sum(F("quantity") * F("product__price"), output_field=models.DecimalField(max_digits=12, decimal_places=2))
        )["total"]
        return total if total is not None else Decimal("0.00")

    def __str__(self):
        return f"Cart({self.user.email})"


class CartItem(models.Model):
    """Individual cart item."""

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("cart", "product")
        indexes = [models.Index(fields=["cart", "product"])]

    @property
    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class OneTimeOrder(models.Model):
    """Single order checkout from cart (non-subscription)."""

    class StatusChoices(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        CANCELLED = "CANCELLED", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="one_time_orders",
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [models.Index(fields=["user", "status"])]

    def recalculate_total(self):
        total = self.items.aggregate(
            total=Sum(
                F("quantity") * F("unit_price"),
                output_field=models.DecimalField(max_digits=12, decimal_places=2),
            )
        )["total"]
        self.total_amount = total if total is not None else Decimal("0.00")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.pk:
            self.recalculate_total()
            super().save(update_fields=["total_amount", "updated_at"])

    def __str__(self):
        return f"OneTimeOrder({self.id}, {self.user.email})"


class OneTimeOrderItem(models.Model):
    """Order line for one-time purchases."""

    order = models.ForeignKey(
        OneTimeOrder,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="one_time_order_items",
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["order", "product"])]

    @property
    def subtotal(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
