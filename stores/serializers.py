from rest_framework import serializers

from .models import RegularCampaign, CampaignUser, Store


class CampaignUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CampaignUser model.
    """

    class Meta:
        model = CampaignUser
        fields = ("campaign", "user", "progress")
