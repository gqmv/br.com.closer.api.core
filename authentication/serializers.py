from rest_framework import serializers

from .models import CustomUser


class RegisterUserSerializer(serializers.ModelSerializer):
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
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}},
        }

    
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)