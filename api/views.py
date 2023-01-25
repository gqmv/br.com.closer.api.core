from rest_framework.generics import CreateAPIView

from authentication.models import CustomUser
from authentication.serializers import RegisterUserSerializer


class RegisterUserView(CreateAPIView):
    """
    Endpoint for registering a new user.
    """

    queryset = CustomUser.objects.all()
    serializer_class = RegisterUserSerializer
