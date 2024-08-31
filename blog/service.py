from datetime import timedelta

from django.db.models import Q, Count, F, ExpressionWrapper, fields, Exists, OuterRef
from django.utils import timezone

from .models import Post, Like


class PostService:
    @staticmethod
    def get_popular_posts():
        return (
            Post.objects.filter(is_deleted=False)
            .annotate(
                popularity=ExpressionWrapper(
                    F("view_count") + (Count("likes") * 3) + (Count("comments") * 2),
                    output_field=fields.IntegerField(),
                )
            )
            .order_by("-popularity")[:5]
        )

    @staticmethod
    def get_weekly_ranking():
        yesterday = timezone.now().date() - timedelta(days=1)
        seven_days_ago = yesterday - timedelta(days=7)

        return (
            Post.objects.filter(
                is_deleted=False,
                created_at__date__gt=seven_days_ago,
                created_at__date__lte=yesterday,
            )
            .annotate(
                weekly_score=ExpressionWrapper(
                    F("view_count") + (Count("likes") * 3) + (Count("comments") * 2),
                    output_field=fields.IntegerField(),
                )
            )
            .order_by("-weekly_score")[:5]
        )

    @staticmethod
    def get_sorted_posts(sort_by, user=None):
        queryset = Post.objects.filter(is_deleted=False)

        if user and user.is_authenticated:
            queryset = queryset.annotate(
                liked_by_user=Exists(
                    Like.objects.filter(user=user, post=OuterRef("pk"))
                )
            )

        if sort_by == "latest":
            return queryset.order_by("-created_at")
        elif sort_by == "likes":
            return queryset.annotate(like_count=Count("likes")).order_by("-like_count")
        elif sort_by == "views":
            return queryset.order_by("-view_count")
        return queryset

    @staticmethod
    def increase_view_count(post):
        Post.objects.filter(pk=post.pk).update(view_count=F("view_count") + 1)
        post.refresh_from_db(fields=["view_count"])

    @staticmethod
    def toggle_like(user, post):
        like, created = Like.objects.get_or_create(user=user, post=post)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        likes_count = post.likes.count()
        return liked, likes_count

    @staticmethod
    def search_posts(query, search_type):
        queryset = Post.objects.filter(is_deleted=False)

        if query:
            if search_type == "title_content":
                queryset = queryset.filter(
                    Q(title__icontains=query) | Q(content__icontains=query)
                )
            elif search_type == "tag":
                queryset = queryset.filter(tags__name__icontains=query).distinct()
            elif search_type == "category":
                queryset = queryset.filter(category__name__icontains=query)
            elif search_type == "all":
                queryset = queryset.filter(
                    Q(title__icontains=query)
                    | Q(content__icontains=query)
                    | Q(tags__name__icontains=query)
                    | Q(category__name__icontains=query)
                ).distinct()
        return queryset
