"""Views for cart APIs."""

import uuid

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from payments.models import Payment
from products.models import Product

from .models import Cart, CartItem, OneTimeOrder, OneTimeOrderItem
from .permissions import IsCustomer
from .serializers import (
    AddCartItemSerializer,
    CartSerializer,
    CheckoutSerializer,
    OneTimeOrderSerializer,
    UpdateCartItemSerializer,
)


class CartDetailAPIView(generics.GenericAPIView):
    """Retrieve current authenticated customer's cart."""

    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return Response(self.get_serializer(cart).data)


class CartItemAPIView(generics.GenericAPIView):
    """Add/update/delete cart items for current customer."""

    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request, *args, **kwargs):
        serializer = AddCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, pk=serializer.validated_data["product_id"])

        if not product.is_available:
            return Response(
                {"detail": "Product is not available."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        quantity = serializer.validated_data["quantity"]
        existing_distinct_count = cart.items.count()
        if existing_distinct_count >= 5 and not cart.items.filter(product=product).exists():
            return Response(
                {"detail": "One time order cart supports up to 5 unique products."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if product.stock_quantity < quantity:
            return Response(
                {"detail": "Insufficient stock for requested quantity."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity},
        )
        if not created:
            new_quantity = item.quantity + quantity
            if product.stock_quantity < new_quantity:
                return Response(
                    {"detail": "Insufficient stock for requested quantity."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            item.quantity = new_quantity
            item.save(update_fields=["quantity"])

        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)

    def patch(self, request, item_id, *args, **kwargs):
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        item = get_object_or_404(CartItem, pk=item_id, cart=cart)
        if item.product.stock_quantity < serializer.validated_data["quantity"]:
            return Response(
                {"detail": "Insufficient stock for requested quantity."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        item.quantity = serializer.validated_data["quantity"]
        item.save(update_fields=["quantity"])
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    def delete(self, request, item_id, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item = get_object_or_404(CartItem, pk=item_id, cart=cart)
        item.delete()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)


class OneTimeCheckoutAPIView(generics.GenericAPIView):
    """Checkout cart as one-time order and create payment entry."""

    permission_classes = [IsAuthenticated, IsCustomer]
    serializer_class = CheckoutSerializer

    def post(self, request, *args, **kwargs):
        checkout_serializer = self.get_serializer(data=request.data)
        checkout_serializer.is_valid(raise_exception=True)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = list(cart.items.select_related("product").all())
        if not cart_items:
            return Response(
                {"detail": "Cart is empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(cart_items) > 5:
            return Response(
                {"detail": "One time order supports up to 5 products."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            with transaction.atomic():
                order = OneTimeOrder.objects.create(user=request.user)
                for cart_item in cart_items:
                    product = cart_item.product
                    if not product.is_available or product.stock_quantity < cart_item.quantity:
                        raise ValueError(f"Product '{product.name}' is unavailable or out of stock.")

                    OneTimeOrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=cart_item.quantity,
                        unit_price=product.price,
                    )

                    product.stock_quantity -= cart_item.quantity
                    product.save(update_fields=["stock_quantity"])

                order.recalculate_total()
                order.save(update_fields=["total_amount", "updated_at"])

                payment = Payment.objects.create(
                    user=request.user,
                    one_time_order=order,
                    amount=order.total_amount,
                    payment_method=checkout_serializer.validated_data["payment_method"],
                    transaction_id=f"OT-{uuid.uuid4().hex[:12].upper()}",
                    status=Payment.StatusChoices.PENDING,
                )

                cart.items.all().delete()
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "order": OneTimeOrderSerializer(order).data,
                "payment_id": payment.id,
                "transaction_id": payment.transaction_id,
            },
            status=status.HTTP_201_CREATED,
        )


class OneTimeOrderListAPIView(generics.ListAPIView):
    """List one-time orders for current customer."""

    serializer_class = OneTimeOrderSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_queryset(self):
        return OneTimeOrder.objects.filter(user=self.request.user).prefetch_related("items__product")
