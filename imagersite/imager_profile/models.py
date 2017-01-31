"""Models for imager_profile."""

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class ActiveProfileManager(models.Manager):
    """Create Model Manager for Active Profiles."""

    def get_queryset(self):
        """Return active users."""
        qs = super(ActiveProfileManager, self).get_queryset()
        return qs.filter(user__is_active__exact=True)


@python_2_unicode_compatible
class ImagerProfile(models.Model):
    """The imager user and all their attributes."""

    objects = models.Manager()
    active = ActiveProfileManager()

    user = models.OneToOneField(
        User,
        related_name="profile",
        on_delete=models.CASCADE
    )
    CAMERA_CHOICES = [
        ('Nikon', 'Nikon'),
        ('iPhone', 'iPhone'),
        ('Canon', 'Canon'),
        ('--------', '--------')
    ]
    TYPE_OF_PHOTOGRAPHY = [
        ('nature', 'nature'),
        ('urban', 'urban'),
        ('portraits', 'portraits')
    ]
    camera_type = models.CharField(
        max_length=10,
        choices=CAMERA_CHOICES,
        blank=True,
        default='--------'
    )
    address = models.CharField(default="", max_length=70, null=True, blank=True)
    bio = models.TextField(default="")
    personal_website = models.URLField(default="")
    for_hire = models.BooleanField(default=False)
    travel_distance = models.IntegerField(default=0, blank=True)
    phone_number = models.CharField(max_length=15, default="", blank=True)
    photography_type = models.CharField(max_length=20, default="", blank=True)

    @property
    def is_active(self):
        """Return True if user associated with this profile is active."""
        return self.user.is_active

    def __str__(self):
        """Display user data as a string."""
        return "User: {}, Camera: {}, Address: {}, Phone number: {}, For Hire? {}, Photography style: {}".format(self.user, self.camera_type, self.address, self.phone_number, self.for_hire, self.photography_type)


@receiver(post_save, sender=User)
def make_profile_for_user(sender, instance, **kwargs):
    """Called when user is made and hooks that user to a profile."""
    if kwargs["created"]:
        new_profile = ImagerProfile(user=instance)
        new_profile.save()
