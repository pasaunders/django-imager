"""Images urls."""
from django.conf.urls import url
from .views import photo_view, all_photos, single_album, all_albums

urlpatterns = [
    url(r'^photos/(?P<photo_id>\d+)', photo_view, name='public_profile'),
    url(r'^photos/$', all_photos, name='private_profile'),  # display all of the public photos that have been uploaded
    url(r'^albums/(?P<slug>[-\w]+)', single_album, name='single_album'),  # display a single selected album
    url(r'^albums/?', all_albums, name='all_albums')
]
