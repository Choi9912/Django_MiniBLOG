from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Profile, Follower
from .forms import ProfileForm

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
        self.user1 = User.objects.create_user(username="user1", password="12345")
        self.user2 = User.objects.create_user(username="user2", password="12345")
        Profile.objects.create(user=self.user1)
        Profile.objects.create(user=self.user2)

    def test_follow_toggle(self):
        self.client.login(username="user1", password="12345")
        url = reverse("accounts:follow_toggle", args=[self.user2.username])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Follower.objects.filter(user=self.user2, follower=self.user1).exists()
        )

        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Follower.objects.filter(user=self.user2, follower=self.user1).exists()
        )

    def test_follow_self(self):
        self.client.login(username="user1", password="12345")
        url = reverse("accounts:follow_toggle", args=[self.user1.username])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("is_following", data)
        self.assertIn("follower_count", data)

        # 첫 번째 요청: 자기 자신을 팔로우
        self.assertTrue(data["is_following"])
        self.assertEqual(data["follower_count"], 1)
        self.assertTrue(
            Follower.objects.filter(user=self.user1, follower=self.user1).exists()
        )

        # 두 번째 요청: 자기 자신을 언팔로우
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["is_following"])
        self.assertEqual(data["follower_count"], 0)
        self.assertFalse(
            Follower.objects.filter(user=self.user1, follower=self.user1).exists()
        )
