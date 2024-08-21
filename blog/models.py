# blog/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.utils.text import slugify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_photo = models.ImageField(upload_to="profile_photos/", blank=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)
    slug = models.SlugField(
        max_length=200, db_index=True, unique=True, allow_unicode=True
    )
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/blog/category/{self.slug}/"

    class Meta:
        verbose_name_plural = "Categories"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        if not self.slug:  # 빈 문자열인 경우를 처리
            self.slug = "tag"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tag_posts", kwargs={"slug": self.slug})


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    head_image = ProcessedImageField(
        upload_to="blog/images/%Y/%m/%d/",
        processors=[ResizeToFill(300, 300)],
        format="JPEG",
        options={"quality": 60},
        blank=True,
    )
    file_upload = models.FileField(upload_to="blog/files/%Y/%m/%d/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL
    )
    tags = models.ManyToManyField(Tag, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_comment = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )
    likes = models.ManyToManyField(User, related_name="liked_comments", blank=True)
