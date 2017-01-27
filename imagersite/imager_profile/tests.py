"""Tests for the imager_profile app."""
from django.test import TestCase
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

        username = factory.Sequence(lambda n: "Prisoner number {}".format(n))
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

    def test_active_users_counted(self):
        """Test acttive user count meets expectations."""
        self.assertTrue(ImagerProfile.active.count() == User.objects.count())

    def test_inactive_users_not_counted(self):
        """Test inactive users not included with active users."""
        deactivated_user = self.users[0]
        deactivated_user.is_active = False
        deactivated_user.save()
        self.assertTrue(ImagerProfile.active.count() == User.objects.count() - 1)

    def test_imagerprofile_attributes(self):
        """Test that ImagerProfile has the expected attributes."""
        attribute_list = ["user", "camera_type", "address", "bio", "personal_website", "for_hire", "travel_distance", "phone_number", "photography_type"]
        for item in attribute_list:
            self.assertTrue(hasattr(ImagerProfile, item))

    def test_field_type(self):
        """Test user field types."""
        attribute_list = ["camera_type", "address", "bio", "personal_website", "for_hire", "travel_distance", "phone_number", "photography_type"]
        field_list = [str, str, str, str, bool, int, str, str]
        test_user = self.users[0]
        # import pdb; pdb.set_trace()
        self.assertIsInstance(test_user.username, str)
        for attribute, field in zip(attribute_list, field_list):
            self.assertIsInstance(getattr(test_user.profile, attribute), field)
