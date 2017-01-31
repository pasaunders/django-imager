"""Views."""
from django.shortcuts import render


def home_view(request):
    """The home view."""
    return render(request,
                  "imagersite/home.html"
                  )
