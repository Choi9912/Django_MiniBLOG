from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect

from comments.forms import CommentForm
from .models import Post, Comment
from .service import CommentService


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "comments/comment_form.html"

    def form_valid(self, form):
        comment = CommentService.create_comment(
            form, self.request.user, self.kwargs["post_pk"]
        )
        return redirect(comment.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = get_object_or_404(Post, pk=self.kwargs["post_pk"])
        return context


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ["content"]
    template_name = "comments/comment_form.html"

    def form_valid(self, form):
        comment = CommentService.update_comment(
            self.object, form.cleaned_data["content"]
        )
        return redirect(comment.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = self.object.post
        return context


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "comments/comment_confirm_delete.html"

    def test_func(self):
        return self.request.user == self.get_object().author

    def form_valid(self, form):
        success_url = CommentService.delete_comment(self.object)
        return redirect(success_url)


class ReplyCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "comments/reply_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.parent_comment = get_object_or_404(Comment, pk=self.kwargs["comment_pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        reply = CommentService.create_reply(
            form, self.request.user, self.kwargs["comment_pk"]
        )
        return redirect(reply.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["parent_comment"] = self.parent_comment
        return context


class ReplyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ["content"]
    template_name = "comments/reply_form.html"

    def test_func(self):
        return self.request.user == self.get_object().author

    def form_valid(self, form):
        comment = CommentService.update_comment(
            self.object, form.cleaned_data["content"]
        )
        return redirect(comment.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(CommentService.get_comment_context(self.object))
        return context


class ReplyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "comments/comment_confirm_delete.html"

    def test_func(self):
        return self.request.user == self.get_object().author

    def form_valid(self, form):
        success_url = CommentService.delete_comment(self.object)
        return redirect(success_url)
