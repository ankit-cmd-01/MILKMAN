"""Serializers for analytics response payloads."""

from rest_framework import serializers


class DashboardStatsSerializer(serializers.Serializer):
    total_customers = serializers.IntegerField()
    total_subscriptions = serializers.IntegerField()
    active_subscriptions = serializers.IntegerField()
    most_demanded_product = serializers.CharField(allow_blank=True)
    revenue_this_month = serializers.DecimalField(max_digits=12, decimal_places=2)
    revenue_total = serializers.DecimalField(max_digits=12, decimal_places=2)


class ProductDemandSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    demand_count = serializers.IntegerField()


class SubscriptionGrowthSerializer(serializers.Serializer):
    month = serializers.CharField()
    total = serializers.IntegerField()
