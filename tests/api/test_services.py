import pytest

from api.services import (
    ComponentsBuilder,
    WhatsAppService,
    get_phone_number_as_whatsapp_id,
)
from tests.authentication.factories import CustomUserFactory
from tests.stores.factories import RegularCampaignFactory


@pytest.mark.django_db
class TestComponentsBuilder:
    def test_build_components(self):
        componentsBuilder = ComponentsBuilder()

        components = componentsBuilder.build()

        assert type(components) == list
        assert type(components[0]) == dict
        assert len(components) == 1
        assert components[0]["type"] == "body"
        assert components[0]["parameters"] == []

    def test_add_text(self):
        componentsBuilder = ComponentsBuilder()

        componentsBuilder.add_text("This is a test")
        componentsBuilder.add_text("This is another test")

        components = componentsBuilder.build()

        assert components[0]["parameters"][0]["type"] == "text"
        assert components[0]["parameters"][0]["text"] == "This is a test"

        assert components[0]["parameters"][1]["type"] == "text"
        assert components[0]["parameters"][1]["text"] == "This is another test"

    def test_add_user_info(self, mocker):
        add_text_mock = mocker.patch("api.services.ComponentsBuilder.add_text")

        user = CustomUserFactory()
        componentsBuilder = ComponentsBuilder()
        componentsBuilder.add_user_info(user)

        assert add_text_mock.called_once_with(user)

    def test_add_reward_info(self, mocker):
        add_text_mock = mocker.patch("api.services.ComponentsBuilder.add_text")

        campaign = RegularCampaignFactory()
        componentsBuilder = ComponentsBuilder()
        componentsBuilder.add_reward_info(campaign)

        assert add_text_mock.called_once_with(campaign.reward_qty)
        assert add_text_mock.called_once_with(campaign.reward_name)
        assert add_text_mock.called_once_with(campaign.store.name)

    def test_add_regular_campaign_info(self, mocker):
        add_text_mock = mocker.patch("api.services.ComponentsBuilder.add_text")
        add_reward_info_mock = mocker.patch(
            "api.services.ComponentsBuilder.add_reward_info"
        )

        campaign = RegularCampaignFactory()
        componentsBuilder = ComponentsBuilder()
        componentsBuilder.add_regular_campaign_info(campaign)

        assert add_text_mock.called_once_with(campaign.item_qty)
        assert add_text_mock.called_once_with(campaign.item_name)
        assert add_reward_info_mock.called_once_with(campaign)


@pytest.mark.django_db
class TestWhatsAppService:
    def test_send_template(self, mocker):
        mock_send_template = mocker.patch("api.services.WhatsApp.send_template")

        user = CustomUserFactory()
        components = ComponentsBuilder().build()
        whatsapp_service = WhatsAppService()
        whatsapp_service.send_template("template_name", user, components)

        assert mock_send_template.called_once_with(
            "template_name",
            get_phone_number_as_whatsapp_id(user.phone_number),
            components,
        )

    def test_send_welcome_message(self, mocker):
        mock_send_template = mocker.patch("api.services.WhatsApp.send_template")

        user = CustomUserFactory()
        whatsapp_service = WhatsAppService()
        whatsapp_service.send_welcome_message(user)

        components = mock_send_template.call_args.kwargs["components"]
        parameters = components[0]["parameters"]

        assert parameters[0]["type"] == "text"
        assert parameters[0]["text"] == user.first_name

    def test_send_coupon_message(self, mocker):
        mock_send_template = mocker.patch("api.services.WhatsApp.send_template")

        user = CustomUserFactory()
        campaign = RegularCampaignFactory()
        whatsapp_service = WhatsAppService()
        whatsapp_service.send_coupon_message(user, campaign, "coupon_code")

        components = mock_send_template.call_args.kwargs["components"]
        parameters = components[0]["parameters"]

        assert parameters[0]["type"] == "text"
        assert parameters[0]["text"] == campaign.reward_qty

        assert parameters[1]["type"] == "text"
        assert parameters[1]["text"] == campaign.reward_name

        assert parameters[2]["type"] == "text"
        assert parameters[2]["text"] == campaign.store.name

        assert parameters[3]["type"] == "text"
        assert parameters[3]["text"] == "coupon_code"
