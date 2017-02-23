"""Views for restfull api."""
from imager_images.models import Photo
from rest_framework import viewsets, permissions
from imager_api.serializers import PhotosSerializer
from imager_api.permissions import Owner


class PhotoViewSet(viewsets.ReadOnlyModelViewSet):
    """Provides a list of all photos belonging to a user."""

    serializer_class = PhotosSerializer
    permission_classes = (permissions.IsAuthenticated, Owner)

    def get_queryset(self):
        """Get photos owned by current user."""
        return Photo.objects.filter(user=self.request.user)
