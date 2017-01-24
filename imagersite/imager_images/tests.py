from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from imager_images.models import Photo, Album
import factory

# Create your tests here.


class UserFactory(factory.django.DjangoModelFactory):
    """Makes users."""

    class Meta:
        """Meta."""

        model = User

    username = factory.Sequence(lambda n: "The Chosen {}".format(n))
    email = factory.LazyAttribute(
        lambda x: "{}@foo.com".format(x.username.replace(" ", ""))
    )


class PhotoTestCase(TestCase):
    """Photo model and view tests."""

    def setUp(self):
        """Set up users for photo tests."""
        self.users = [UserFactory.create() for i in range(20)]
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
        """Set up users for photo tests."""
        self.users = [UserFactory.create() for i in range(20)]

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
        """Set up users for front end tests."""
        self.users = [UserFactory.create() for i in range(20)]

    """
    To test:
        Views return 200
        Routes return 200
        all four templates are used
        albums are visible in albums.html
        correct number of photos and albums are visible
    """