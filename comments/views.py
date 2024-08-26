from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect

from comments.forms import CommentForm

from .models import Post, Comment


class BaseCommentView:
    model = Comment


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "comments/comment_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.get_post()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.post.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = self.get_post()
        return context

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs["post_pk"])


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ["content"]
    template_name = "comments/comment_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = self.object.post
        return context


class CommentDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, BaseCommentView, DeleteView
):
    template_name = "comments/comment_confirm_delete.html"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.post.pk})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        if self.object.replies.exists():
            self.object.content = "이 댓글은 삭제되었습니다."
            self.object.is_removed = True
            self.object.save()
        else:
            self.object.delete()
        return redirect(success_url)


class ReplyCreateView(LoginRequiredMixin, BaseCommentView, CreateView):
    fields = ["content"]
    template_name = "comments/reply_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.parent_comment = get_object_or_404(Comment, pk=self.kwargs["comment_pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.parent_comment.post
        form.instance.parent_comment = self.parent_comment
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.post.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["parent_comment"] = self.parent_comment
        return context


class ReplyDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, BaseCommentView, DeleteView
):
    template_name = "comments/comment_confirm_delete.html"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.post.pk})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return redirect(success_url)
