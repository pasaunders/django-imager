"""Views for restfull api."""
from imager_images.models import Photo
from rest_framework import viewsets
from imager_api.serializers import PhotosSerializer


class PhotoViewSet(viewsets.ReadOnlyModelViewSet):
    """Provides a list of all photos belonging to a user."""

    serializer_class = PhotosSerializer

    def get_queryset(self):
        """Get photos owned by current user."""
        return Photo.objects.filter(user=self.request.user)
