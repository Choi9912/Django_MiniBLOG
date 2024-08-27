from django.utils import timezone
from django.db import models

from django.contrib.auth import get_user_model

from django.urls import reverse
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.utils.text import slugify

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_posts", kwargs={"slug": self.slug})

    class Meta:
        verbose_name_plural = "Categories"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        if not self.slug:
            self.slug = "tag"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("tag_posts", kwargs={"slug": self.slug})


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self, *args, **kwargs):
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True


class Post(SoftDeleteModel):
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
        "Category", null=True, blank=True, on_delete=models.SET_NULL
    )
    tags = models.ManyToManyField("Tag", blank=True)
    view_count = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    def __str__(self):
        return self.title

    def calculate_popularity(self):
        like_weight = 3
        comment_weight = 2
        return (
            self.likes.count() * like_weight
            + self.comment_set.count()
            * comment_weight  # comment_set을 사용하여 댓글 수 계산
        )

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})
