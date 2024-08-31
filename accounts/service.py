import logging
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .forms import ProfileForm
from .models import Profile, User
from blog.models import Post
from .service import ProfileService

logger = logging.getLogger(__name__)

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
        user_stats = ProfileService.get_user_stats(user)
        is_own_profile = self.request.user == user
        context.update({
            "user_posts": Post.objects.filter(author=user, is_deleted=False).order_by("-created_at"),
            "is_own_profile": is_own_profile,
            "user_stats": user_stats,
            "follower_count": user_stats["follower_count"],
        })
        if self.request.user.is_authenticated:
            context["is_following"] = Follower.objects.filter(
                user=user, follower=self.request.user
            ).exists()
        else:
            context["is_following"] = False
        return context

class FollowTog