from django.urls import path, include
from rest_framework import routers

from .views import user_register


urlpatterns = [
    path("register/", user_register, name="register"),
    path("register/<int:store_id>/", user_register, name="register-affiliated-store"),
]
