import os
from heyoo import WhatsApp

from authentication.models import CustomUser
from stores.models import CampaignUser, Store, BaseCampaign, RegularCampaign

"""
The contents of this file are definitely not ideal and should be refactored soon.
"""


class ComponentsBuilder:
    """
    This class is responsible for building the components of a WhatsApp message.
    To learn more about the components of a WhatsApp message, check out the documentation:
    https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-message-templates
    """

    def __init__(self):
        self.components = [
            {
                "type": "body",
                "parameters": [],
            }
        ]

    def add_text(self, text: str):
        """
        Adds a text field to the components.
        """
        self.components[0]["parameters"].append({"type": "text", "text": text})

    def add_user_info(self, user: CustomUser):
        """
        Adds the user information to the components.
        """
        self.add_text(user.first_name)

    def add_reward_info(self, campaign: BaseCampaign):
        """
        Adds the reward information to the components.
        """
        self.add_text(campaign.reward_qty)
        self.add_text(campaign.reward_name)
        self.add_text(campaign.store.name)

    def add_regular_campaign_info(self, campaign: RegularCampaign):
        """
        Adds information about a regular campaign to the components.
        """
        self.add_text(campaign.item_qty)
        self.add_text(campaign.item_name)
        self.add_reward_info(campaign)

    def build(self) -> list[dict]:
        """
        Returns the components.
        """
        return self.components


def get_phone_number_as_whatsapp_id(phone_number: str) -> str:
    """
    Returns the phone number as a WhatsApp ID.
    """
    return str(phone_number).replace("+", "")


class WhatsAppService:
    def __init__(self):
        self.messenger = WhatsApp(
            os.environ.get("WHATSAPP_TOKEN"), os.environ.get("WHATSAPP_NUMBER_ID")
        )

    def send_template(
        self, template: str, recipient: CustomUser, components: list[dict]
    ):
        """
        Sends a template message to the user.
        """
        user_number_id = get_phone_number_as_whatsapp_id(recipient.phone_number)
        self.messenger.send_template(
            template=template,
            recipient_id=user_number_id,
            lang=os.environ.get("WHATSAPP_LANG"),
            components=components,
        )

    def send_welcome_message(self, user: CustomUser):
        """
        Sends a welcome message to the user.
        """
        componentsBuilder = ComponentsBuilder()
        componentsBuilder.add_user_info(user)

        components = componentsBuilder.build()

        self.send_template(
            template="welcome_message",
            recipient=user,
            components=components,
        )

    def send_coupon_message(
        self, user: CustomUser, campaign: BaseCampaign, coupon: str
    ):
        """
        Sends a message to the user with the coupon code and the information about the campaign associated with the coupon.
        """
        componentsBuilder = ComponentsBuilder()
        componentsBuilder.add_reward_info(campaign)
        componentsBuilder.add_text(coupon)

        components = componentsBuilder.build()

        self.send_template(
            template="coupon",
            recipient=user,
            components=components,
        )

    def send_periodic_message(self, campaign_user_list: list[CampaignUser]):
        """
        Sends a periodic message to the user with the information about the campaigns passed as arguments.
        """

        def select_template(campaign_user_count: int) -> str:
            """
            Selects the template to be used for the message.
            """
            template_map = {1: "periodic_message_1", 2: "periodic_message_2"}

            try:
                return template_map[campaign_user_count]
            except KeyError:
                raise NotImplementedError

        template = select_template(len(campaign_user_list))
        user = campaign_user_list[0].user

        componentsBuilder = ComponentsBuilder()
        componentsBuilder.add_user_info(user)

        for campaign_user in campaign_user_list:
            componentsBuilder.add_regular_campaign_info(campaign_user.campaign)

        components = componentsBuilder.build()

        self.send_template(
            template=template,
            recipient=user,
            components=components,
        )
