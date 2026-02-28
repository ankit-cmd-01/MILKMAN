"""URL routes for analytics app."""

from django.urls import path

from .views import DashboardAnalyticsAPIView, ProductDemandStatsAPIView, SubscriptionGrowthAPIView


urlpatterns = [
    path("dashboard/", DashboardAnalyticsAPIView.as_view(), name="analytics-dashboard"),
    path("product-demand/", ProductDemandStatsAPIView.as_view(), name="analytics-product-demand"),
    path("subscription-growth/", SubscriptionGrowthAPIView.as_view(), name="analytics-subscription-growth"),
]
