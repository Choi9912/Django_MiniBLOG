from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Profile


class Command(BaseCommand):
    help = "Creates user profiles for users without one"

    def handle(self, *args, **kwargs):
        users_without_profile = User.objects.filter(profile__isnull=True)
        for user in users_without_profile:
            Profile.objects.create(user=user)
            self.stdout.write(
                self.style.SUCCESS(f"Profile created for user: {user.username}")
            )
