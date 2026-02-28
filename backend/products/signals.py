"""Signals for product availability synchronization."""

from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Product


@receiver(pre_save, sender=Product)
def sync_product_availability(sender, instance, **kwargs):
    """Auto-disable product availability when stock is depleted."""
    if instance.stock_quantity <= 0:
        instance.is_available = False
