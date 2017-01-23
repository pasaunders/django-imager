"""Views for images."""
from django.shortcuts import render
from imager_images.models import Photo
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
