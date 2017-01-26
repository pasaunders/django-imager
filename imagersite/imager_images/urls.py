"""Images urls."""
from django.conf.urls import url
from .views import PhotosView, single_album, all_albums, library, PhotoView

urlpatterns = [
    url(r'^photos/(?P<photo_id>\d+)', PhotoView.as_view(), name='public_profile'),
    url(r'^photos/$', PhotosView.as_view(), name='private_profile'),  # display all of the public photos that have been uploaded
    url(r'^albums/(?P<album_id>\d+)', single_album, name='single_album'),  # display a single selected album
    url(r'^albums/?', all_albums, name='all_albums'),
    url(r'^library$', library, name='library'),
]
