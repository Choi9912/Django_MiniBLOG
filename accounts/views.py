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
from .models import Profile, User, Follower
from blog.models import Post

logger = logging.getLogger(__name__)


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
        "follower_count": Follower.objects.filter(user=user).count(),
    }


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "accounts/profile_update.html"

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_own_profile"] = True
        return context


class ProfileDetailView(DetailView):
    model = Profile
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
        user_stats = get_user_stats(user)
        is_own_profile = self.request.user == user
        context.update(
            {
                "user_posts": Post.objects.filter(
                    author=user, is_deleted=False
                ).order_by("-created_at"),
                "is_own_profile": is_own_profile,
                "user_stats": user_stats,
                "follower_count": user_stats["follower_count"],
            }
        )
        if self.request.user.is_authenticated:
            context["is_following"] = Follower.objects.filter(
                user=user, follower=self.request.user
            ).exists()
        else:
            context["is_following"] = False

        return context

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        if context["is_own_profile"]:
            response.context_data["body_class"] = "own-profile"
        return response


class FollowToggleView(LoginRequiredMixin, View):
    @method_decorator(require_POST)
    def post(self, request, username):
        logger.info(
            f"Follow toggle requested for {username} by {request.user.username}"
        )
        user_to_follow = get_object_or_404(User, username=username)
        user = request.user

        # 자기 자신을 팔로우하려는 시도 방지
        if user == user_to_follow:
            logger.warning(f"{user.username} attempted to follow themselves")
            return JsonResponse(
                {
                    "error": "You cannot follow yourself",
                    "is_following": False,
                    "follower_count": Follower.objects.filter(
                        user=user_to_follow
                    ).count(),
                },
                status=400,
            )

        follower, created = Follower.objects.get_or_create(
            user=user_to_follow, follower=user
        )
        if not created:
            follower.delete()
            is_following = False
            action = "unfollowed"
        else:
            is_following = True
            action = "followed"

        follower_count = Follower.objects.filter(user=user_to_follow).count()

        logger.info(
            f"{user.username} {action} {user_to_follow.username}. New follower count: {follower_count}"
        )

        return JsonResponse(
            {
                "is_following": is_following,
                "follower_count": follower_count,
            }
        )


@login_required
def user_dashboard(request):
    stats = get_user_stats(request.user)
    return render(request, "accounts/user_dashboard.html", stats)


def share_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "blog/share_post.html", {"post": post})
