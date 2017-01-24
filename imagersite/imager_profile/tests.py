"""Tests for the imager_profile app."""
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
import factory


class UserFactory(factory.django.DjangoModelFactory):
    """Makes users."""

    class Meta:
        """Meta."""

        model = User

    username = factory.Sequence(lambda n: "The Chosen {}".format(n))
    email = factory.LazyAttribute(
        lambda x: "{}@foo.com".format(x.username.replace(" ", ""))
    )


class ProfileTestCase(TestCase):
    """The Profile Model test runner."""

    def setUp(self):
        """The appropriate setup for the appropriate test."""
        self.users = [UserFactory.create() for i in range(20)]

    def test_profile_is_made_when_user_is_saved(self):
        """Test profile is made when user is saved."""
        self.assertTrue(ImagerProfile.objects.count() == 20)

    def test_profile_is_associated_with_actual_users(self):
        """Test profile is associated with actual users."""
        profile = ImagerProfile.objects.first()
        self.assertTrue(hasattr(profile, "user"))
        self.assertIsInstance(profile.user, User)

    def test_user_has_profile_attached(self):
        """Test user has profile attached."""
        user = self.users[0]
        self.assertTrue(hasattr(user, "profile"))
        self.assertIsInstance(user.profile, ImagerProfile)

    def test_user_model_has_str(self):
        """Test user has a string method."""
        user = self.users[0]
        self.assertIsInstance(str(user), str)

    # def test_user_model_has_attributes(self):
    #     """Test user attributes are present."""
    #     pass

    def test_active_users_counted(self):
        """Test acttive user count meets expectations."""
        self.assertTrue(ImagerProfile.active.count() == User.objects.count())

    def test_inactive_users_not_counted(self):
        """Test inactive users not included with active users."""
        deactivated_user = self.users[0]
        deactivated_user.is_active = False
        deactivated_user.save()
        self.assertTrue(ImagerProfile.active.count() == User.objects.count() - 1)


class FrontendTestCases(TestCase):
    """Test the frontend of the imager_profile site."""

    def setUp(self):
        """Set up client and request factory."""
        self.client = Client()
        self.request = RequestFactory()

    def test_home_view_status(self):
        """Test home view has 200 status."""
        from imagersite.views import home_view
        req = self.request.get("/route")
        response = home_view(req)
        self.assertTrue(response.status_code == 200)

    def test_home_route_status(self):
        """Test home route has 200 status."""
        response = self.client.get("/")
        self.assertTrue(response.status_code == 200)

    def test_home_route_templates(self):
        """Test the home route templates are correct."""
        response = self.client.get("/")
        self.assertTemplateUsed(response, "imagersite/base.html")
        self.assertTemplateUsed(response, "imagersite/home.html")

    def test_login_redirect_code(self):
        """Test built-in login route redirects properly."""
        user_register = UserFactory.create()
        user_register.username = "username"
        user_register.password = "potatoes"
        user_register.save()
        response = self.client.post("/login/", {
            "username": user_register.username,
            "password": "potatoes"

        })
        self.assertTrue(response.status_code == 302)

    def test_login_redirect_home(self):
        """Test built-in login route redirects to home."""
        user_register = UserFactory.create()
        user_register.username = "username2"
        user_register.password = "potatoes2"
        user_register.save()
        response = self.client.post("/login/", {
            "username": user_register.username,
            "password": "potatoes"
        }, follow=True)
        self.assertTrue(response.redirect_chain[0][0] == '/')

    def test_register_user(self):
        """Test that tests can register users."""
        self.assertTrue(User.objects.count() == 0)
        self.client.post("/registration/register/", {
            "username": "Sir_Joseph",
            "email": "e@mail.com",
            "password1": "rutabega",
            "password2": "rutabega"
        })
        self.assertTrue(User.objects.count() == 1)

    def test_new_user_inactive(self):
        """Test django-created user starts as inactive."""
        self.client.post("/registration/register/", {
            "username": "Sir_Joseph",
            "email": "e@mail.com",
            "password1": "rutabega",
            "password2": "rutabega"
        })
        inactive_user = User.objects.first()
        self.assertFalse(inactive_user.is_active)

    def test_registration_redirect(self):
        """Test redirect on registration."""
        response = self.client.post("/registration/register/", {
            "username": "Sir_Joseph",
            "email": "e@mail.com",
            "password1": "rutabega",
            "password2": "rutabega"
        })
        self.assertTrue(response.status_code == 302)

    def test_registration_reidrect_home(self):
        """Test registration redirects home."""
        response = self.client.post("/registration/register/", {
            "username": "Sir_Joseph",
            "email": "e@mail.com",
            "password1": "rutabega",
            "password2": "rutabega"
        }, follow=True)
        self.assertTrue(
            response.redirect_chain[0][0] == "/registration/register/complete/"
        )
