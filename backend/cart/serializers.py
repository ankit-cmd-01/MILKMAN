"""Serializers for cart operations."""

from rest_framework import serializers

from .models import Cart, CartItem, OneTimeOrder, OneTimeOrderItem


class CartItemSerializer(serializers.ModelSerializer):
    """Cart item serializer."""

    product_name = serializers.CharField(source="product.name", read_only=True)
    unit_price = serializers.DecimalField(source="product.price", max_digits=10, decimal_places=2, read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ("id", "product", "product_name", "unit_price", "quantity", "subtotal", "created_at")
        read_only_fields = ("id", "product_name", "unit_price", "subtotal", "created_at")

    def get_subtotal(self, obj):
        return obj.subtotal


class CartSerializer(serializers.ModelSerializer):
    """Cart serializer with nested items."""

    items = CartItemSerializer(many=True, read_only=True)
    total_value = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ("id", "user", "items", "total_value", "created_at", "updated_at")
        read_only_fields = ("id", "user", "items", "total_value", "created_at", "updated_at")


class AddCartItemSerializer(serializers.Serializer):
    """Add cart item input serializer."""

    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class UpdateCartItemSerializer(serializers.Serializer):
    """Update cart item quantity serializer."""

    quantity = serializers.IntegerField(min_value=1)


class OneTimeOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    image_url = serializers.URLField(source="product.image_url", read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OneTimeOrderItem
        fields = (
            "id",
            "product",
            "product_name",
            "image_url",
            "quantity",
            "unit_price",
            "subtotal",
        )
        read_only_fields = fields

    def get_subtotal(self, obj):
        return obj.subtotal


class OneTimeOrderSerializer(serializers.ModelSerializer):
    items = OneTimeOrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = OneTimeOrder
        fields = ("id", "status", "total_amount", "items", "created_at", "updated_at")
        read_only_fields = fields


class CheckoutSerializer(serializers.Serializer):
    payment_method = serializers.ChoiceField(
        choices=["CARD", "UPI", "NET_BANKING", "CASH"],
        default="UPI",
    )
