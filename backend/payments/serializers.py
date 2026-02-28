"""Payment serializers."""

from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for payments."""

    user_email = serializers.CharField(source="user.email", read_only=True)
    subscription_details = serializers.SerializerMethodField()
    one_time_order_id = serializers.IntegerField(source="one_time_order.id", read_only=True)

    class Meta:
        model = Payment
        fields = (
            "id",
            "user",
            "user_email",
            "subscription",
            "subscription_details",
            "one_time_order",
            "one_time_order_id",
            "amount",
            "payment_method",
            "transaction_id",
            "status",
            "paid_at",
            "created_at",
        )
        read_only_fields = ("id", "user", "user_email", "subscription_details", "one_time_order_id", "paid_at", "created_at")

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate(self, attrs):
        subscription = attrs.get("subscription", getattr(self.instance, "subscription", None))
        one_time_order = attrs.get("one_time_order", getattr(self.instance, "one_time_order", None))
        if not subscription and not one_time_order:
            raise serializers.ValidationError("Payment must reference subscription or one time order.")
        return attrs

    def get_subscription_details(self, obj):
        if obj.subscription:
            return str(obj.subscription)
        return ""
