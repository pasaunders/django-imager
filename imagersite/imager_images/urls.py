"""Images urls."""
from django.conf.urls import url
from .views import PhotosView, AlbumView, AlbumsView, Library, PhotoView, AddAlbum, AddPhoto
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^photos/add/$', AddPhoto.as_view(), name='AddPhoto'),
    url(r'^photos/(?P<photo_id>\d+)', PhotoView.as_view(), name='public_profile'),
    url(r'^photos/$', PhotosView.as_view(), name='private_profile'),
    url(r'^albums/(?P<album_id>\d+)', AlbumView.as_view(), name='AlbumView'),
    url(r'^albums/add/$', AddAlbum.as_view(), name='AddAlbum'),
    url(r'^albums/$', AlbumsView.as_view(), name='AlbumsView'),
    url(r'^library/$', login_required(Library.as_view()), name='library'),
]
