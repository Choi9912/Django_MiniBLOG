from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import ProfileForm
from .models import Profile, Follower

User = get_user_model()


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.profile = Profile.objects.create(user=self.user, bio="Test bio")

    def test_profile_creation(self):
        self.assertTrue(isinstance(self.profile, Profile))
        self.assertEqual(self.profile.__str__(), self.user.username)


class ProfileFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.profile = Profile.objects.create(user=self.user)

    def test_valid_form(self):
        form = ProfileForm(
            instance=self.profile,
            data={"username": "newusername", "bio": "New bio", "location": "Test City"},
        )
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = ProfileForm(instance=self.profile, data={})
        self.assertFalse(form.is_valid())

    def test_duplicate_username(self):
        User.objects.create_user(username="existinguser", password="12345")
        form = ProfileForm(
            instance=self.profile,
            data={
                "username": "existinguser",
                "bio": "New bio",
            },
        )
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)


class ProfileViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.profile = Profile.objects.create(user=self.user)

    def test_profile_detail_view(self):
        url = reverse("accounts:profile_view", args=[self.user.username])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/profile.html")

    def test_profile_update_view(self):
        self.client.login(username="testuser", password="12345")
        url = reverse("accounts:profile_update")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/profile_update.html")

        response = self.client.post(
            url,
            {
                "username": "updateduser",
                "bio": "Updated bio",
                "location": "Updated City",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.user.username, "updateduser")
        self.assertEqual(self.profile.bio, "Updated bio")


class FollowToggleViewTest(TestCase):
    def setUp(self):
        # Setup initialization like user creation
        self.user1 = User.objects.create_user(username='user1', password='12345')
        self.user2 = User.objects.create_user(username='user2', password='12345')

    def test_follow_self(self):
        self.client.login(username="user1", password="12345")
        url = reverse("accounts:follow_toggle", args=[self.user1.username])

        # First request: Self-follow
        response = self.client.post(url)
        print('First request (self-follow) response content:', response.content)  # Debugging output
        self.assertEqual(response.status_code, 200,
                         msg=f"Unexpected status code: {response.status_code}, content: {response.content.decode()}")

        data = response.json()
        self.assertIn("is_following", data)
        self.assertIn("follower_count", data)

        self.assertTrue(data["is_following"])
        self.assertEqual(data["follower_count"], 1)
        self.assertTrue(
            Follower.objects.filter(user=self.user1, follower=self.user1).exists()
        )

        # Second request: Self-unfollow
        response = self.client.post(url)
        print('Second request (self-unfollow) response content:', response.content)  # Debugging output
        self.assertEqual(response.status_code, 200,
                         msg=f"Unexpected status code: {response.status_code}, content: {response.content.decode()}")

        data = response.json()
        self.assertFalse(data["is_following"])
        self.assertEqual(data["follower_count"], 0)
        self.assertFalse(
            Follower.objects.filter(user=self.user1, follower=self.user1).exists()
        )

    def test_follow_other_user(self):
        self.client.login(username="user1", password="12345")
        url = reverse("accounts:follow_toggle", args=[self.user2.username])

        # First request: Follow user2
        response = self.client.post(url)
        print('First request (follow user2) response content:', response.content)  # Debugging output
        self.assertEqual(response.status_code, 200,
                         msg=f"Unexpected status code: {response.status_code}, content: {response.content.decode()}")

        data = response.json()
        self.assertIn("is_following", data)
        self.assertIn("follower_count", data)

        self.assertTrue(data["is_following"])
        self.assertEqual(data["follower_count"], 1)
        self.assertTrue(
            Follower.objects.filter(user=self.user2, follower=self.user1).exists()
        )

        # Second request: Unfollow user2
        response = self.client.post(url)
        print('Second request (unfollow user2) response content:', response.content)  # Debugging output
        self.assertEqual(response.status_code, 200,
                         msg=f"Unexpected status code: {response.status_code}, content: {response.content.decode()}")

        data = response.json()
        self.assertFalse(data["is_following"])
        self.assertEqual(data["follower_count"], 0)
        self.assertFalse(
            Follower.objects.filter(user=self.user2, follower=self.user1).exists()
        )