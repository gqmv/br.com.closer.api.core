from rest_framework import serializers

from .utils import update_campaign_user_progress, handle_campaign_user_rewards
from stores.models import Store, RegularCampaign, CampaignUser
from authentication.models import CustomUser


def get_valid_campaigns_from_item_id(
    item_id: str, store: Store
) -> list[RegularCampaign]:
    """
    Returns a iterable of valid campaigns for a given item id.
    """
    return RegularCampaign.objects.filter(item_id=item_id, store=store)


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

        campaigns = get_valid_campaigns_from_item_id(
            self.validated_data.get("item_id"), store
        )

        for campaign in campaigns:
            campaign_user = CampaignUser.objects.get_or_create(
                campaign=campaign, user=user
            )[
                0
            ]  # get_or_create returns a tuple with the object and a boolean indicating if it was created or not.

            campaign_user = update_campaign_user_progress(
                campaign_user, self.validated_data.get("item_qty")
            )

            if campaign_user.progress >= campaign.item_qty:
                handle_campaign_user_rewards(campaign_user)
