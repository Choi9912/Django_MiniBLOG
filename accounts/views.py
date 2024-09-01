from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, UpdateView

from .forms import ProfileForm
from .models import Profile, User
from .service import ProfileService


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
        return ProfileService.get_or_create_profile(username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object.user
        user_stats = ProfileService.get_user_stats(user)
        is_own_profile = self.request.user == user
        context.update(
            {
                "user_posts": ProfileService.get_user_posts(user),
                "is_own_profile": is_own_profile,
                "user_stats": user_stats,
                "follower_count": user_stats['follower_count'],
                "is_following": (
                    ProfileService.is_following(self.request.user, user)
                    if self.request.user.is_authenticated
                    else False
                ),
            }
        )
        return context


class FollowToggleView(LoginRequiredMixin, View):
    @method_decorator(require_POST)
    def post(self, request, username):
        user_to_follow = User.objects.get(username=username)
        user = request.user

        try:
            is_following, follower_count = ProfileService.toggle_follow(
                user, user_to_follow
            )
            return JsonResponse(
                {"is_following": is_following, "follower_count": follower_count}
            )
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)


@login_required
def user_dashboard(request):
    stats = ProfileService.get_user_stats(request.user)
    return render(request, "accounts/user_dashboard.html", stats)


def share_post(request, post_id):
    from blog.models import Post

    post = Post.objects.get(id=post_id)
    return render(request, "blog/share_post.html", {"post": post})
