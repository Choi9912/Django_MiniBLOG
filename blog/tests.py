from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Post, Category, Tag
from .forms import CustomPostForm
from django.utils import timezone

User = get_user_model()


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.tag = Tag.objects.create(name="Test Tag", slug="test-tag")
        self.post = Post.objects.create(
            title="Test Post",
            content="Test Content",
            author=self.user,
            category=self.category,
        )
        self.post.tags.add(self.tag)

    def test_post_creation(self):
        self.assertEqual(self.post.title, "Test Post")
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.category, self.category)
        self.assertIn(self.tag, self.post.tags.all())

    def test_category_str(self):
        self.assertEqual(str(self.category), "Test Category")

    def test_tag_str(self):
        self.assertEqual(str(self.tag), "Test Tag")

    def test_post_str(self):
        self.assertEqual(str(self.post), "Test Post")


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.tag = Tag.objects.create(name="Test Tag", slug="test-tag")
        self.post = Post.objects.create(
            title="Test Post",
            content="Test Content",
            author=self.user,
            category=self.category,
        )
        self.post.tags.add(self.tag)

    def test_post_list_view(self):
        response = self.client.get(reverse("post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_list.html")
        self.assertContains(response, "Test Post")

    def test_post_detail_view(self):
        response = self.client.get(reverse("post_detail", kwargs={"pk": self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_detail.html")
        self.assertContains(response, "Test Post")

    def test_post_create_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("create_post"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_form.html")

    def test_post_update_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("post_update", kwargs={"pk": self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_form.html")

    def test_post_delete_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(reverse("post_delete", kwargs={"pk": self.post.pk}))
        self.assertRedirects(response, reverse("post_list"))
        self.assertTrue(Post.objects.get(pk=self.post.pk).is_deleted)


class FormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )

    def test_custom_post_form_valid(self):
        form_data = {
            "title": "Test Post",
            "content": "Test Content",
            "category": self.category.id,
            "tags": "#test #tag",
        }
        form = CustomPostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_custom_post_form_invalid(self):
        form_data = {
            "title": "",  # Title is required
            "content": "Test Content",
            "category": self.category.id,
        }
        form = CustomPostForm(data=form_data)
        self.assertFalse(form.is_valid())


class PopularPostsMixinTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.post1 = Post.objects.create(
            title="Popular Post",
            content="Test Content",
            author=self.user,
            category=self.category,
            view_count=100,
        )
        self.post2 = Post.objects.create(
            title="Less Popular Post",
            content="Test Content",
            author=self.user,
            category=self.category,
            view_count=10,
        )

    def test_get_popular_posts(self):
        response = self.client.get(reverse("post_list"))
        self.assertEqual(response.status_code, 200)
        popular_posts = response.context["popular_posts"]
        self.assertEqual(popular_posts[0], self.post1)


class SortPostsMixinTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.post1 = Post.objects.create(
            title="Old Post",
            content="Test Content",
            author=self.user,
            category=self.category,
            created_at=timezone.now() - timezone.timedelta(days=2),
        )
        self.post2 = Post.objects.create(
            title="New Post",
            content="Test Content",
            author=self.user,
            category=self.category,
            created_at=timezone.now(),
        )

    def test_sort_posts_by_latest(self):
        response = self.client.get(reverse("post_list") + "?sort=latest")
        self.assertEqual(response.status_code, 200)
        posts = list(response.context["posts"])
        self.assertEqual(posts[0], self.post2)
        self.assertEqual(posts[1], self.post1)
