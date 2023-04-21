from django.urls import path, include
from rest_framework import routers
from .views import user_register, post_register, landing_page


urlpatterns = [
    path("", landing_page, name="landing-page"),
    path("register/", user_register, name="register"),
    path("register/<int:store_id>/", user_register, name="register-affiliated-store"),
    path("post-register/<str:user_first_name>/", post_register, name="post-register"),
    path("post-register/<str:user_first_name>/<int:store_id>/", post_register, name="post-register-affiliated-store"),
]
