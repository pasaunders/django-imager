"""Tests for the imager_profile app."""
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
import factory


class ProfileTestCase(TestCase):
    """The Profile Model test runner."""

    class UserFactory(factory.django.DjangoModelFactory):
        """Makes users."""

        class Meta:
            """Meta."""

            model = User

        username = factory.Sequence(lambda n: "The Chosen {}".format(n))
        email = factory.LazyAttribute(
            lambda x: "{}@foo.com".format(x.username.replace(" ", ""))
        )

    def setUp(self):
        """The appropriate setup for the appropriate test."""
        self.foo = "bar"
        self.users = [self.UserFactory.create() for i in range(20)]

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

    def test_user_model_has_attributes(self):
        """Test user attributes are present."""
        pass

    def test_active_users_counted(self):
        """Test acttive user count meets expectations."""
        self.assertTrue(ImagerProfile.active.count() == User.objects.count())

    def test_inactive_users_not_counted(self):
        """Test inactive users not included with active users."""
        deactivated_user = self.users[0]
        deactivated_user.is_active = False
        deactivated_user.save()
        self.assertTrue(ImagerProfile.active.count() == User.objects.count() - 1)



class frontend_test_cases(TestCase):
    """Test the frontend of the imager_profile site."""
    pass
