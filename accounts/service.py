from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum, Count
from django.shortcuts import get_object_or_404

from blog.models import Post
from .models import Profile, User, Follower


class ProfileService:
    @staticmethod
    def get_user_stats(user):
        user_posts = Post.objects.filter(author=user)
        stats = user_posts.aggregate(
            post_count=Count("id"),
            total_views=Sum("view_count"),
            total_likes=Sum("likes__id", distinct=True),
            follower_count=Count("author__followers", distinct=True),
        )
        return {k: v or 0 for k, v in stats.items()}

    @staticmethod
    def get_or_create_profile(username):
        try:
            return Profile.objects.select_related("user").get(user__username=username)
        except Profile.DoesNotExist:
            user = get_object_or_404(User, username=username)
            return Profile.objects.create(user=user)

    @staticmethod
    def is_following(user, target_user):
        return Follower.objects.filter(user=target_user, follower=user).exists()

    @staticmethod
    @transaction.atomic
    def toggle_follow(user, user_to_follow):
        if user == user_to_follow:
            raise ValidationError("You cannot follow yourself")

        follower, created = Follower.objects.get_or_create(
            user=user_to_follow, follower=user
        )
        if not created:
            follower.delete()
            is_following = False
        else:
            is_following = True

        follower_count = Follower.objects.filter(user=user_to_follow).count()
        return is_following, follower_count

    @staticmethod
    def get_user_posts(user, include_deleted=False):
        posts = Post.objects.filter(author=user)
        if not include_deleted:
            posts = posts.filter(is_deleted=False)
        return posts.order_by("-created_at")
