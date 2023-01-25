from django.test import TestCase
from django.contrib.auth import get_user_model


MOCK_USER_DATA = {
    "tax_id": "12345678910",
    "email": "a@a.com",
    "phone_number": "+5581999999999",
    "first_name": "John",
    "last_name": "Doe",
}

PASSWORD = "123456"


class CustomUserModelManagerTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(**MOCK_USER_DATA, password=PASSWORD)
        self.assertDictContainsSubset(MOCK_USER_DATA, user.__dict__)
        self.assertNotEqual(user.password, PASSWORD) # password is hashed
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            User.objects.create_user(**MOCK_USER_DATA, tax_id=None)
            

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(**MOCK_USER_DATA, password=PASSWORD)
        self.assertDictContainsSubset(MOCK_USER_DATA, admin_user.__dict__)
        self.assertNotEqual(admin_user.password, PASSWORD) # password is hashed
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                **MOCK_USER_DATA,
                is_staff=False,
            )

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                **MOCK_USER_DATA,
                is_superuser=False,
            )
