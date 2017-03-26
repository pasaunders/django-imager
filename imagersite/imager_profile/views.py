"""Profile views."""
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView
from imager_profile.forms import ProfileForm
from django.http import HttpResponseRedirect

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


class EditProfile(LoginRequiredMixin, UpdateView):
    """Edit users profile."""

    login_required = True
    template_name = 'imager_profile/edit_profile.html'
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('private_profile')

    def get_object(self):
        """Return logged in users profile."""
        return self.request.user.profile

    def form_valid(self, form):
        """Save object after post."""
        self.object = form.save()
        self.object.user.first_name = form.cleaned_data['First Name']
        self.object.user.last_name = form.cleaned_data['Last Name']
        self.object.user.email = form.cleaned_data['Email']
        self.object.user.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
