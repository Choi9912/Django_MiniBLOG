import re
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from allauth.account.views import LoginView

from blog.forms import CustomPostForm, ProfileForm
from .models import Post, Comment, Category, Tag, Profile
from django.db.models import Count
import markdown2


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"

    def get_success_url(self):
        return reverse("post_list")


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "accounts/profile_update.html"
    success_url = reverse_lazy("profile_view")

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        # Print or log form errors if needed
        if not form.is_valid():
            print(form.errors)
        return super().form_valid(form)


from django.contrib.auth.models import User


class ProfileView(DetailView):
    model = Profile
    template_name = "accounts/profile.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        username = self.kwargs.get("username")
        user = get_object_or_404(User, username=username)
        profile, created = Profile.objects.get_or_create(user=user)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object.user
        context["user_posts"] = Post.objects.filter(author=user).order_by("-created_at")
        context["is_own_profile"] = (
            self.request.user.is_authenticated and self.request.user == user
        )
        return context


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        queryset = Post.objects.all()

        # 정렬 옵션 처리
        sort_by = self.request.GET.get("sort", "latest")
        if sort_by == "latest":
            queryset = queryset.order_by("-created_at")
        elif sort_by == "likes":
            queryset = queryset.annotate(like_count=Count("likes")).order_by(
                "-like_count"
            )
        elif sort_by == "views":
            queryset = queryset.order_by("-view_count")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["tags"] = Tag.objects.all()
        context["current_sort"] = self.request.GET.get("sort", "latest")
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

    def get_object(self):
        obj = super().get_object()
        obj.view_count += 1
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        # 마크다운을 HTML로 변환
        content_html = markdown2.markdown(
            post.content, extras=["fenced-code-blocks", "tables"]
        )

        # HTML에서 태그 링크 생성
        content_with_links = re.sub(
            r"#(\w+)",
            lambda m: f'<a href="{reverse("tag_posts", kwargs={"slug": m.group(1)})}" class="tag-link">#{m.group(1)}</a>',
            content_html,
        )

        context["content"] = content_with_links
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CustomPostForm
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("post_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = CustomPostForm
    template_name = "blog/post_form.html"

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.pk})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post_list")


class PostSearchView(ListView):
    model = Post
    template_name = "blog/post_search.html"
    context_object_name = "posts"

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = "blog/comment_form.html"
    fields = ["content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs["post_pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.post.pk})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = "blog/comment_form.html"
    fields = ["content"]

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.post.pk})


class CategoryListView(ListView):
    model = Category
    template_name = "blog/category_list.html"
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.annotate(post_count=Count("post"))
        return context


class CategoryPostListView(ListView):
    model = Post
    template_name = "blog/category_posts.html"
    context_object_name = "posts"
    paginate_by = 6  # 페이지당 포스트 수, PostListView와 일치시킴

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        return Post.objects.filter(category=self.category).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context


class TagListView(ListView):
    model = Tag
    template_name = "blog/tag_list.html"
    context_object_name = "tags"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = Tag.objects.annotate(post_count=Count("post")).filter(post_count__gt=0)
        context["tags"] = tags
        return context


class TagPostListView(ListView):
    model = Post
    template_name = "blog/tag_posts.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        tag_slug = self.kwargs.get("slug")
        if not tag_slug:
            return Post.objects.none()  # 빈 쿼리셋 반환
        self.tag = get_object_or_404(Tag, slug=tag_slug)
        return Post.objects.filter(tags=self.tag).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = getattr(self, "tag", None)
        return context


class TagDetailView(DetailView):
    model = Tag
    template_name = "blog/tag_detail.html"
    context_object_name = "tag"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(tags=self.object)
        return context


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name="dispatch")
class PostLikeToggleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs["pk"])
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True

        return JsonResponse({"likes_count": post.likes.count(), "liked": liked})


class CommentLikeToggleView(LoginRequiredMixin, DetailView):
    model = Comment

    def post(self, request, *args, **kwargs):
        comment = self.get_object()
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)
        return redirect("post_detail", pk=comment.post.pk)


class ReplyCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = "blog/reply_form.html"
    fields = ["content"]

    def form_valid(self, form):
        parent_comment = get_object_or_404(Comment, pk=self.kwargs["comment_pk"])
        form.instance.author = self.request.user
        form.instance.post = parent_comment.post
        form.instance.parent_comment = parent_comment
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parent_comment = get_object_or_404(Comment, pk=self.kwargs["comment_pk"])
        context["parent_comment"] = parent_comment
        return context

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.post.pk})
