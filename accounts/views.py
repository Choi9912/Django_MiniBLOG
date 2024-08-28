import logging
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count

from .forms import ProfileForm
from .models import Profile, User
from blog.models import Post

logger = logging.getLogger(__name__)


class BasePostView:
    model = Post


class BaseProfileView:
    model = Profile


def get_user_stats(user):
    user_posts = Post.objects.filter(author=user)
    return {
        "post_count": user_posts.count(),
        "total_views": user_posts.aggregate(total_views=Sum("view_count"))[
            "total_views"
        ]
        or 0,
        "total_likes": user_posts.annotate(like_count=Count("likes")).aggregate(
            total_likes=Sum("like_count")
        )["total_likes"]
        or 0,
        "follower_count": user.profile.followers.count(),
    }


class ProfileUpdateView(LoginRequiredMixin, BaseProfileView, UpdateView):
    form_class = ProfileForm
    template_name = "accounts/profile_update.html"

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_own_profile"] = True
        return context


class ProfileDetailView(BaseProfileView, DetailView):
    template_name = "accounts/profile.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        username = self.kwargs.get("username")
        user = get_object_or_404(User, username=username)
        profile, _ = Profile.objects.get_or_create(user=user)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object.user
        context["user_posts"] = Post.objects.filter(
            author=user, is_deleted=False
        ).order_by("-created_at")
        context["is_own_profile"] = self.request.user == user
        if self.request.user.is_authenticated and not context["is_own_profile"]:
            context["is_following"] = self.is_following(self.request.user, user)
        else:
            context["is_following"] = False
        context["user_stats"] = get_user_stats(user)
        return context

    def is_following(self, user, target_user):
        return user.following.filter(user=target_user).exists()


class FollowToggleView(LoginRequiredMixin, View):
    @method_decorator(require_POST)
    def post(self, request, username):
        logger.info(
            f"Follow toggle requested for {username} by {request.user.username}"
        )
        user_to_follow = get_object_or_404(User, username=username)
        user = request.user

        if user == user_to_follow:
            logger.warning(f"User {user.username} attempted to follow themselves")
            return JsonResponse({"error": "자신을 팔로우 할 수 없습니다"}, status=400)

        is_following = self.toggle_follow(user, user_to_follow)
        action = "followed" if is_following else "unfollowed"
        logger.info(f"{user.username} {action} {user_to_follow.username}")

        return JsonResponse(
            {
                "is_following": is_following,
                "follower_count": user_to_follow.profile.followers.count(),
            }
        )

    def toggle_follow(self, user, target_user):
        if self.is_following(user, target_user):
            target_user.profile.followers.remove(user)
            return False
        else:
            target_user.profile.followers.add(user)
            return True

    def is_following(self, user, target_user):
        return user.following.filter(user=target_user).exists()


@login_required
def user_dashboard(request):
    stats = get_user_stats(request.user)
    return render(request, "accounts/user_dashboard.html", stats)


def share_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "blog/share_post.html", {"post": post})
