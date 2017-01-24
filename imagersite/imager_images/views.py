"""Views for images."""
from django.shortcuts import render
from imager_images.models import Photo, Album
from django.http import HttpResponse


def photo_view(request, photo_id):
    """Render individual image by id."""
    photo = Photo.objects.get(id=photo_id)
    if photo.published != 'private' or photo.user.username == request.user.username:
        return render(request, 'imager_images/photo.html', {"photo": photo})
    return HttpResponse('Unauthorized', status=401)


def all_photos(request):
    """Render all photos in app."""
    public_photos = []
    photos = Photo.objects.all()
    for photo in photos:
        if photo.published != 'private' or photo.user.username == request.user.username:
            public_photos.append(photo)
    return render(request, 'imager_images/photos.html', {"photos": public_photos})


def single_album(request, album_id):
    """Render a specific album."""
    album = Album.objects.get(id=album_id)
    if album.published != 'private' or album.user.username == request.user.username:
        return render(
            request,
            'imager_images/album.html',
            {'album': album}
        )
    return HttpResponse('Unauthorized', status=401)


def all_albums(request):
    """Render all public albums."""
    public_albums = []
    albums = Album.objects.all()
    for album in albums:
        if album.published != 'private' or album.user.username == request.user.username:
            public_albums.append(album)
    return render(
        request,
        'imager_images/albums.html',
        {'albums': public_albums}
    )
