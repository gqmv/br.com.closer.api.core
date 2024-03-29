import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from stores.services import DummyPOSService
from tests.stores.factories import (
    StoreFactory,
    RegularCampaignFactory,
    CampaignUserFactory,
)
from stores.models import CampaignUser
from .factories import PurchaseRegistrationRequestFactory
from tests.authentication.factories import CustomUserFactory
from api import utils as api_utils


@pytest.fixture
def user():
    return CustomUserFactory()


@pytest.fixture
def store1():
    return StoreFactory()


@pytest.fixture
def store2():
    return StoreFactory()


@pytest.fixture
def campaign1(store1):
    return RegularCampaignFactory(store=store1, item_qty=5)


@pytest.fixture
def campaign2(store2):
    return RegularCampaignFactory(store=store2, item_qty=5)


@pytest.fixture
def campaign3(store2):
    return RegularCampaignFactory(store=store2, item_qty=5)


@pytest.fixture
def campaign_user1(campaign1, user):
    return CampaignUserFactory(campaign=campaign1, user=user)


@pytest.fixture
def campaign_user2(campaign2, user):
    return CampaignUserFactory(campaign=campaign2, user=user)


@pytest.fixture
def campaign_user3(campaign3, user):
    return CampaignUserFactory(campaign=campaign3, user=user)


@pytest.mark.django_db
class TestPeriodicNotificationView:
    endpoint = reverse("api_send_periodic_notifications")
    client = APIClient()

    def test_success(self, user, campaign_user1, campaign_user2, mocker):
        mock_send_notification = mocker.patch(
            "api.views.WhatsAppService.send_periodic_message"
        )
        mock_permission = mocker.patch("core.permissions.GCPServicePermission.has_permission")
        mock_send_notification.return_value = None
        mock_permission.return_value = True
        x = self.client.post(self.endpoint)
        mock_send_notification.assert_called_once_with(campaign_user1, campaign_user2)


@pytest.mark.django_db
class TestRegisterPurchaseView:
    endpoint = reverse("api_purchase")
    client = APIClient()

    def test_success(self, user, campaign_user1):
        request = PurchaseRegistrationRequestFactory(
            user_entity=user,
            store_entity=campaign_user1.campaign.store,
            item_id=campaign_user1.campaign.item_id,
            item_qty=1,
        )

        response = self.client.post(self.endpoint, request)

        campaign_user1.refresh_from_db()
        assert campaign_user1.progress == 1
        assert response.status_code == status.HTTP_201_CREATED

    def test_tax_id_does_not_exits(self):
        request = PurchaseRegistrationRequestFactory(
            user="123456789",
            item_id=1,
            item_qty=1,
        )

        response = self.client.post(self.endpoint, request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("user", None) is not None

    def test_store_does_not_exist(self):
        request = PurchaseRegistrationRequestFactory(
            store=2,  # The factory creates a store with id=1
            item_id=1,
            item_qty=1,
        )

        response = self.client.post(self.endpoint, request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("store", None) is not None

    def test_campaign_user_does_not_exist(self, user, store1, campaign1, mocker):
        request = PurchaseRegistrationRequestFactory(
            user_entity=user,
            store_entity=store1,
            item_id=campaign1.item_id,
            item_qty=1,
        )

        campaign_user_creator = mocker.spy(CampaignUser.objects, "get_or_create")
        response = self.client.post(self.endpoint, request)

        campaign_user = CampaignUser.objects.get(user=user, campaign=campaign1)

        campaign_user_creator.assert_called_once()
        assert campaign_user_creator.spy_return == (campaign_user, True)
        assert response.status_code == status.HTTP_201_CREATED

    def test_coupon_generated(self, user, campaign_user1, mocker):
        request = PurchaseRegistrationRequestFactory(
            user_entity=user,
            store_entity=campaign_user1.campaign.store,
            item_id=campaign_user1.campaign.item_id,
            item_qty=campaign_user1.campaign.item_qty,
        )

        get_pos_service_mock = mocker.patch("api.utils.get_pos_service")
        get_pos_service_mock.return_value = DummyPOSService
        generate_coupon_mock = mocker.patch(
            "stores.services.DummyPOSService.generate_coupon_code"
        )
        notify_coupon_mock = mocker.patch(
            "api.utils.WhatsAppService.send_coupon_message"
        )
        generate_coupon_mock.return_value = "XXX-YYY-ZZZ"
        notify_coupon_mock.return_value = None

        response = self.client.post(self.endpoint, request)

        get_pos_service_mock.assert_called_once_with(
            campaign_user1.campaign.store.pos_service
        )
        generate_coupon_mock.assert_called_once()
        notify_coupon_mock.assert_called_once_with(user, campaign_user1.campaign, "XXX-YYY-ZZZ")

        assert response.status_code == status.HTTP_201_CREATED

    def test_store_with_no_pos_service(self, user, mocker):
        store = StoreFactory(pos_service=None)
        campaign = RegularCampaignFactory(store=store, item_qty=5)
        campaign_user = CampaignUserFactory(campaign=campaign, user=user)

        request = PurchaseRegistrationRequestFactory(
            user_entity=user,
            store_entity=store,
            item_id=campaign.item_id,
            item_qty=campaign.item_qty,
        )

        get_pos_service_mock = mocker.spy(api_utils, "get_pos_service")
        generate_coupon_mock = mocker.patch(
            "stores.services.DummyPOSService.generate_coupon_code"
        )
        notify_coupon_mock = mocker.patch(
            "api.utils.WhatsAppService.send_coupon_message"
        )

        response = self.client.post(self.endpoint, request)

        get_pos_service_mock.assert_called_once_with(store.pos_service)
        generate_coupon_mock.assert_not_called()
        notify_coupon_mock.assert_not_called()

        assert response.status_code == status.HTTP_201_CREATED
