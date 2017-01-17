from django.db import models
from django.contrib.auth.models import User
import uuid

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class ImagerProfile(models.Model):
    """The imager user and all their attributes."""

    user = models.OneToOneField(
        User,
        related_name="profile",
        on_delete=models.CASCADE
    )
    CAMERA_CHOICES = ('Nikon', 'iPhone', 'Canon'),
    ACTIVE = False
    camera_type = models.CharField(max_length=10, choices=CAMERA_CHOICES, null=True, blank=True),
    address = models.CharField(max_length=40, null=True, blank=True),
    bio = models.TextField(),
    personal_website = models.URLField(),
    for_hire = models.BooleanField(default=False),
    travel_distance = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    photography_type = models.CharField(max_length=20, null=True, blank=True)
