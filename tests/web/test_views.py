import pytest
from django.test import Client
from django.urls import reverse
from http import HTTPStatus

from authentication.models import CustomUser
from .factories import UserRegistrationFormDataFactory

from web.forms import UserRegistrationForm


@pytest.mark.django_db
class TestUserRegisterView:
    client = Client()
    url = reverse("register")

    def test_success(self):
        form_data = UserRegistrationFormDataFactory.build()
        response = self.client.post(self.url, data=form_data)

        assert response.status_code == HTTPStatus.FOUND

        user = CustomUser.objects.get(tax_id=form_data["tax_id"])

        assert user.first_name == form_data["first_name"]
        assert user.phone_number == form_data["phone_number"]

    def test_get(self):
        response = self.client.get(self.url)
        assert response.status_code == HTTPStatus.OK
        assert response.templates[0].name == "registration.html"

    def test_invalid_form_data(self, mocker):
        mock_form_save = mocker.patch("web.forms.UserRegistrationForm.save")

        form_data = UserRegistrationFormDataFactory.build()
        form_data["tax_id"] = "Banana"

        response = self.client.post(self.url, data=form_data)

        mock_form_save.assert_not_called()