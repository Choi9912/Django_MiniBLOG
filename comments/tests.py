from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Comment, Post
from .forms import CommentForm
from .views import (
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    ReplyCreateView,
)

User = get_user_model()


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.post = Post.objects.create(
            title="Test Post", content="Test Content", author=self.user
        )
        self.comment = Comment.objects.create(
            post=self.post, author=self.user, content="Test comment"
        )

    def test_comment_creation(self):
        self.assertTrue(isinstance(self.comment, Comment))
        self.assertEqual(
            self.comment.__str__(),
            f"Comment by {self.user.username} on {self.post.title}",
        )

    def test_comment_soft_delete(self):
        reply = Comment.objects.create(
            post=self.post,
            author=self.user,
            content="Test reply",
            parent_comment=self.comment,
        )
        self.comment.delete()
        updated_comment = Comment.objects.get(pk=self.comment.pk)
        self.assertTrue(updated_comment.is_deleted)
        self.assertEqual(updated_comment.content, "이 댓글은 삭제되었습니다.")

    def test_comment_hard_delete(self):
        self.comment.hard_delete()
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())


class CommentFormTest(TestCase):
    def test_comment_form_valid(self):
        form_data = {"content": "Valid comment"}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_comment_form_invalid(self):
        form_data = {"content": ""}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("댓글 내용을 입력해주세요.", form.errors["content"])


class CommentViewsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.post = Post.objects.create(
            title="Test Post", content="Test Content", author=self.user
        )

    def test_comment_create_view(self):
        data = {"content": "New comment"}
        request = self.factory.post("/fake-url/", data=data)
        request.user = self.user
        response = CommentCreateView.as_view()(request, post_pk=self.post.pk)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(content="New comment").exists())

    def test_comment_update_view(self):
        comment = Comment.objects.create(
            post=self.post, author=self.user, content="Original comment"
        )
        data = {"content": "Updated comment"}
        request = self.factory.post("/fake-url/", data=data)
        request.user = self.user
        response = CommentUpdateView.as_view()(request, pk=comment.pk)
        self.assertEqual(response.status_code, 302)
        comment.refresh_from_db()
        self.assertEqual(comment.content, "Updated comment")

    def test_comment_delete_view(self):
        comment = Comment.objects.create(
            post=self.post, author=self.user, content="Comment to delete"
        )
        request = self.factory.post("/fake-url/")
        request.user = self.user
        response = CommentDeleteView.as_view()(request, pk=comment.pk)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())

    def test_reply_create_view(self):
        parent_comment = Comment.objects.create(
            post=self.post, author=self.user, content="Parent comment"
        )
        data = {"content": "New reply"}
        request = self.factory.post("/fake-url/", data=data)
        request.user = self.user
        response = ReplyCreateView.as_view()(request, comment_pk=parent_comment.pk)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Comment.objects.filter(
                content="New reply", parent_comment=parent_comment
            ).exists()
        )
