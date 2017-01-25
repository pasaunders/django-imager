"""Test the imager_images app."""
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.db import models
from imager_images.models import Photo, Album
import factory
from faker import Faker


class UserFactory(factory.django.DjangoModelFactory):
    """Makes users."""

    class Meta:
        """Meta."""

        model = User

    username = factory.Sequence(lambda n: "Prisoner number {}".format(n))
    email = factory.LazyAttribute(
        lambda x: "{}@foo.com".format(x.username.replace(" ", ""))
    )


class PhotoTestCase(TestCase):
    """Photo model and view tests."""

    def setUp(self):
        """The appropriate setup for the appropriate test."""
        self.users = [UserFactory.create() for i in range(20)]
        for profile in Photo.objects.all():
            self.fake_photo_attrs(profile)

    def fake_photo_attrs(self, profile):
        """Build a fake photo."""
        fake = Faker()
        profile.image =  # Work this one out
        profile.title = fake.name()
        profile.description = fake.paragraph()
        profile.date_uploaded = models.DateTimeField(auto_now_add=True)
        profile.date_modified = models.DateTimeField(auto_now=True)
        profile.date_published = fake.date()
        profile.published = fake.boolean()
        profile.save()

        """
        To test:
        photo model is built
        photos are associated with users
        assigning values to photo attributes
        presence of string method
        """


class AlbumTestCase(TestCase):
    """Album model and view tests."""

    def setUp(self):
        """The appropriate setup for the appropriate test."""
        self.users = [UserFactory.create() for i in range(20)]
        for profile in Album.objects.all():
            self.fake_album_attrs(profile)

    def fake_profile_attrs(self, profile):
        """Build a fake album."""
        fake = Faker()
        profile.cover =
        profile.title =
        profile.description =
        profile.photos =
        profile.date_created = models.DateTimeField(auto_now_add=True)
        profile.date_modified = models.DateTimeField(auto_now=True)
        profile.date_published = fake.date()
        profile.published = fake.boolean()
        profile.save()

    """
    To test:
        album model is built
        albums are associated with users
        assigning values to album attributes
        presence of string method
        photo creation and modified date/times are now
    """


class FrontEndTestCase(TestCase):
    """Front end tests."""

    def setUp(self):
        """Set up client and requestfactory."""
        self.client = Client()
        self.request = RequestFactory()

    """
    To test:
        Views return 200
        Routes return 200
        all four templates are used
        albums are visible in albums.html
        correct number of photos and albums are visible
    """
