"""Views."""
from django.shortcuts import render
import registration.backends.hmac.views.RegistrationView


def home_view(request):
    """The home view."""
    return render(request,
                  "imagersite/home.html"
                  )
