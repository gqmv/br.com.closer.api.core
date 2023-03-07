import pytest

from web.forms import UserRegistrationForm
from .factories import UserRegistrationFormDataFactory
from tests.stores.factories import WelcomeCampaignFactory


@pytest.mark.django_db
class TestUserRegistrationForm:
    def test_success_no_store(self, mocker):
        form_data = UserRegistrationFormDataFactory.build()

        form = UserRegistrationForm(data=form_data)

        assert form.is_valid()

        mock_welcome_message = mocker.patch("web.forms.welcome_message")
        mock_welcome_message.return_value = None

        user = form.save()

        mock_welcome_message.assert_not_called()

        assert user.tax_id == form_data["tax_id"]
        assert user.phone_number == form_data["phone_number"]
        assert user.first_name == form_data["first_name"]

    def test_success_referral_store(self, mocker):
        store = WelcomeCampaignFactory.create().store

        form_data = UserRegistrationFormDataFactory.build()
        form = UserRegistrationForm(data=form_data)

        assert form.is_valid()

        mock_welcome_message = mocker.patch("web.forms.welcome_message")
        mock_welcome_message.return_value = None

        user = form.save(store_id=store.id)

        mock_welcome_message.assert_called_once_with(user, store)
