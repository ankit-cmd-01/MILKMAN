"""Product serializers."""

from decimal import Decimal

from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for product categories."""

    class Meta:
        model = Category
        fields = ("id", "name", "description", "created_at")
        read_only_fields = ("id", "created_at")


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for products."""

    category_name = serializers.CharField(source="category.name", read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    stock_warning = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "category_name",
            "name",
            "description",
            "image_url",
            "price",
            "stock_quantity",
            "unit",
            "is_available",
            "is_low_stock",
            "stock_warning",
            "demand_count",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "demand_count", "created_at", "updated_at")

    def validate_price(self, value: Decimal):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    def validate_stock_quantity(self, value: int):
        if value < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative.")
        return value

    def get_stock_warning(self, obj):
        if obj.is_low_stock:
            return f"Low stock: only {obj.stock_quantity} left"
        return ""
