"""Serializers fo rest api."""
from imager_images.models import Photo
from rest_framework import serializers


class PhotosSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Photos."""

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        """Meta."""

        model = Photo
        fields = (
            'user',
            'image',
            'title',
            'description',
            'date_uploaded',
            'date_modified',
            'date_published',
            'published'
        )
