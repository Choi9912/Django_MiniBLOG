from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birthday = models.DateField(null=True, blank=True)
    images = models.ImageField(upload_to="profile_pics", blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("accounts:profile_view", kwargs={"username": self.user.username})


class Follower(models.Model):
    user = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    follower = models.ForeignKey(
        User, related_name="following", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "follower")

    def __str__(self):
        return f"{self.follower.username} follows {self.user.username}"
