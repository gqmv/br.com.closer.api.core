from django.test import TestCase
from django.contrib.auth import get_user_model

MOCK_USER_DATA = {
    "tax_id": "12345678910",
    "email": "a@a.com",
    "phone_number": "+5581999999999",
    "first_name": "John",
    "last_name": "Doe",
}


class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            tax_id=MOCK_USER_DATA["tax_id"],
            email=MOCK_USER_DATA["email"],
            phone_number=MOCK_USER_DATA["phone_number"],
            first_name=MOCK_USER_DATA["first_name"],
            last_name=MOCK_USER_DATA["last_name"],
        )
        self.assertEquals(user.tax_id, MOCK_USER_DATA["tax_id"])
        self.assertEquals(user.email, MOCK_USER_DATA["email"])
        self.assertEquals(user.phone_number, MOCK_USER_DATA["phone_number"])
        self.assertEquals(user.first_name, MOCK_USER_DATA["first_name"])
        self.assertEquals(user.last_name, MOCK_USER_DATA["last_name"])
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            User.objects.create_user(
                tax_id=None,
                email=MOCK_USER_DATA["email"],
                phone_number=MOCK_USER_DATA["phone_number"],
                first_name=MOCK_USER_DATA["first_name"],
                last_name=MOCK_USER_DATA["last_name"],
            )

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            tax_id=MOCK_USER_DATA["tax_id"],
            email=MOCK_USER_DATA["email"],
            phone_number=MOCK_USER_DATA["phone_number"],
            first_name=MOCK_USER_DATA["first_name"],
            last_name=MOCK_USER_DATA["last_name"],
        )
        self.assertEquals(admin_user.tax_id, MOCK_USER_DATA["tax_id"])
        self.assertEquals(admin_user.email, MOCK_USER_DATA["email"])
        self.assertEquals(admin_user.phone_number, MOCK_USER_DATA["phone_number"])
        self.assertEquals(admin_user.first_name, MOCK_USER_DATA["first_name"])
        self.assertEquals(admin_user.last_name, MOCK_USER_DATA["last_name"])
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                tax_id=MOCK_USER_DATA["tax_id"],
                email=MOCK_USER_DATA["email"],
                phone_number=MOCK_USER_DATA["phone_number"],
                first_name=MOCK_USER_DATA["first_name"],
                last_name=MOCK_USER_DATA["last_name"],
                is_staff=False,
            )

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                tax_id=MOCK_USER_DATA["tax_id"],
                email=MOCK_USER_DATA["email"],
                phone_number=MOCK_USER_DATA["phone_number"],
                first_name=MOCK_USER_DATA["first_name"],
                last_name=MOCK_USER_DATA["last_name"],
                is_superuser=False,
            )
