import factory

from tests.authentication.factories import CustomUserFactory
from stores.models import (
    Store,
    BaseCampaign,
    WelcomeCampaign,
    RegularCampaign,
    CampaignUser,
)


class StoreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Store

    name = factory.Faker("company")


class BaseCampaignFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BaseCampaign
        abstract = True

    name = factory.sequence(lambda n: f"Campaign {n}")
    reward_id = factory.sequence(lambda n: str(n))
    reward_name = factory.sequence(lambda n: f"Reward {n}")
    reward_qty = factory.sequence(lambda n: n)
    store = factory.SubFactory(StoreFactory)


class WelcomeCampaignFactory(BaseCampaignFactory):
    class Meta:
        model = WelcomeCampaign

    store = factory.SubFactory(StoreFactory)


class RegularCampaignFactory(BaseCampaignFactory):
    class Meta:
        model = RegularCampaign

    item_id = factory.sequence(lambda n: str(n))
    item_name = factory.sequence(lambda n: f"Item {n}")
    item_qty = factory.sequence(lambda n: n)


class CampaignUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CampaignUser

    campaign = factory.SubFactory(RegularCampaignFactory)
    user = factory.SubFactory(CustomUserFactory)
    progress = 0
