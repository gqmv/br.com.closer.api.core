from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField
from cpf_field.models import CPFField


class CustomUserManager(BaseUserManager):
    def _create_user(
        self,
        tax_id,
        phone_number,
        email,
        first_name,
        last_name,
        password,
        **extra_fields
    ):
        if not tax_id:
            raise TypeError("Users must have a tax_id.")

        email = self.normalize_email(email)
        UserModel = self.model

        user = UserModel(
            tax_id=tax_id,
            phone_number=phone_number,
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )

        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        tax_id,
        phone_number,
        email,
        first_name,
        last_name,
        password=None,
        **extra_fields
    ):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(
            tax_id, phone_number, email, first_name, last_name, password, **extra_fields
        )

    def create_superuser(
        self,
        tax_id,
        phone_number,
        email,
        first_name,
        last_name,
        password=None,
        **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(
            tax_id, phone_number, email, first_name, last_name, password, **extra_fields
        )


class CustomUser(AbstractBaseUser, PermissionsMixin):
    tax_id = CPFField("CPF", blank=False, unique=True)
    email = models.EmailField(_("email address"), blank=False, unique=True)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True, region="BR")
    first_name = models.CharField(_("first name"), max_length=20, blank=False)
    last_name = models.CharField(_("last name"), max_length=20, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "tax_id"
    REQUIRED_FIELDS = ["email", "phone_number", "first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.tax_id
