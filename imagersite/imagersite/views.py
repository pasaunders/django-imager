"""Views."""
from django.shortcuts import render
# from registration.backends.hmac.views import RegistrationView


def home_view(request):
    """The home view."""
    return render(request,
                  "imagersite/home.html"
                  )


def profile_view(request):
    """The user profile view."""
    return render(request,
                  "imagersite/profile.html"
                  )
