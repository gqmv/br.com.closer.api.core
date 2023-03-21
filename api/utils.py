from stores.models import CampaignUser
from authentication.models import CustomUser


def select_relevant_campaigns(user: CustomUser) -> list[CampaignUser]:
    """
    Selects the most relevant campaigns for a user.
    Currently, the most relevant campaigns are selected by the store name. (should be changed to something else)
    """
    campaign_users = CampaignUser.objects.filter(user=user)
    campaign_users.order_by("campaign__store__name")

    if len(campaign_users) >= 2:
        return campaign_users[:2]

    return list(campaign_users)
