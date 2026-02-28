"""Serializers for subscriptions."""

from rest_framework import serializers

from products.models import Product

from .models import Subscription, SubscriptionHistory


class SubscriptionSerializer(serializers.ModelSerializer):
    """Subscription serializer with validation and read-only pricing."""

    user_email = serializers.CharField(source="user.email", read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)
    estimated_end_date = serializers.DateField(source="effective_end_date", read_only=True)

    class Meta:
        model = Subscription
        fields = (
            "id",
            "user",
            "user_email",
            "product",
            "product_name",
            "quantity",
            "frequency",
            "start_date",
            "end_date",
            "estimated_end_date",
            "status",
            "total_price",
            "created_at",
        )
        read_only_fields = ("id", "user", "total_price", "created_at")

    def validate(self, attrs):
        start_date = attrs.get("start_date", getattr(self.instance, "start_date", None))
        end_date = attrs.get("end_date", getattr(self.instance, "end_date", None))
        quantity = attrs.get("quantity", getattr(self.instance, "quantity", None))
        product = attrs.get("product", getattr(self.instance, "product", None))
        if quantity is not None and quantity < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError("End date cannot be before start date.")
        if product and (not product.is_available or product.stock_quantity < 1):
            raise serializers.ValidationError("Product unavailable for subscription.")
        return attrs


class BulkSubscriptionItemSerializer(serializers.Serializer):
    """Input serializer for bulk subscription creation."""

    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(min_value=1, default=1)
    frequency = serializers.ChoiceField(choices=Subscription.FrequencyChoices.choices)
    start_date = serializers.DateField()
    end_date = serializers.DateField(required=False, allow_null=True)


class BulkSubscriptionSerializer(serializers.Serializer):
    """Bulk subscription payload serializer."""

    items = BulkSubscriptionItemSerializer(many=True, min_length=1, max_length=5)


class SubscriptionHistorySerializer(serializers.ModelSerializer):
    """Subscription history serializer."""

    class Meta:
        model = SubscriptionHistory
        fields = ("id", "subscription", "changed_at", "old_status", "new_status")
        read_only_fields = fields
