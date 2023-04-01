from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django_cpf_cnpj.fields import CPFField

from .exceptions import NullTaxIdError, InvalidPermissionError


class CustomUserManager(BaseUserManager):
    def _create_user(
        self,
        tax_id: str,
        phone_number: str,
        first_name: str,
        password: str = None,
        **extra_fields
    ) -> "CustomUser":
        """
        Used as a helper method for creating a user.
        """
        if not tax_id:
            raise NullTaxIdError()

        UserModel = self.model

        user = UserModel(
            tax_id=tax_id,
            phone_number=phone_number,
            first_name=first_name,
            **extra_fields
        )

        user.save(using=self._db)
        return user

    def create_user(
        self,
        tax_id: str,
        phone_number: str,
        first_name: str,
        password: str = None,
        **extra_fields
    ) -> "CustomUser":
        """
        Creates and saves a user with the given tax_id, phone_number, first_name and password.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(
            tax_id, phone_number, first_name, password, **extra_fields
        )

    def create_superuser(
        self,
        tax_id: str,
        phone_number: str,
        first_name: str,
        password: str = None,
        **extra_fields
    ) -> "CustomUser":
        """
        Creates and saves a superuser with the given tax_id, phone_number, first_name and password.
        It also sets is_staff and is_superuser to True.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise InvalidPermissionError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise InvalidPermissionError("Superuser must have is_superuser=True.")

        return self._create_user(
            tax_id, phone_number, first_name, password, **extra_fields
        )


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses CPF as the unique identifier instead of username.
    """

    class Meta:
        verbose_name = _("User")

    tax_id = CPFField(verbose_name=_("CPF"), blank=False, unique=True)
    phone_number = PhoneNumberField(
        verbose_name=_("Phone Number"),
        null=False,
        blank=False,
        unique=True,
        region="BR",
    )
    first_name = models.CharField(_("First Name"), max_length=20, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "tax_id"
    REQUIRED_FIELDS = ["phone_number", "first_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.tax_id.__str__()

    def save(self, *args, **kwargs):
        if not self.password:
            self.set_unusable_password()

        super().save(*args, **kwargs)
