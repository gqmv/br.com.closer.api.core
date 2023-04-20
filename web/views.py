from django.shortcuts import render
from django.http import HttpResponseRedirect
from stores.models import WelcomeCampaign
from .forms import UserRegistrationForm
from authentication.models import CustomUser
from django.urls import reverse


def user_register(request, store_id: int = None):
    """
    View for registering a new user.
    It receives a store_id as a parameter, which is optional.
    """
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save(store_id=store_id)
            

            #redirect to the right post registration page wether or not the user is affiliated with a store
            kwargs = {"user_first_name": form.cleaned_data["first_name"]}
    
            if store_id:
                kwargs["store_id"] = store_id
                reverse_name = "post-register-affiliated-store"
            else:
                reverse_name = "post-register"
            
            url = reverse(reverse_name, kwargs=kwargs)
            return HttpResponseRedirect(url)
    else:
        form = UserRegistrationForm()


    #get the welcome campaign + store by store id
    welcome_campaign = WelcomeCampaign.objects.filter(store__id=store_id)

    try:
        welcome_campaign = welcome_campaign.get()
    except WelcomeCampaign.DoesNotExist:
        welcome_campaign = None
    
    return render(request, "registration.html", {"form": form, "welcome_campaign": welcome_campaign})


def post_register(request, user_first_name: str, store_id: int = None):
    """
    View thats displayed after registration
    """

    welcome_campaign = WelcomeCampaign.objects.filter(store__id=store_id)

    try:
        welcome_campaign = welcome_campaign.get()
    except WelcomeCampaign.DoesNotExist:
        welcome_campaign = None
    
    return render(request, "post_registration.html", {"user_first_name": user_first_name, "welcome_campaign": welcome_campaign})