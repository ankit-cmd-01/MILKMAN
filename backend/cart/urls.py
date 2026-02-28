"""URL routes for cart app."""

from django.urls import path

from .views import CartDetailAPIView, CartItemAPIView, OneTimeCheckoutAPIView, OneTimeOrderListAPIView


urlpatterns = [
    path("", CartDetailAPIView.as_view(), name="cart-detail"),
    path("items/", CartItemAPIView.as_view(), name="cart-add-item"),
    path("items/<int:item_id>/", CartItemAPIView.as_view(), name="cart-item-update-delete"),
    path("checkout/", OneTimeCheckoutAPIView.as_view(), name="one-time-checkout"),
    path("orders/", OneTimeOrderListAPIView.as_view(), name="one-time-orders"),
]
