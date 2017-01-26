"""Views for images."""
from django.shortcuts import render
from imager_images.models import Photo, Album
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView


class PhotoView(ListView):
    """Photo View."""

    model = Photo
    template_name = "imager_images/photo.html"

    def get_context_data(self):
        """Return photo."""
        photo = Photo.objects.get(id=self.kwargs['photo_id'])
        if photo.published != 'private' or photo.user.username == self.request.user.username:
            return {"photo": photo}
        return HttpResponse('Unauthorized', status=401)


class PhotosView(ListView):
    """Photos View."""

    model = Photo
    template_name = "imager_images/photos.html"

    def get_context_data(self):
        """Return photos."""
        public_photos = []
        photos = Photo.objects.all()
        for photo in photos:
            if photo.published != 'private' or photo.user.username == request.user.username:
                public_photos.append(photo)
        return {"photos": public_photos}


class AlbumView(ListView):
    """Album View."""

    model = Album
    template_name = "imager_images/album.html"

    def get_context_data(self):
        """Return album."""
        album = Album.objects.get(id=self.kwargs['album_id'])
        if album.published != 'private' or album.user.username == self.request.user.username:
            return {'album': album}
        return HttpResponse('Unauthorized', status=401)


class AlbumsView(ListView):
    """Albums View."""

    model = Album
    template_name = "imager_images/albums.html"

    def get_context_data(self):
        """Return albums."""
        public_albums = []
        albums = Album.objects.all()
        for album in albums:
            if album.published != 'private' or album.user.username == self.request.user.username:
                public_albums.append(album)
        return {'albums': public_albums}


@login_required(login_url='/accounts/login/')
def library(request):
    """Library view."""
    albums = request.user.albums.all()
    photos = request.user.photos.all()
    return render(request,
                  'imager_images/library.html',
                  context={'albums': albums, 'photos': photos})
