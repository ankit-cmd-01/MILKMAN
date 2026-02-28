"""Signals for subscription state and product demand tracking."""

from django.db.models import F
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Subscription, SubscriptionHistory


@receiver(pre_save, sender=Subscription)
def cache_previous_status(sender, instance, **kwargs):
    """Store old status for history generation on updates."""
    if not instance.pk:
        instance._old_status = None
        return
    previous = sender.objects.filter(pk=instance.pk).values("status").first()
    instance._old_status = previous["status"] if previous else None


@receiver(post_save, sender=Subscription)
def track_subscription_events(sender, instance, created, **kwargs):
    """Create history records and update product demand on creation."""
    old_status = None if created else getattr(instance, "_old_status", None)

    if created:
        instance.product.__class__.objects.filter(pk=instance.product_id).update(
            demand_count=F("demand_count") + instance.quantity
        )

    if created or old_status != instance.status:
        SubscriptionHistory.objects.create(
            subscription=instance,
            old_status=old_status,
            new_status=instance.status,
        )

