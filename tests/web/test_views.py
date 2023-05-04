import pytest
from django.test import Client
from django.urls import reverse
from http import HTTPStatus
from bs4 import BeautifulSoup
from authentication.models import CustomUser
from .factories import UserRegistrationFormDataFactory
from tests.stores.factories import WelcomeCampaignFactory, StoreFactory
from web.forms import UserRegistrationForm


@pytest.mark.django_db
class TestUserRegisterView:
    """
    TODO: Test the sucessfull post with affiliated store
    TODO: Test the sucessfull get with affiliated store
    """
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



@pytest.mark.django_db
class TestUserPostRegisterView:
    client = Client()
    urls = ["register", "register-affiliated-store", "post-register", "post-register-affiliated-store"]
    kwargs = {"user_first_name": "Jonh"}

    def test_success_redirect(self):
        form_data = UserRegistrationFormDataFactory.build()
        self.kwargs["user_first_name"] = form_data["first_name"]

        url = reverse(self.urls[0])
        response = self.client.post(url, data=form_data)

        assert response.status_code == HTTPStatus.FOUND
        assert response.has_header("Location")
        assert response["Location"] == reverse(self.urls[2], kwargs=self.kwargs)
        

    def test_success_redirect_affiliated_store(self):
        store = WelcomeCampaignFactory.create().store
        form_data = UserRegistrationFormDataFactory.build()
        self.kwargs["user_first_name"] = form_data["first_name"]
        self.kwargs["store_id"] = store.id

        url = reverse(self.urls[1], kwargs={"store_id": store.id})
        response = self.client.post(url, data=form_data)

        assert response.status_code == HTTPStatus.FOUND
        assert response.has_header("Location")
        assert response["Location"] == reverse(self.urls[3], kwargs=self.kwargs)

    def test_get(self):
        url = reverse(self.urls[2], kwargs=self.kwargs)
        response = self.client.get(url)
        
        assert response.status_code == HTTPStatus.OK
        assert response.templates[0].name == "post_registration.html"

        soup = BeautifulSoup(response.content, "html.parser")
        store_name = soup.select_one(".store-name")
        assert store_name is None
        

    def test_get_affiliated_store(self):
        store = WelcomeCampaignFactory.create().store
        self.kwargs["store_id"] = store.id
        url = reverse(self.urls[3], kwargs=self.kwargs)

        response = self.client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert response.templates[0].name == "post_registration.html"

        soup = BeautifulSoup(response.content, "html.parser")
        store_name = soup.select_one(".store-name")
        assert store_name.text == store.name

    def test_get_null_store(self):
        self.kwargs["store_id"] = 0
        url = reverse(self.urls[3], kwargs=self.kwargs)

        response = self.client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert response.templates[0].name == "post_registration.html"

        soup = BeautifulSoup(response.content, "html.parser")
        store_name = soup.select_one(".store-name")
        assert store_name is None

    def test_get_null_welcome_campaign(self):
        store = StoreFactory()
        self.kwargs["store_id"] = store.id
        url = reverse(self.urls[3], kwargs=self.kwargs)

        response = self.client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert response.templates[0].name == "post_registration.html"

        soup = BeautifulSoup(response.content, "html.parser")
        store_name = soup.select_one(".store-name")
        assert store_name is None
        