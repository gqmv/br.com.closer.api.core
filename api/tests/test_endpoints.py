from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from authentication.tests.factories import CustomUserFactory


class TestRegisterUserEndpoint(TestCase):

    endpoint = "/api/register/"
    client = APIClient()

    def test_register_post_success(self):
        user_dict = CustomUserFactory.stub().__dict__

        response = self.client.post(self.endpoint, user_dict)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["tax_id"], user_dict["tax_id"])

    def test_register_post_password_hashed(self):
        user_dict = CustomUserFactory.stub().__dict__

        response = self.client.post(self.endpoint, user_dict)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user_object = get_user_model().objects.get(tax_id=user_dict["tax_id"])
        self.assertNotEqual(user_object.password, user_dict["password"])

    def test_register_post_repeated_tax_id(self):
        user1_dict = CustomUserFactory.stub().__dict__
        user2_dict = CustomUserFactory.stub(tax_id=(user1_dict["tax_id"])).__dict__

        response1 = self.client.post(self.endpoint, user1_dict)
        response2 = self.client.post(self.endpoint, user2_dict)

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(response2.data.keys()), {"tax_id"})

    def test_register_post_repeated_email(self):
        user1_dict = CustomUserFactory.stub().__dict__
        user2_dict = CustomUserFactory.stub(email=(user1_dict["email"])).__dict__

        response1 = self.client.post(self.endpoint, user1_dict)
        response2 = self.client.post(self.endpoint, user2_dict)

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(response2.data.keys()), {"email"})

    def test_register_post_repeated_phone_number(self):
        user1_dict = CustomUserFactory.stub().__dict__
        user2_dict = CustomUserFactory.stub(
            phone_number=(user1_dict["phone_number"])
        ).__dict__

        response1 = self.client.post(self.endpoint, user1_dict)
        response2 = self.client.post(self.endpoint, user2_dict)

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(response2.data.keys()), {"phone_number"})

    def test_register_post_missing_fields(self):
        user_dict = CustomUserFactory.stub().__dict__
        user_dict.pop("tax_id")

        response = self.client.post(self.endpoint, user_dict)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(response.data.keys()), {"tax_id"})

    def test_register_post_set_superuser(self):
        user_dict = CustomUserFactory.stub().__dict__
        user_dict["is_staff"] = True
        user_dict["is_superuser"] = True

        response = self.client.post(self.endpoint, user_dict)

        user = get_user_model().objects.get(tax_id=user_dict["tax_id"])
        self.assertNotEqual(user.is_staff, user_dict["is_staff"])
        self.assertNotEqual(user.is_superuser, user_dict["is_superuser"])
        
        
