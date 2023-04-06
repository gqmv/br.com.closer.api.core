from django.shortcuts import render
from django.http import HttpResponseRedirect
from stores.models import WelcomeCampaign
from .forms import UserRegistrationForm


def user_register(request, store_id: int = None):
    """
    View for registering a new user.
    It receives a store_id as a parameter, which is optional.
    """
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save(store_id=store_id)
            return HttpResponseRedirect("/")
    else:
        form = UserRegistrationForm()

    #pelo store id pegar a campanha de boas vindas + a loja

    welcome_campaign = WelcomeCampaign.objects.filter(store__id=store_id)

    try:
        welcome_campaign = welcome_campaign.get()
    except WelcomeCampaign.DoesNotExist:
        welcome_campaign = None
    
    return render(request, "registration.html", {"form": form, "welcome_campaign": welcome_campaign})
