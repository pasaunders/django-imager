"""Profile urls."""
from django.conf.urls import url
from .views import Profile, PublicProfile, EditProfile
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^edit', EditProfile.as_view(), name='edit-profile'),
    url(r'^(?P<username>\w+)', PublicProfile.as_view(), name='public_profile'),
    url(r'^$', login_required(Profile.as_view()), name='private_profile')
]
