"""Test the imager_images app."""
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from imager_images.models import Photo, Album
import factory
from django.core.urlresolvers import reverse_lazy
from .views import photo_view, all_photos, single_album, all_albums, library


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

    user = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: "Album number {}".format(n))
    description = factory.LazyAttribute(lambda a: '{} is an album'.format(a.title))


class PhotoTestCase(TestCase):
    """Photo model and view tests."""

    def setUp(self):
        """The appropriate setup for the appropriate test."""
        self.users = [UserFactory.create() for i in range(20)]
        self.photos = [PhotoFactory.create() for i in range(20)]

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
        self.albums = [AlbumFacotory.create() for i in range(20)]

    def test_image_has_no_album(self):
        """Test that the image is in an album."""
        image = Photo.objects.first()
        self.assertTrue(image.albums.count() == 0)

    def test_image_has_album(self):
        """Test that the image is in an album."""
        image = Photo.objects.first()
        album = Album.objects.first()
        image.albums.add(album)
        self.assertTrue(image.albums.count() == 1)

    def test_album_has_no_image(self):
        """Test that an album has no image before assignemnt."""
        album = Album.objects.first()
        self.assertTrue(album.photos.count() == 0)

    def test_album_has_image(self):
        """Test that an album has an image after assignemnt."""
        image = Photo.objects.first()
        album = Album.objects.first()
        image.albums.add(album)
        self.assertTrue(image.albums.count() == 1)

    def test_two_images_have_album(self):
        """Test that two images have same album."""
        image1 = Photo.objects.all()[0]
        image2 = Photo.objects.all()[1]
        album = Album.objects.first()
        image1.albums.add(album)
        image2.albums.add(album)
        image1.save()
        image2.save()
        self.assertTrue(image1.albums.all()[0] == album)
        self.assertTrue(image2.albums.all()[0] == album)

    def test_album_has_two_images(self):
        """Test that an album has two images."""
        image1 = Photo.objects.all()[0]
        image2 = Photo.objects.all()[1]
        album = Album.objects.first()
        image1.albums.add(album)
        image2.albums.add(album)
        image1.save()
        image2.save()
        self.assertTrue(album.photos.count() == 2)

    def test_image_has_two_albums(self):
        """Test that an image has two albums."""
        image = Photo.objects.first()
        album1 = Album.objects.all()[0]
        album2 = Album.objects.all()[1]
        image.albums.add(album1)
        image.albums.add(album2)
        image.save()
        self.assertTrue(image.albums.count() == 2)

    def test_album_title(self):
        """Test that the album has a title."""
        self.assertTrue("Album" in Album.objects.first().title)

    def test_album_has_description(self):
        """Test that the album description field exists."""
        self.assertTrue("is an album" in Album.objects.first().description)

    def test_album_has_published(self):
        """Test that the album published field exists."""
        album = Album.objects.first()
        album.published = 'public'
        album.save()
        self.assertTrue(Album.objects.first().published == "public")

    def test_album_has_user(self):
        """Test that album has an user."""
        self.assertTrue(Album.objects.first().user)

    def test_user_has_album(self):
        """Test that the user has the album."""
        album = Album.objects.first()
        user = User.objects.first()
        self.assertTrue(user.albums.count() == 0)
        album.user = user
        album.save()
        self.assertTrue(user.albums.count() == 1)

    def test_two_albums_have_user(self):
        """Test two albums have the same user."""
        album1 = Album.objects.all()[0]
        album2 = Album.objects.all()[1]
        user = User.objects.first()
        album1.user = user
        album2.user = user
        album1.save()
        album2.save()
        self.assertTrue(album1.user == user)
        self.assertTrue(album2.user == user)

    def test_user_has_two_albums(self):
        """Test that user has two albums."""
        album1 = Album.objects.all()[0]
        album2 = Album.objects.all()[1]
        user = User.objects.first()
        album1.user = user
        album2.user = user
        album1.save()
        album2.save()
        self.assertTrue(user.albums.count() == 2)

    def test_adding_cover_image(self):
        """Test that the image is in an album."""
        image = Photo.objects.first()
        album = Album.objects.first()
        self.assertTrue(album.cover is None)
        album.cover = image
        album.save()
        self.assertTrue(Album.objects.first().cover is not None)


class FrontEndTestCase(TestCase):
    """Front end tests."""

    def setUp(self):
        """Set up client and requestfactory."""
        self.client = Client()
        self.request = RequestFactory()
        self.users = [UserFactory.create() for i in range(20)]
        self.photos = [PhotoFactory.create() for i in range(20)]
        self.albums = [AlbumFacotory.create() for i in range(20)]

    """
    To test:
        Views return 200
        Routes return 200
        all four templates are used
        albums are visible in albums.html
        correct number of photos and albums are visible
    """
    def test_libary_view_returns_200(self):
        """Test Library View returns a 200."""
        user = UserFactory.create()
        user.save()
        view = library
        req = self.request.get(reverse_lazy('library'))
        req.user = user
        response = view(req)
        self.assertTrue(response.status_code == 200)

    def test_logged_in_user_has_library(self):
        """A logged in user gets a 200 resposne."""
        user = UserFactory.create()
        user.save()
        self.client.force_login(user)
        response = self.client.get(reverse_lazy("library"))
        self.assertTrue(response.status_code == 200)

    def test_logged_in_user_sees_their_albums(self):
        """Test that a logged in user can see their images in library."""
        user = UserFactory.create()
        album1 = Album.objects.first()
        user.albums.add(album1)
        user.save()
        self.client.force_login(user)
        response = self.client.get(reverse_lazy("library"))
        self.assertTrue(album1.title in str(response.content))

    def test_album_view_returns_200(self):
        """Test that the album view returns a 200."""
        req = self.request.get(reverse_lazy('all_albums'))
        response = all_albums(req)
        self.assertTrue(response.status_code == 200)

    def test_photoid_view_returns_200(self):
        """Test that the photo id view returns a 200."""
        photo = self.photos[6]
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=open('imager_images/test_img.jpg', 'rb').read(),
            content_type='image/jpeg'
        )
        photo.image = image
        photo.save()
        response = self.client.get(reverse_lazy('single_photo',
                                                kwargs={'photo_id': photo.id}))
        self.assertTrue(response.status_code == 200)

    def test_photoid_view_returns_error_private_photo(self):
        """Test that a user cannot view a private photo of another user."""
        photo = self.photos[12]
        photo.published = 'private'
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=open('imager_images/test_img.jpg', 'rb').read(),
            content_type='image/jpeg'
        )
        photo.image = image
        photo.save()
        response = self.client.get(reverse_lazy('single_photo',
                                                kwargs={'photo_id': photo.id}))
        self.assertTrue(response.status_code == 401)

    def test_photo_id_user_views_own_private_photo(self):
        """Test that a user can view their own private photo."""
        user = self.users[2]
        user.save()
        self.client.force_login(user)
        photo = self.photos[15]
        photo.published = 'private'
        photo.user = user
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=open('imager_images/test_img.jpg', 'rb').read(),
            content_type='image/jpeg'
        )
        photo.image = image
        photo.save()
        response = self.client.get(reverse_lazy('single_photo',
                                                kwargs={'photo_id': photo.id}))
        self.assertTrue(response.status_code == 200)

    def test_albumid_view_returns_200(self):
        """Test that the album id view returns a 200."""
        user = self.users[0]
        self.client.force_login(user)
        album = self.albums[9]
        album.user = user
        album.save()
        response = self.client.get(reverse_lazy('single_album',
                                                kwargs={'album_id': album.id}))
        self.assertTrue(response.status_code == 200)

    def test_album_id_view_doesnt_return_private_album(self):
        """Test that a user cannot view a private album."""
        album = self.albums[9]
        album.published = 'private'
        album.save()
        response = self.client.get(reverse_lazy('single_album',
                                                kwargs={'album_id': album.id}))
        self.assertTrue(response.status_code == 401)

    def test_description_of_album_shows(self):
        """Test that the description of an album shows."""
        album = self.albums[17]
        response = self.client.get(reverse_lazy('single_album',
                                                kwargs={'album_id': album.id}))
        self.assertTrue('is an album' in response.content.decode())

    def test_description_of_photo_shows(self):
        """Test that the description of an photo shows."""
        photo = self.photos[17]
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=open('imager_images/test_img.jpg', 'rb').read(),
            content_type='image/jpeg'
        )
        photo.image = image
        photo.save()
        response = self.client.get(reverse_lazy('single_photo',
                                                kwargs={'photo_id': photo.id}))
        self.assertTrue('is a photo' in response.content.decode())

    def test_title_of_photo_shows(self):
        """Test that the title of an photo shows."""
        photo = self.photos[17]
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=open('imager_images/test_img.jpg', 'rb').read(),
            content_type='image/jpeg'
        )
        photo.image = image
        photo.save()
        response = self.client.get(reverse_lazy('single_photo',
                                                kwargs={'photo_id': photo.id}))
        self.assertTrue('Photo number' in response.content.decode())
