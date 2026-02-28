"""Admin config for products app."""

from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
        "price",
        "stock_quantity",
        "unit",
        "is_available",
        "demand_count",
        "updated_at",
    )
    list_filter = ("category", "unit", "is_available")
    search_fields = ("name", "description")
    ordering = ("-updated_at",)

