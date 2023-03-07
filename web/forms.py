from django.forms import ModelForm
from django import forms

from api.services import welcome_message
from authentication.models import CustomUser
from stores.models import Store


class UserRegistrationForm(ModelForm):
    accept_terms = forms.BooleanField(
        required=True,
        label="I accept the terms of use",
        error_messages={"required": "You must accept the terms of use to register."},
    )

    class Meta:
        model = CustomUser
        fields = ("tax_id", "phone_number", "first_name")

    def save(self, commit: bool = True, store_id: int = None) -> CustomUser:
        user = super().save(commit)
        store = Store.objects.filter(id=store_id)

        if store.exists():
            store = store.get()
            welcome_message(user, store)

        return user
