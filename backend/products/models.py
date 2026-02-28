"""Product domain models."""

from django.db import models


class Category(models.Model):
    """Product category."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("name",)
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return self.name


class Product(models.Model):
    """Sellable product."""

    class UnitChoices(models.TextChoices):
        LITRE = "litre", "Litre"
        KG = "kg", "Kg"
        PACK = "pack", "Pack"

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    unit = models.CharField(max_length=10, choices=UnitChoices.choices, default=UnitChoices.PACK)
    is_available = models.BooleanField(default=True)
    demand_count = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["category", "is_available"]),
            models.Index(fields=["demand_count"]),
        ]

    def __str__(self):
        return self.name

    @property
    def is_low_stock(self):
        """Flag low stock for UI warnings."""
        return self.stock_quantity <= 10
