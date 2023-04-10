from django.urls import path, include
from rest_framework import routers

from .views import user_register, landing_page


urlpatterns = [
    path("register/", user_register, name="register"),
    path("register/<int:store_id>/", user_register, name="register-affiliated-store"),
    path("", landing_page, name="landing-page"),
]
