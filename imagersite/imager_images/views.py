"""Views for images."""
from imager_images.models import Photo, Album
from django.http import HttpResponse  # reimplement if we get around to fixing the views, otherwise use below.
from django.http import Http404
from django.views.generic import ListView, TemplateView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
import random


class PhotoView(ListView):
    """Photo View."""

    model = Photo
    template_name = "imager_images/photo.html"

    def get_context_data(self):
        """Return photo."""
        photo = Photo.objects.get(id=self.kwargs['photo_id'])
        tag_match = []
        for tag in photo.tags.all():
            check_photo = Photo.objects.filter(tags__slug=tag).all()
            if check_photo:
                next_photo = random.choice(check_photo)
                if next_photo not in tag_match:
                    tag_match.append(next_photo)
                if len(tag_match) >= 5:
                    break
        if photo.published != 'private' or photo.user.username == self.request.user.username:
            return {"photo": photo, "tag_match": tag_match}
        else:
            raise Http404('Unauthorized')
        return {}


class PhotosView(TemplateView):
    """Photos View."""

    template_name = "imager_images/photos.html"

    def get_context_data(self):
        """Return photos."""
        public_photos = []
        photos = Photo.objects.all()
        for photo in photos:
            if photo.published != 'private' or photo.user.username == self.request.user.username:
                public_photos.append(photo)
        return {"photos": public_photos}


class TagListView(ListView):
    """The listing for tagged photos."""

    template_name = "imager_images/list.html"

    def get_queryset(self):
        """Return all photos with __ tag name."""
        return Photo.objects.filter(tags__slug=self.kwargs.get("slug")).all()

    def get_context_data(self, **kwargs):
        """Make tag in context and sets it to self.kwargs.get("slug")."""
        context = super(TagListView, self).get_context_data(**kwargs)
        context["tag"] = self.kwargs.get("slug")
        return context


class AlbumView(ListView):
    """Album View."""

    model = Album
    template_name = "imager_images/album.html"

    def get_context_data(self):
        """Return album."""
        album = Album.objects.get(id=self.kwargs['album_id'])
        if album.published != 'private' or album.user.username == self.request.user.username:
            return {'album': album}
        else:
            raise Http404('Unauthorized')
        return {}


class AlbumsView(TemplateView):
    """Albums View."""

    template_name = "imager_images/albums.html"

    def get_context_data(self):
        """Return albums."""
        public_albums = []
        albums = Album.objects.all()
        for album in albums:
            if album.published != 'private' or album.user.username == self.request.user.username:
                public_albums.append(album)
        return {'albums': public_albums}


class Library(LoginRequiredMixin, TemplateView):
    """Library View."""

    login_url = reverse_lazy('login')

    template_name = "imager_images/library.html"

    def get_context_data(self):
        """Return albums."""
        albums = self.request.user.albums.all()
        photos = self.request.user.photos.all()
        return {'albums': albums, 'photos': photos}


class AddAlbum(PermissionRequiredMixin, CreateView):
    """Add Album."""

    permission_required = "imager_images.add_album"

    template_name = "imager_images/add_album.html"
    model = Album
    fields = ['title', "cover", "description", "photos", "published", "date_published"]
    success_url = reverse_lazy('imager_images:library')

    def form_valid(self, form):
        """Make the form user instance the current user."""
        form.instance.user = self.request.user
        return super(AddAlbum, self).form_valid(form)


class EditAlbum(PermissionRequiredMixin, UpdateView):
    """Add Album."""

    permission_required = "imager_images.change_album"

    template_name = "imager_images/add_album.html"
    model = Album
    fields = ['title', "cover", "description", "photos", "published", "date_published"]
    success_url = reverse_lazy('imager_images:library')


class AddPhoto(PermissionRequiredMixin, CreateView):
    """Add a photo."""

    login_url = reverse_lazy('login')
    permission_required = "imager_images.add_photo"

    template_name = "imager_images/add_photo.html"
    model = Photo
    fields = ['image', 'title', 'description', 'date_published', 'published', 'tags']
    success_url = reverse_lazy('imager_images:library')

    def form_valid(self, form):
        """Make the form user instance the current user."""
        form.instance.user = self.request.user
        return super(AddPhoto, self).form_valid(form)


class EditPhoto(PermissionRequiredMixin, UpdateView):
    """Add a photo."""

    permission_required = "imager_images.change_photo"

    template_name = "imager_images/add_photo.html"
    model = Photo
    fields = ['image', 'title', 'description', 'date_published', 'published', 'tags']
    # success_url = '/images/library'
    success_url = reverse_lazy('imager_images:library')
