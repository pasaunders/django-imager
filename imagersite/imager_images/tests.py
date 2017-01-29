"""Test the imager_images app."""
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.db import models
from imager_images.models import Photo, Album
import factory


class UserFactory(factory.django.DjangoModelFactory):
    """Makes users."""

    class Meta:
        """Meta."""

        model = User

    username = factory.Sequence(lambda n: "Prisoner number {}".format(n))
    email = factory.LazyAttribute(
        lambda x: "{}@foo.com".format(x.username.replace(" ", ""))
    )


class PhotoFactory(factory.django.DjangoModelFactory):
    """Makes photos."""

    class Meta:
        """Meta."""

        model = Photo

    title = factory.Sequence(lambda n: "Photo number {}".format(n))
    description = factory.LazyAttribute(lambda a: '{} is a photo'.format(a.title))


class AlbumFacotory(factory.django.DjangoModelFactory):
    """Makes albums."""

    class Meta:
        """Meta."""

        model = Album

    title = factory.Sequence(lambda n: "Album number {}".format(n))
    description = factory.LazyAttribute(lambda a: '{} is an album'.format(a.title))


class PhotoTestCase(TestCase):
    """Photo model and view tests."""

    def setUp(self):
        """The appropriate setup for the appropriate test."""
        self.users = [UserFactory.create() for i in range(20)]
        self.photos = [PhotoFactory.create() for i in range(20)]

        """
        To test:
        photo model is built
        photos are associated with users
        assigning values to photo attributes
        presence of string method
        """

    def test_photo_made_when_saved(self):
        """Test photos are added to the database."""
        self.assertTrue(Photo.objects.count() == 1)

    def test_photo_associated_with_user(self):
        """Test that a photo is attached to a user."""
        photo = Photo.objects.first()
        self.assertTrue(hasattr(photo, "user"))
        self.assertIsInstance(photo.user, User)

    def test_photo_has_str(self):
        """Test photo model includes string method."""


class AlbumTestCase(TestCase):
    """Album model and view tests."""

    def setUp(self):
        """The appropriate setup for the appropriate test."""
        self.users = [UserFactory.create() for i in range(20)]
        self.photos = [PhotoFactory.create() for i in range(20)]
        self.album = [AlbumFacotory.create() for i in range(20)]

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
