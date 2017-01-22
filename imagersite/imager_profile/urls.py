"""Profile urls."""
from django.conf.urls import url
from .views import public_profile, profile_view

urlpatterns = [
    url(r'^(?P<username>\w+)', public_profile, name='public_profile'),
    url(r'^$', profile_view, name='private_profile')
]
