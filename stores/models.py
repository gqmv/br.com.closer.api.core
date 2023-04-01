from django.db import models
from django.contrib.auth import get_user_model
from django_cryptography.fields import encrypt
from django.utils.translation import gettext_lazy as _

from stores.services import AbstractPOSServiceRegistry


class Store(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=100)
    pos_service = models.CharField(
        verbose_name=_("POS service"),
        max_length=30,
        choices=AbstractPOSServiceRegistry.get_django_choices(),
        null=True,
        blank=True,
    )
    api_key = encrypt(
        models.CharField(
            verbose_name=_("API key"), max_length=100, null=True, blank=True
        )
    )

    def __str__(self):
        return self.name


class BaseCampaign(models.Model):
    """
    Abstract model for campaigns.
    """

    name = models.CharField(verbose_name=_("Nome"), max_length=100)
    reward_id = models.CharField(verbose_name=_("Reward ID"), max_length=100)
    reward_name = models.CharField(verbose_name=_("Reward name"), max_length=100)
    reward_qty = models.IntegerField(verbose_name=_("Reward quantity"))
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class WelcomeCampaign(BaseCampaign):
    """
    A campaign that is triggered when a user registers in the system with an affiliated store.
    """

    store = models.OneToOneField(
        Store, verbose_name=_("Store"), on_delete=models.CASCADE, unique=True
    )


class RegularCampaign(BaseCampaign):
    """
    A campaign that is triggered when a user makes "item_qty" purchases of "item_id".
    """

    item_id = models.CharField(verbose_name=_("Item ID"), max_length=100)
    item_name = models.CharField(verbose_name=_("Item name"), max_length=100)
    item_qty = models.IntegerField(verbose_name=_("Item quantity"))

    def __str__(self):
        return self.name


class CampaignUser(models.Model):
    """
    A model that represents the progress of a user in a campaign.
    """

    campaign = models.ForeignKey(
        RegularCampaign, verbose_name=_("Campaign"), on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        get_user_model(), verbose_name=_("User"), on_delete=models.CASCADE
    )
    progress = models.IntegerField(verbose_name=_("Progress"), default=0)

    def __str__(self):
        return self.user.first_name
