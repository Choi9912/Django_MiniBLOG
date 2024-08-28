from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from blog.models import SoftDeleteModel, Post
from django.urls import reverse

User = get_user_model()


class Comment(SoftDeleteModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_comment = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

    def delete(self, *args, **kwargs):
        if self.replies.exists():
            super().delete(*args, **kwargs)
            self.content = "이 댓글은 삭제되었습니다."
            self.save(update_fields=["content"])
        else:
            self.hard_delete()

    def hard_delete(self):
        super(SoftDeleteModel, self).delete()

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.post.pk})
