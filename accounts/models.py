from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from blog.models import Post


User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birthday = models.DateField(null=True, blank=True)
    images = models.ImageField(upload_to="profile_pics", blank=True)
    followers = models.ManyToManyField(User, related_name="following", blank=True)

    def __str__(self):
        return self.user.username

    def is_following(self, user):
        return self.user.following.filter(user=user).exists()

    def toggle_follow(self, user):
        if self.is_following(user):
            user.profile.followers.remove(self.user)
            return False
        else:
            user.profile.followers.add(self.user)
            return True

    def get_absolute_url(self):
        return reverse("accounts:profile_view", kwargs={"username": self.user.username})

    def get_stats(self):

        user_posts = Post.objects.filter(author=self.user)
        return {
            "post_count": user_posts.count(),
            "total_views": user_posts.aggregate(total_views=models.Sum("view_count"))[
                "total_views"
            ]
            or 0,
            "total_likes": user_posts.annotate(
                like_count=models.Count("likes")
            ).aggregate(total_likes=models.Sum("like_count"))["total_likes"]
            or 0,
            "follower_count": self.followers.count(),
        }
