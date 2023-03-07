import pytest
from django.contrib.auth import authenticate

from authentication.models import CustomUser
from authentication.exceptions import NullTaxIdError, InvalidPermissionError


MOCK_USER_DATA = {
    "tax_id": "12345678910",
    "phone_number": "+5581999999999",
    "first_name": "John",
}

PASSWORD = "123456"


@pytest.mark.django_db
class TestCustomUserModelManager:
    def test__create_user_success(self):
        mock = MOCK_USER_DATA.copy()
        user = CustomUser.objects._create_user(**mock, password=PASSWORD)

        assert mock.items() <= user.__dict__.items()
        assert user.password != PASSWORD

    def test__create_user_no_tax_id(self):
        mock = MOCK_USER_DATA.copy()
        mock["tax_id"] = None
        with pytest.raises(NullTaxIdError):
            CustomUser.objects._create_user(**mock, password=PASSWORD)

    def test__create_user_no_password(self):
        mock = MOCK_USER_DATA.copy()
        user = CustomUser.objects._create_user(**mock, password=None)

        assert mock.items() <= user.__dict__.items()
        assert (
            authenticate(tax_id=mock["tax_id"], password=None) == None
        )  # password is unusable

    def test_create_user_success(self):
        mock = MOCK_USER_DATA.copy()
        user = CustomUser.objects.create_user(**mock, password=PASSWORD)

        assert mock.items() <= user.__dict__.items()
        assert user.password != PASSWORD  # password is hashed
        assert not user.is_staff
        assert not user.is_superuser

    def test_create_user_superuser(self):
        mock = MOCK_USER_DATA.copy()
        mock["is_superuser"] = True
        mock["is_staff"] = True
        user = CustomUser.objects.create_user(**mock, password=PASSWORD)

        assert mock.items() <= user.__dict__.items()
        assert user.password != PASSWORD  # password is hashed
        assert user.is_staff
        assert user.is_superuser

    def test_create_superuser_success(self):
        mock = MOCK_USER_DATA.copy()
        admin_user = CustomUser.objects.create_superuser(
            **MOCK_USER_DATA, password=PASSWORD
        )

        assert mock.items() <= admin_user.__dict__.items()
        assert admin_user.password != PASSWORD  # password is hashed
        assert admin_user.is_staff
        assert admin_user.is_superuser

    def test_create_superuser_no_staff(self):
        mock = MOCK_USER_DATA.copy()
        mock["is_staff"] = False
        with pytest.raises(InvalidPermissionError):
            CustomUser.objects.create_superuser(**mock, password=PASSWORD)

    def test_create_superuser_no_superuser(self):
        mock = MOCK_USER_DATA.copy()
        mock["is_superuser"] = False
        with pytest.raises(InvalidPermissionError):
            CustomUser.objects.create_superuser(**mock, password=PASSWORD)
