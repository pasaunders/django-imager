"""Profile views."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required(login_url='/accounts/login/')
def profile_view(request):
    """The user profile view."""
    return render(request,
                  "imager_profile/profile.html",
                  {"user": request.user}
                  )


def public_profile(request, username):
    """Public profile view."""
    return render(request,
                  "imager_profile/profile.html",
                  {"user": User.objects.get(username=username)}
                  )
