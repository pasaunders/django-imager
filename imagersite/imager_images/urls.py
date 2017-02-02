"""Images urls."""
from django.conf.urls import url
from .views import(
    PhotosView,
    AlbumView,
    AlbumsView,
    Library,
    PhotoView,
    AddAlbum,
    AddPhoto,
    EditAlbum,
    EditPhoto,
    TagListView
)
from django.contrib.auth.decorators import login_required

app_name = 'imager_images'
urlpatterns = [
    url(r'^photos/add/$', AddPhoto.as_view(), name='AddPhoto'),
    url(r'^photos/(?P<photo_id>\d+)$', PhotoView.as_view(), name='single_photo'),
    url(r'^photos/(?P<pk>\d+)/edit/$', EditPhoto.as_view(), name='edit_photo'),
    url(r'^photos/$', PhotosView.as_view(), name='photos'),
    url(r'^albums/(?P<album_id>\d+)/$', AlbumView.as_view(), name='AlbumView'),
    url(r'^albums/(?P<pk>\d+)/edit/$', EditAlbum.as_view(), name='edit_album'),
    url(r'^albums/add/$', AddAlbum.as_view(), name='AddAlbum'),
    url(r'^albums/$', AlbumsView.as_view(), name='AlbumsView'),
    url(r'^library/$', login_required(Library.as_view()), name='library'),
    url(r'^tagged/(?P<slug>[-\w]+)/$', TagListView.as_view(), name="tagged_photos")
]
