from django.db import models
from django.contrib.auth import get_user_model

from django.dispatch import receiver
from django.db.models.signals import post_save

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

    def follow(self, user):
        if not self.is_following(user):
            user.profile.followers.add(self.user)

    def unfollow(self, user):
        if self.is_following(user):
            user.profile.followers.remove(self.user)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
