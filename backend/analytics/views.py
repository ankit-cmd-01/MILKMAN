"""Views serving admin dashboard analytics."""

from datetime import date
from decimal import Decimal

from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from payments.models import Payment
from products.models import Product
from subscriptions.models import Subscription
from users.models import User

from .permissions import IsAnalyticsAdmin
from .serializers import (
    DashboardStatsSerializer,
    ProductDemandSerializer,
    SubscriptionGrowthSerializer,
)


class DashboardAnalyticsAPIView(APIView):
    """Aggregated metrics for admin dashboard."""

    permission_classes = [IsAuthenticated, IsAnalyticsAdmin]

    def get(self, request, *args, **kwargs):
        now = date.today()
        month_start = now.replace(day=1)

        successful_payments = Payment.objects.filter(status=Payment.StatusChoices.SUCCESS)
        this_month_revenue = successful_payments.filter(paid_at__date__gte=month_start).aggregate(
            total=Sum("amount")
        )["total"] or Decimal("0.00")
        total_revenue = successful_payments.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

        most_demanded = Product.objects.order_by("-demand_count", "name").first()
        payload = {
            "total_customers": User.objects.filter(role=User.Roles.CUSTOMER, is_active=True).count(),
            "total_subscriptions": Subscription.objects.count(),
            "active_subscriptions": Subscription.objects.filter(
                status=Subscription.StatusChoices.ACTIVE
            ).count(),
            "most_demanded_product": most_demanded.name if most_demanded else "",
            "revenue_this_month": this_month_revenue,
            "revenue_total": total_revenue,
        }
        serializer = DashboardStatsSerializer(payload)
        return Response(serializer.data)


class ProductDemandStatsAPIView(APIView):
    """Demand counts by product for dashboard charts."""

    permission_classes = [IsAuthenticated, IsAnalyticsAdmin]

    def get(self, request, *args, **kwargs):
        products = Product.objects.order_by("-demand_count", "name").values(
            "id",
            "name",
            "demand_count",
        )
        payload = [
            {
                "product_id": row["id"],
                "product_name": row["name"],
                "demand_count": row["demand_count"],
            }
            for row in products
        ]
        serializer = ProductDemandSerializer(payload, many=True)
        return Response(serializer.data)


class SubscriptionGrowthAPIView(APIView):
    """Monthly subscription growth for admin charts."""

    permission_classes = [IsAuthenticated, IsAnalyticsAdmin]

    def get(self, request, *args, **kwargs):
        rows = (
            Subscription.objects.annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(total=Count("id"))
            .order_by("month")
        )
        payload = [
            {
                "month": row["month"].strftime("%Y-%m"),
                "total": row["total"],
            }
            for row in rows
        ]
        serializer = SubscriptionGrowthSerializer(payload, many=True)
        return Response(serializer.data)
