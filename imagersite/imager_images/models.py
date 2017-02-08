"""Album and Photo models."""
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

PUBLISHED_OPTIONS = (
    ("private", "private"),
    ("shared", "shared"),
    ("public", "public"),
)


def image_path(instance, file_name):
    """Upload file to media root in user folder."""
    return 'user_{0}/{1}'.format(instance.user.id, file_name)


@python_2_unicode_compatible
class Photo(models.Model):
    """Create Photo Model."""

    tags = TaggableManager()
    user = models.ForeignKey(
        User,
        related_name='photos',
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to=image_path, blank=True, null=True)
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=120, blank=True, null=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(blank=True, null=True)
    published = models.CharField(max_length=10, choices=PUBLISHED_OPTIONS, default='public')

    def __str__(self):
        """Return string description of photo."""
        return "{}: Photo belonging to {}".format(self.title, self.user)


@python_2_unicode_compatible
class Album(models.Model):
    """Create Album Model."""

    user = models.ForeignKey(
        User,
        related_name="albums",
        on_delete=models.CASCADE,
    )
    cover = models.ForeignKey(
        "Photo",
        null=True,
        related_name="albums_covered"
    )
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=200)
    photos = models.ManyToManyField(
        "Photo",
        related_name="albums",
        symmetrical=False
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(blank=True, null=True)
    published = models.CharField(max_length=10, choices=PUBLISHED_OPTIONS, default='public')

    def __str__(self):
        """Return String Representation of Album."""
        return "{}: Album belonging to {}".format(self.title, self.user)
