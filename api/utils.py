from stores.models import CampaignUser
from authentication.models import CustomUser
from django.db.models import F

from .services import WhatsAppService
from stores.services import get_pos_service


def select_relevant_campaign_user_list(user: CustomUser) -> list[CampaignUser]:
    """
    Selects the most relevant campaigns for a user.
    Currently, the most relevant campaigns are selected by the store name. (should be changed to something else)
    """
    campaign_users = CampaignUser.objects.filter(user=user)
    campaign_users.order_by("campaign__store__name")

    if len(campaign_users) >= 2:
        return campaign_users[:2]

    return list(campaign_users)


def handle_campaign_user_rewards(campaign_user: CampaignUser):
    """
    Handles the rewards for a campaign user.
    """
    pos_service_class = get_pos_service(campaign_user.campaign.store.pos_service)

    if pos_service_class is None:
        return

    pos_service = pos_service_class()
    whatsapp_service = WhatsAppService()
    while campaign_user.progress >= campaign_user.campaign.item_qty:
        coupon = pos_service.generate_coupon_code(
            campaign_user.campaign.store,
            campaign_user.campaign.reward_id,
            campaign_user.campaign.reward_qty,
        )

        whatsapp_service.send_coupon_message(
            campaign_user.user, campaign_user.campaign, coupon
        )
        update_campaign_user_progress(campaign_user, -campaign_user.campaign.item_qty)


def update_campaign_user_progress(campaign_user: CampaignUser, item_qty_diff: int):
    """
    Updates the progress of a campaign.
    """
    campaign_user.progress = F("progress") + item_qty_diff
    campaign_user.save()
    campaign_user.refresh_from_db()

    return campaign_user
