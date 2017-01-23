"""Images urls."""
from django.conf.urls import url
from .views import photo_view, all_photos

urlpatterns = [
    url(r'^photos/(?P<photo_id>\d+)', photo_view, name='public_profile'),
    url(r'^photos/$', all_photos, name='private_profile')  # display all of the public photos that have been uploaded
]
