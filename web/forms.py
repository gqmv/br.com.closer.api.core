from django.forms import ModelForm
from django import forms

from api.services import WhatsAppService
from authentication.models import CustomUser
from stores.models import Store


class UserRegistrationForm(ModelForm):
    """
    Form for registering a new user.
    """

    accept_terms = forms.BooleanField(
        required=True,
        label="Eu aceito os termos de uso.",
        error_messages={"required": "Você precisa aceitar os termos de uso para se cadastrar."},
    )

    class Meta:
        model = CustomUser
        fields = ("tax_id", "phone_number", "first_name")

    def save(self, commit: bool = True, store_id: int = None) -> CustomUser:
        """
        Saves the user.
        If the optional parameter store_id is passed, a welcome message is sent to the user.
        """
        user = super().save(commit)
        store = Store.objects.filter(id=store_id)
        
        whatsapp_service = WhatsAppService()
        whatsapp_service.send_welcome_message(user)

        if store.exists():
            pass
        
        return user
