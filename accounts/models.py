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
    followers = models.ManyToManyField(User, related_name="following", blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("accounts:profile_view", kwargs={"username": self.user.username})
