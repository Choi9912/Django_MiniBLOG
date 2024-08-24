from datetime import timezone
import re
from django.conf import settings
from django.db import IntegrityError
from django.http import JsonResponse
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from allauth.account.views import LoginView

from blog.forms import CustomPostForm, ProfileForm
from .models import Post, Comment, Category, Tag, Profile
from django.db.models import Count, F, ExpressionWrapper, fields
import markdown2

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import requests


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"

    def get_success_url(self):
        return reverse("post_list")


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "accounts/profile_update.html"

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse("profile_view", kwargs={"username": self.request.user.username})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user_posts"] = Post.objects.filter(author=user).order_by("-created_at")
        context["is_own_profile"] = True
        return context

    def form_valid(self, form):
        try:
            # 사용자 이름 변경 시도
            new_username = form.cleaned_data["username"]
            if new_username != self.request.user.username:
                if User.objects.filter(username=new_username).exists():
                    form.add_error("username", "이미 사용 중인 사용자 이름입니다.")
                    return self.form_invalid(form)
                self.request.user.username = new_username
                self.request.user.save()

            response = super().form_valid(form)
            messages.success(self.request, "프로필이 성공적으로 업데이트되었습니다.")
            return response
        except IntegrityError:
            form.add_error("username", "사용자 이름 업데이트 중 오류가 발생했습니다.")
            return self.form_invalid(form)


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
        context["is_own_profile"] = self.request.user == user

        if self.request.user.is_authenticated and not context["is_own_profile"]:
            context["is_following"] = self.request.user.profile.followers.filter(
                id=user.id
            ).exists()
        else:
            context["is_following"] = False

        return context


from django.db.models import Count, F, ExpressionWrapper, fields
from django.utils import timezone
from datetime import timedelta


class PopularPostsMixin:
    def get_popular_posts(self):
        return Post.objects.annotate(
            popularity=ExpressionWrapper(
                F("view_count") + (Count("likes") * 3) + (Count("comments") * 2),
                output_field=fields.IntegerField(),
            )
        ).order_by("-popularity")[:5]

    def get_weekly_ranking(self):
        one_week_ago = timezone.now() - timedelta(days=7)
        return (
            Post.objects.filter(created_at__gte=one_week_ago)
            .annotate(
                weekly_score=ExpressionWrapper(
                    F("view_count") + (Count("likes") * 3) + (Count("comments") * 2),
                    output_field=fields.IntegerField(),
                )
            )
            .order_by("-weekly_score")[:5]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_posts"] = self.get_popular_posts()
        context["weekly_ranking"] = self.get_weekly_ranking()
        return context


class PostListView(PopularPostsMixin, ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        queryset = Post.objects.all()
        sort_by = self.request.GET.get("sort", "latest")
        if sort_by == "latest":
            return queryset.order_by("-created_at")
        elif sort_by == "likes":
            return queryset.annotate(like_count=Count("likes")).order_by("-like_count")
        elif sort_by == "views":
            return queryset.order_by("-view_count")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["tags"] = Tag.objects.all()
        context["current_sort"] = self.request.GET.get("sort", "latest")
        context["show_sidebar"] = True
        return context


class PostDetailView(PopularPostsMixin, DetailView):
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
        content_html = markdown2.markdown(
            post.content, extras=["fenced-code-blocks", "tables"]
        )
        content_with_links = re.sub(
            r"#(\w+)",
            lambda m: f'<a href="{reverse("tag_posts", kwargs={"slug": m.group(1)})}" class="tag-link">#{m.group(1)}</a>',
            content_html,
        )
        context["content"] = content_with_links
        return context


from django.contrib import messages
from .utils import suggest_title_improvement


def suggest_title(request):
    original_title = request.GET.get("title", "")
    suggested_title = suggest_title_improvement(original_title)
    return JsonResponse({"suggested_title": suggested_title})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CustomPostForm
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("post_list")

    def form_valid(self, form):

        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_new_post"] = True
        return context


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


from django.views.generic import ListView
from django.db.models import Q
from .models import Post, Category


class PostSearchView(ListView):
    model = Post
    template_name = "blog/post_search.html"
    context_object_name = "posts"
    paginate_by = 10  # 페이지당 10개의 결과를 보여줍니다

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        search_type = self.request.GET.get("type", "all")

        if query:
            if search_type == "title":
                return Post.objects.filter(title__icontains=query)
            elif search_type == "tag":
                return Post.objects.filter(tags__name__icontains=query).distinct()
            elif search_type == "category":
                return Post.objects.filter(category__name__icontains=query).distinct()
            else:  # 'all' or any other value
                return Post.objects.filter(
                    Q(title__icontains=query)
                    | Q(content__icontains=query)
                    | Q(tags__name__icontains=query)
                    | Q(category__name__icontains=query)
                ).distinct()
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        context["search_type"] = self.request.GET.get("type", "all")
        context["categories"] = Category.objects.all()
        return context


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


class PostLikeToggleView(LoginRequiredMixin, View):
    @method_decorator(require_POST)
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


@method_decorator(csrf_exempt, name="dispatch")
class CommentLikeToggleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs["pk"])
        user = request.user

        if user in comment.likes.all():
            comment.likes.remove(user)
            liked = False
        else:
            comment.likes.add(user)
            liked = True

        return JsonResponse({"likes_count": comment.likes.count(), "liked": liked})


class ReplyCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ["content"]
    template_name = "blog/reply_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.parent_comment = get_object_or_404(Comment, pk=self.kwargs["comment_pk"])
        if self.parent_comment.parent_comment:
            messages.error(self.request, "답글에는 답글을 달 수 없습니다.")
            return redirect("post_detail", pk=self.parent_comment.post.pk)
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


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

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


class ReplyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def test_func(self):
        comment = self.get_object()
        return (
            self.request.user == comment.author and comment.parent_comment is not None
        )

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.post.pk})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return redirect(success_url)


@login_required
def notifications(request):
    notifications = request.user.notifications.order_by("-created_at")
    return render(request, "blog/notifications.html", {"notifications": notifications})


@login_required
@require_POST
def follow_toggle(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    profile = request.user.profile

    if profile.is_following(user_to_follow):
        profile.unfollow(user_to_follow)
        is_following = False
    else:
        profile.follow(user_to_follow)
        is_following = True

    return JsonResponse(
        {
            "is_following": is_following,
            "follower_count": user_to_follow.profile.followers.count(),
        }
    )


def share_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "blog/share_post.html", {"post": post})


from django.db.models import Count, Sum  # Sum을 추가로 임포트


@login_required
def user_dashboard(request):
    user_posts = Post.objects.filter(author=request.user)
    post_count = user_posts.count()
    total_views = user_posts.aggregate(total_views=Sum("view_count"))["total_views"]
    total_likes = user_posts.annotate(like_count=Count("likes")).aggregate(
        total_likes=Sum("like_count")
    )["total_likes"]
    follower_count = request.user.profile.followers.count()

    return render(
        request,
        "blog/user_dashboard.html",
        {
            "post_count": post_count,
            "total_views": total_views,
            "total_likes": total_likes,
            "follower_count": follower_count,
        },
    )
