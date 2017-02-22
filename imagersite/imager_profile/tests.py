"""Tests for the imager_profile app."""
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User, Group, Permission
from imager_profile.models import ImagerProfile
import factory
from faker import Faker
from django.core.urlresolvers import reverse_lazy


def add_user_group():
    """Add user group with permissions to testing database."""
    new_group, created = Group.objects.get_or_create(name='user')
    permission1 = Permission.objects.get(name='Can add album')
    permission2 = Permission.objects.get(name='Can change album')
    permission3 = Permission.objects.get(name='Can delete album')
    permission4 = Permission.objects.get(name='Can add photo')
    permission5 = Permission.objects.get(name='Can change photo')
    permission6 = Permission.objects.get(name='Can delete photo')
    new_group.permissions.add(
        permission1, permission2, permission3,
        permission4, permission5, permission6
    )
    new_group.save()


class UserFactory(factory.django.DjangoModelFactory):
    """Makes users."""

    class Meta:
        """Meta."""

        model = User

    username = factory.Sequence(lambda n: "Prisoner_number_{}".format(n))
    email = factory.LazyAttribute(
        lambda x: "{}@foo.com".format(x.username.replace(" ", ""))
    )


class ProfileTestCase(TestCase):
    """The Profile Model test runner."""

    def setUp(self):
        """The appropriate setup for the appropriate test."""
        add_user_group()
        self.users = [UserFactory.create() for i in range(20)]
        for profile in ImagerProfile.objects.all():
            self.fake_profile_attrs(profile)

    def fake_profile_attrs(self, profile):
        """Build a fake user."""
        fake = Faker()
        profile.address = fake.street_name()
        profile.bio = fake.paragraph()
        profile.personal_website = fake.url()
        profile.for_hire = fake.boolean()
        profile.travel_distance = fake.random_int()
        profile.phone_number = fake.phone_number()
        profile.photography_type = 'Nikon'
        profile.save()

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
        user = User.objects.get(pk=self.users[0].id)
        self.assertTrue(user.profile.bio)

    def test_active_users_counted(self):
        """Test acttive user count meets expectations."""
        self.assertTrue(ImagerProfile.active.count() == User.objects.count())

    def test_inactive_users_not_counted(self):
        """Test inactive users not included with active users."""
        deactivated_user = self.users[0]
        deactivated_user.is_active = False
        deactivated_user.save()
        self.assertTrue(ImagerProfile.active.count() == User.objects.count() - 1)

    def test_user_in_group(self):
        """Test that on creation of user add them to user group."""
        user = self.users[5]
        group = user.groups.all()[0]
        self.assertTrue(group.name == 'user')


class FrontendTestCases(TestCase):
    """Test the frontend of the imager_profile site."""

    def setUp(self):
        """Set up client and request factory."""
        self.client = Client()
        self.request = RequestFactory()

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
        add_user_group()
        user_register = UserFactory.create()
        user_register.is_active = True
        user_register.username = "username"
        user_register.set_password("potatoes")
        user_register.save()
        response = self.client.post("/login/", {
            "username": user_register.username,
            "password": "potatoes"

        })
        self.assertRedirects(response, '/profile/')

    def test_register_user(self):
        """Test that tests can register users."""
        add_user_group()
        self.assertTrue(User.objects.count() == 0)
        self.client.post("/accounts/register/", {
            "username": "Sir_Joseph",
            "email": "e@mail.com",
            "password1": "rutabega",
            "password2": "rutabega"
        })
        self.assertTrue(User.objects.count() == 1)

    def test_new_user_inactive(self):
        """Test django-created user starts as inactive."""
        add_user_group()
        self.client.post("/accounts/register/", {
            "username": "Sir_Joseph",
            "email": "e@mail.com",
            "password1": "rutabega",
            "password2": "rutabega"
        })
        inactive_user = User.objects.first()
        self.assertFalse(inactive_user.is_active)

    def test_registration_redirect(self):
        """Test redirect on registration."""
        add_user_group()
        response = self.client.post("/accounts/register/", {
            "username": "Sir_Joseph",
            "email": "e@mail.com",
            "password1": "rutabega",
            "password2": "rutabega"
        })
        self.assertTrue(response.status_code == 302)

    def test_registration_reidrect_home(self):
        """Test registration redirects home."""
        add_user_group()
        response = self.client.post("/accounts/register/", {
            "username": "Sir_Joseph",
            "email": "e@mail.com",
            "password1": "rutabega",
            "password2": "rutabega"
        }, follow=True)
        self.assertRedirects(
            response,
            "/accounts/register/complete/"
        )

    def test_profile_renders(self):
        """Test public profile route response is 200."""
        add_user_group()
        user = UserFactory.create()
        response = self.client.get(reverse_lazy('public_profile', kwargs={'username': user.username}))
        self.assertTrue(response.status_code == 200)

    def test_logged_in_user_profile(self):
        """Test the logged in user goes to private profile."""
        add_user_group()
        user = UserFactory.create()
        self.client.force_login(user)
        response = self.client.get(reverse_lazy('private_profile'))
        self.assertTrue(response.status_code == 200)

    def test_edit_profile_status(self):
        """Test edit profile has 200 status."""
        add_user_group()
        user = UserFactory.create()
        self.client.force_login(user)
        response = self.client.get(reverse_lazy('edit-profile'))
        self.assertTrue(response.status_code == 200)

    def test_edit_profile_correct_template(self):
        """Test edit profile correct template."""
        add_user_group()
        user = UserFactory.create()
        self.client.force_login(user)
        response = self.client.get(reverse_lazy('edit-profile'))
        self.assertTemplateUsed(response, "imagersite/base.html")
        self.assertTemplateUsed(response, "imager_profile/edit_profile.html")

    def test_correct_html_in_template(self):
        """Test correct html in template."""
        add_user_group()
        user = UserFactory.create()
        self.client.force_login(user)
        response = self.client.get(reverse_lazy('edit-profile'))
        self.assertTrue('input' in str(response.content))
        self.assertTrue('Address' in str(response.content))
        self.assertTrue('Camera type' in str(response.content))
        self.assertTrue('Phone number' in str(response.content))

    def test_not_logged_in_redirects_to_login_page(self):
        """Test not logged in redirects to login page."""
        response = self.client.get(reverse_lazy('edit-profile'))
        self.assertRedirects(response, '/login/?next=/profile/edit')
