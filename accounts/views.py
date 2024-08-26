from venv import logger
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic import (
    DetailView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum

from django.db import IntegrityError

from accounts.forms import ProfileForm
from accounts.models import Profile
from blog.models import Post

from allauth.account.views import LoginView
from django.contrib.auth import get_user_model

User = get_user_model()


class BasePostView:
    model = Post


class BaseProfileView:
    model = Profile


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"

    def get_success_url(self):
        return reverse("post_list")


class ProfileUpdateView(LoginRequiredMixin, BaseProfileView, UpdateView):
    form_class = ProfileForm
    template_name = "accounts/profile_update.html"

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse(
            "accounts:profile_view",
            kwargs={"username": self.request.user.username},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user_posts"] = Post.objects.filter(author=user).order_by("-created_at")
        context["is_own_profile"] = True
        return context

    def form_valid(self, form):
        try:
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
        if self.object:
            user = self.object.user
            context["user_posts"] = Post.objects.filter(author=user).order_by(
                "-created_at"
            )
            context["is_own_profile"] = self.request.user == user

            if self.request.user.is_authenticated and not context["is_own_profile"]:
                context["is_following"] = self.request.user.profile.followers.filter(
                    id=user.id
                ).exists()
            else:
                context["is_following"] = False
        return context


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
            return JsonResponse({"error": "Cannot follow yourself"}, status=400)

        if user.profile.is_following(user_to_follow):
            user.profile.unfollow(user_to_follow)
            is_following = False
            logger.info(f"{user.username} unfollowed {user_to_follow.username}")
        else:
            user.profile.follow(user_to_follow)
            is_following = True
            logger.info(f"{user.username} followed {user_to_follow.username}")

        return JsonResponse(
            {
                "is_following": is_following,
                "follower_count": user_to_follow.profile.followers.count(),
            }
        )


def share_post(cls, request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "blog/share_post.html", {"post": post})


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
        "accounts/user_dashboard.html",
        {
            "post_count": post_count,
            "total_views": total_views,
            "total_likes": total_likes,
            "follower_count": follower_count,
        },
    )
