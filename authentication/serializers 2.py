from rest_framework import serializers

from .models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.
    """

    class Meta:
        model = CustomUser
        fields = (
            "tax_id",
            "phone_number",
            "email",
            "first_name",
            "last_name",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}
