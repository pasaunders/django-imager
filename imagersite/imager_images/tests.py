"""Test the imager_images app."""
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
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

    user = factory.SubFactory(UserFactory)
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
        self.assertTrue(Photo.objects.count() == 20)

    def test_photo_associated_with_user(self):
        """Test that a photo is attached to a user."""
        photo = Photo.objects.first()
        self.assertTrue(hasattr(photo, "__str__"))

    def test_photo_has_str(self):
        """Test photo model includes string method."""
        photo = Photo.objects.first()
        self.assertTrue(hasattr(photo, "user"))

    def test_image_title(self):
        """Test that the image has a title."""
        self.assertTrue("Photo" in Photo.objects.first().title)

    def test_image_has_description(self):
        """Test that the Photo description field can be assigned."""
        image = Photo.objects.first()
        description = "This is a test of description field."
        image.description = description
        image.save()
        self.assertTrue(Photo.objects.first().description == description)

    def test_image_has_published(self):
        """Test the image published field."""
        image = Photo.objects.first()
        image.published = 'public'
        image.save()
        self.assertTrue(Photo.objects.first().published == "public")

    def test_user_has_image(self):
        """Test that the user has the image."""
        image = Photo.objects.first()
        user = User.objects.first()
        self.assertTrue(user.photos.count() == 0)
        image.user = user
        image.save()
        self.assertTrue(user.photos.count() == 1)

    def test_two_images_have_user(self):
        """Test two images have the same user."""
        image1 = Photo.objects.all()[0]
        image2 = Photo.objects.all()[1]
        user = User.objects.first()
        image1.user = user
        image2.user = user
        image1.save()
        image2.save()
        self.assertTrue(image1.user == user)
        self.assertTrue(image2.user == user)

    def test_user_has_two_images(self):
        """Test that user has two image."""
        image1 = Photo.objects.all()[0]
        image2 = Photo.objects.all()[1]
        user = User.objects.first()
        image1.user = user
        image2.user = user
        image1.save()
        image2.save()
        self.assertTrue(user.photos.count() == 2)

    def test_user_has_photo_uploaded(self):
        """Test user has photo uploaded."""
        photo = self.photos[4]
        self.assertTrue(photo.image.name is None)
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=open('imager_images/test_img.jpg', 'rb').read(),
            content_type='image/jpeg'
        )
        photo.image = image
        self.assertTrue(photo.image.name is not None)


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
