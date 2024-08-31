from django.shortcuts import get_object_or_404
from django.urls import reverse

from .models import Post, Comment


class CommentService:
    @staticmethod
    def create_comment(form, user, post_pk):
        form.instance.author = user
        form.instance.post = get_object_or_404(Post, pk=post_pk)
        return form.save()

    @staticmethod
    def update_comment(comment, content):
        comment.content = content
        comment.save()
        return comment

    @staticmethod
    def delete_comment(comment):
        post_pk = comment.post.pk
        comment.delete()
        return reverse("post_detail", kwargs={"pk": post_pk})

    @staticmethod
    def create_reply(form, user, parent_comment_pk):
        parent_comment = get_object_or_404(Comment, pk=parent_comment_pk)
        form.instance.author = user
        form.instance.post = parent_comment.post
        form.instance.parent_comment = parent_comment
        form.instance.depth = parent_comment.depth + 1
        return form.save()

    @staticmethod
    def get_comment_context(comment):
        return {"parent_comment": comment.parent_comment, "post": comment.post}
