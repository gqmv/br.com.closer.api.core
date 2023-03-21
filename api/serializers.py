from rest_framework import serializers
from cpf_field.models import CPFField

from .utils import update_campaign_user_progress
from stores.models import Store, RegularCampaign, CampaignUser
from authentication.models import CustomUser


class PurchaseSerializer(serializers.Serializer):
    """
    Serializer responsible for parsing the purchase registration request.
    """

    user = serializers.SlugRelatedField(
        queryset=CustomUser.objects.all(), slug_field="tax_id", many=False
    )
    store = serializers.PrimaryKeyRelatedField(queryset=Store.objects.all(), many=False)
    item_id = (
        serializers.CharField()
    )  # Different systems might use different id formats. To account for that, we use a string.
    item_qty = serializers.IntegerField()

    def save(self, *args, **kwargs):
        """
        Saves the purchase by updating the campaign progress and creating a new coupon if necessary.
        """
        user = self.validated_data.get("user")
        store = self.validated_data.get("store")

        campaigns = RegularCampaign.objects.filter(
            store=store, item_id=self.validated_data.get("item_id")
        )

        for campaign in campaigns:
            try:
                campaign_user = CampaignUser.objects.get(campaign=campaign, user=user)
            except CampaignUser.DoesNotExist:
                campaign_user = CampaignUser.objects.create(
                    campaign=campaign, user=user
                )

            update_campaign_user_progress(
                campaign_user, self.validated_data.get("item_qty")
            )
