from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import UserRegistrationForm


def user_register(request, store_id: int = None):
    """
    View for registering a new user.
    It receives a store_id as a parameter, which is optional.
    """
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(store_id=store_id)
            return HttpResponseRedirect("/")
    else:
        form = UserRegistrationForm()

    return render(request, "registration.html", {"form": form})
