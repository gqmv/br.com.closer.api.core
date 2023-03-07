import os
from heyoo import WhatsApp

from authentication.models import CustomUser
from stores.models import CampaignUser, Store


def generate_coupon(store, item, quantity):
    return "XXX-YYY-ZZZ"


class ComponentsBuilder:
    def __init__(self):
        self.components = [
            {
                "type": "body",
                "parameters": [],
            }
        ]

    def add_text(self, text):
        self.components[0]["parameters"].append({"type": "text", "text": text})

    def build(self):
        return self.components


def welcome_message(user: CustomUser, store: Store):
    if store.welcomecampaign is None:
        return

    messenger = WhatsApp(
        os.environ.get("WHATSAPP_TOKEN"), os.environ.get("WHATSAPP_NUMBER_ID")
    )

    componentsBuilder = ComponentsBuilder()
    componentsBuilder.add_text(user.first_name)
    componentsBuilder.add_text(store.welcomecampaign.reward_qty)
    componentsBuilder.add_text(store.welcomecampaign.reward_name)
    componentsBuilder.add_text(store.name)
    componentsBuilder.add_text("XXX-YYY-ZZZ")

    components = componentsBuilder.build()

    user_number_id = str(user.phone_number).replace("+", "")
    messenger.send_template(
        template="welcome_message",
        recipient_id=user_number_id,
        lang=os.environ.get("WHATSAPP_LANG"),
        components=components,
    )


def notify_coupon(user: CustomUser, coupon: str, campaign: CampaignUser):
    messenger = WhatsApp(
        os.environ.get("WHATSAPP_TOKEN"), os.environ.get("WHATSAPP_NUMBER_ID")
    )

    componentsBuilder = ComponentsBuilder()
    componentsBuilder.add_text(campaign.campaign.reward_qty)
    componentsBuilder.add_text(campaign.campaign.reward_name)
    componentsBuilder.add_text(campaign.campaign.store.name)
    componentsBuilder.add_text(campaign.campaign.item_name)
    componentsBuilder.add_text(campaign.campaign.item_qty)
    componentsBuilder.add_text(coupon)

    components = componentsBuilder.build()

    user_number_id = str(user.phone_number).replace("+", "")
    messenger.send_template(
        template="reward",
        recipient_id=user_number_id,
        lang=os.environ.get("WHATSAPP_LANG"),
        components=components,
    )


def periodic_notification(user: CustomUser, *campaign_users: CampaignUser):
    if len(campaign_users) == 2:
        _periodic_notification(user, campaign_users)
    else:
        raise NotImplementedError


def _periodic_notification(user: CustomUser, *campaign_users: CampaignUser):
    messenger = WhatsApp(
        os.environ.get("WHATSAPP_TOKEN"), os.environ.get("WHATSAPP_NUMBER_ID")
    )

    campaign1 = campaign_users[0]
    campaign2 = campaign_users[1]

    user_name = user.first_name

    campaign1_store_name = campaign1.campaign.store.name
    campaign1_item_qty_left = campaign1.campaign.item_qty - campaign1.progress
    campaign1_item = campaign1.campaign.item_name
    campaign1_reward = (
        f"{campaign1.campaign.reward_qty} {campaign1.campaign.reward_name}"
    )

    campaign2_store_name = campaign2.campaign.store.name
    campaign2_item_qty_left = campaign2.campaign.item_qty - campaign2.progress
    campaign2_item = campaign2.campaign.item_name
    campaign2_reward = (
        f"{campaign2.campaign.reward_qty} {campaign2.campaign.reward_name}"
    )

    componentsBuilder = ComponentsBuilder()
    componentsBuilder.add_text(user_name)
    componentsBuilder.add_text(campaign1_store_name)
    componentsBuilder.add_text(campaign1_item_qty_left)
    componentsBuilder.add_text(campaign1_item)
    componentsBuilder.add_text(campaign1_reward)
    componentsBuilder.add_text(campaign2_store_name)
    componentsBuilder.add_text(campaign2_item_qty_left)
    componentsBuilder.add_text(campaign2_item)
    componentsBuilder.add_text(campaign2_reward)

    components = componentsBuilder.build()

    user_number_id = str(user.phone_number).replace("+", "")
    messenger.send_template(
        template="periodic_message",
        recipient_id=user_number_id,
        lang=os.environ.get("WHATSAPP_LANG"),
        components=components,
    )
