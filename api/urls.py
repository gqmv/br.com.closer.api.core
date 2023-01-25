from django.urls import path, include
from rest_framework import routers

from .views import RegisterUserView

router = routers.DefaultRouter()


urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
]

urlpatterns += router.urls
