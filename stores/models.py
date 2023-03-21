from django.db import models
from django.contrib.auth import get_user_model


class Store(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BaseCampaign(models.Model):
    """
    Abstract model for campaigns.
    """

    name = models.CharField(max_length=100)
    reward_id = models.CharField(max_length=100)
    reward_name = models.CharField(max_length=100)
    reward_qty = models.IntegerField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class WelcomeCampaign(BaseCampaign):
    """
    A campaign that is triggered when a user registers in the system with an affiliated store.
    """

    store = models.OneToOneField(Store, on_delete=models.CASCADE, unique=True)


class RegularCampaign(BaseCampaign):
    """
    A campaign that is triggered when a user makes "item_qty" purchases of "item_id".
    """

    item_id = models.CharField(max_length=100)
    item_name = models.CharField(max_length=100)
    item_qty = models.IntegerField()

    def __str__(self):
        return self.name


class CampaignUser(models.Model):
    """
    A model that represents the progress of a user in a campaign.
    """

    campaign = models.ForeignKey(RegularCampaign, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)

    def __str__(self):
        return self.user.first_name
