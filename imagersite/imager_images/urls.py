"""Images urls."""
from django.conf.urls import url
from .views import PhotosView, AlbumView, AlbumsView, library, PhotoView

urlpatterns = [
    url(r'^photos/(?P<photo_id>\d+)', PhotoView.as_view(), name='public_profile'),
    url(r'^photos/$', PhotosView.as_view(), name='private_profile'),  # display all of the public photos that have been uploaded
    url(r'^albums/(?P<album_id>\d+)', AlbumView.as_view(), name='AlbumView'),  # display a single selected album
    url(r'^albums/?', AlbumsView.as_view(), name='AlbumsView'),
    url(r'^library$', library, name='library'),
]
