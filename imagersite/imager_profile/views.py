"""Profile views."""
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView

PROFILE_TEMPLATE_PATH = "imager_profile/profile.html"


class Profile(LoginRequiredMixin, ListView):
    """The user profile view."""

    login_url = reverse_lazy('login')

    model = User
    template_name = PROFILE_TEMPLATE_PATH


class PublicProfile(ListView):
    """Public profile view."""

    model = User
    template_name = PROFILE_TEMPLATE_PATH

    def get_context_data(self):
        """Return user object."""
        return {"user": User.objects.get(username=self.kwargs['username'])}
