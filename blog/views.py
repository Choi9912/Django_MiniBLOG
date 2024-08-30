from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count, F, ExpressionWrapper, fields
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from datetime import timedelta
import re
from django.db import transaction
from .models import Post, Category, Tag
from blog.forms import CustomPostForm


class PopularPostsMixin:
    def get_popular_posts(self):
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

    def get_weekly_ranking(self):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_posts"] = self.get_popular_posts()
        context["weekly_ranking"] = self.get_weekly_ranking()
        return context


class SortPostsMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get("sort", "latest")
        if sort_by == "latest":
            return queryset.order_by("-created_at")
        elif sort_by == "likes":
            return queryset.annotate(like_count=Count("likes")).order_by("-like_count")
        elif sort_by == "views":
            return queryset.order_by("-view_count")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_sort"] = self.request.GET.get("sort", "latest")
        return context


class PostListView(SortPostsMixin, PopularPostsMixin, ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["tags"] = Tag.objects.all()
        context["show_sidebar"] = True
        return context


class PostDetailView(PopularPostsMixin, DetailView):
    model = Post
    template_name = "blog/post_detail.html"

    def get_object(self):
        obj = super().get_object()
        if obj.is_deleted:
            raise Http404("존재하지 않는 게시글입니다.")
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.increase_view_count()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    @transaction.atomic
    def increase_view_count(self):
        Post.objects.filter(pk=self.object.pk).update(view_count=F("view_count") + 1)
        self.object.refresh_from_db(fields=["view_count"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        content_with_links = re.sub(
            r"#(\w+)",
            lambda m: f'<a href="{reverse("tag_posts", kwargs={"slug": m.group(1)})}" class="tag-link">#{m.group(1)}</a>',
            post.content,
        )
        context["content"] = content_with_links
        context["view_count"] = post.view_count
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CustomPostForm
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("post_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_new_post"] = True
        return context


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = CustomPostForm
    template_name = "blog/post_form.html"


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post_list")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class PostSearchView(ListView):
    model = Post
    template_name = "blog/post_search.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        search_type = self.request.GET.get("type", "all")

        queryset = Post.objects.all()

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        context["search_type"] = self.request.GET.get("type", "all")
        return context


class PostLikeToggleView(View):
    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"error": "login_required"}, status=401)
            else:
                return HttpResponseRedirect(reverse("login") + f"?next={request.path}")

        post = get_object_or_404(Post, pk=kwargs["pk"])
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True

        return JsonResponse({"likes_count": post.likes.count(), "liked": liked})


class CategoryListView(ListView):
    model = Category
    template_name = "blog/category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.annotate(post_count=Count("post"))


class CategoryPostListView(SortPostsMixin, ListView):
    model = Post
    template_name = "blog/category_posts.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        return super().get_queryset().filter(category=self.category)


class TagListView(ListView):
    model = Tag
    template_name = "blog/tag_list.html"
    context_object_name = "tags"

    def get_queryset(self):
        return Tag.objects.annotate(post_count=Count("post")).filter(post_count__gt=0)


class TagPostListView(SortPostsMixin, ListView):
    model = Post
    template_name = "blog/tag_posts.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs.get("slug"))
        return super().get_queryset().filter(tags=self.tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.tag
        return context


class TagDetailView(DetailView):
    model = Tag
    template_name = "blog/tag_detail.html"
    context_object_name = "tag"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = self.object.get_posts()
        return context
