from rest_framework import serializers

from .models import RegularCampaign, CampaignUser, Store


class CampaignUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignUser
        fields = ("campaign", "user", "progress")
