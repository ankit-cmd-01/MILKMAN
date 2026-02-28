"""Admin config for cart app."""

from django.contrib import admin

from .models import Cart, CartItem, OneTimeOrder, OneTimeOrderItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "updated_at")
    search_fields = ("user__email",)
    ordering = ("-updated_at",)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product", "quantity", "created_at")
    list_filter = ("created_at",)
    search_fields = ("cart__user__email", "product__name")
    ordering = ("-created_at",)


@admin.register(OneTimeOrder)
class OneTimeOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "total_amount", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__email",)
    ordering = ("-created_at",)


@admin.register(OneTimeOrderItem)
class OneTimeOrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "unit_price", "created_at")
    search_fields = ("order__user__email", "product__name")
    ordering = ("-created_at",)
