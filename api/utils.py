from stores.models import CampaignUser

def select_relevant_campaigns(user):
    """_summary_
    Selects the most relevant campaigns for a user.
    """
    campaign_users = CampaignUser.objects.filter(user=user)
    campaign_users.order_by("campaign__store__name")
    
    if len(campaign_users) >= 2:
        return campaign_users[:2]
    
    return list(campaign_users)
    
    