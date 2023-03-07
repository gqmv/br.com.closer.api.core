from django.urls import path, include
from rest_framework import routers

from .views import RegisterPurchase, PeriodicNotificationView

router = routers.DefaultRouter()


urlpatterns = [
    path("purchase/", RegisterPurchase.as_view(), name="api_purchase"),
    path(
        "send_periodic_notifications/",
        PeriodicNotificationView.as_view(),
        name="api_send_periodic_notifications",
    ),
]

urlpatterns += router.urls
