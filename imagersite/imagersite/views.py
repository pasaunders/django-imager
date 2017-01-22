"""Views."""
from django.shortcuts import render
# from registration.backends.hmac.views import RegistrationView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def home_view(request):
    """The home view."""
    return render(request,
                  "imagersite/home.html"
                  )


@login_required(login_url='/accounts/login/')
def profile_view(request):
    """The user profile view."""
    user = {"user": request.user}
    user['public'] = False
    return render(request,
                  "imagersite/profile.html",
                  user
                  )


def public_profile(request, username):
    """Public profile view."""
    user = {"user": User.objects.get(username=username)}
    user['public'] = True
    return render(request,
                  "imagersite/profile.html",
                  user
                  )
