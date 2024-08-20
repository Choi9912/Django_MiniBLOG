# blog/models.py
from django.db import models
from django.contrib.auth.models import User


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
        return f"/blog/tag/{self.slug}/"


from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


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
