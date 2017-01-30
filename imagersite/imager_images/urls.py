"""Images urls."""
from django.conf.urls import url
from .views import photo_view, all_photos, single_album, all_albums, library

urlpatterns = [
    url(r'^photos/(?P<photo_id>\d+)', photo_view, name='single_photo'),
    url(r'^photos/$', all_photos, name='private_profile'),  # display all of the public photos that have been uploaded
    url(r'^albums/(?P<album_id>\d+)', single_album, name='single_album'),  # display a single selected album
    url(r'^albums/?', all_albums, name='all_albums'),
    url(r'^library$', library, name='library'),
]
