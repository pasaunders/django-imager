"""Models for imager_profile."""

from django.db import models
from django.contrib.auth.models import User, Group
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
        ('Canon', 'Canon')
    ]
    camera_type = models.CharField(
        max_length=10,
        choices=CAMERA_CHOICES,
        default=""
    )
    address = models.CharField(max_length=70, default="")
    bio = models.TextField(default="")
    personal_website = models.URLField(default="")
    for_hire = models.BooleanField(default=False)
    travel_distance = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=20, default="")
    STYLE_CHOICES = [
        ('Portrait', 'Portrait'),
        ('Landscape', 'Landscape'),
        ('Black and White', 'Black and White'),
        ('Sport', 'Sport')
    ]
    photography_type = models.CharField(
        max_length=20,
        choices=STYLE_CHOICES,
        default=""
    )

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
        # import pdb; pdb.set_trace()
        group = Group.objects.get(name="user")
        instance.groups.add(group)
        new_profile = ImagerProfile(user=instance)
        new_profile.save()
