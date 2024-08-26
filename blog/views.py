from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect
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
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from datetime import timedelta
import markdown2
import re


from accounts.models import Profile
from .models import Post, Category, Tag
from blog.forms import CustomPostForm


class BasePostView:
    model = Post


class BaseProfileView:
    model = Profile


class BaseCategoryView:
    model = Category


class BaseTagView:
    model = Tag


class PopularPostsMixin:
    def get_popular_posts(self):
        return Post.objects.annotate(
            popularity=ExpressionWrapper(
                F("view_count") + (Count("likes") * 3) + (Count("comments") * 2),
                output_field=fields.IntegerField(),
            )
        ).order_by("-popularity")[:5]

    def get_weekly_ranking(self):
        yesterday = timezone.now().date() - timedelta(days=1)
        seven_days_ago = yesterday - timedelta(days=7)

        return (
            Post.objects.filter(
                created_at__date__gt=seven_days_ago, created_at__date__lte=yesterday
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


class PostListView(PopularPostsMixin, BasePostView, ListView):
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        queryset = Post.objects.filter(is_deleted=False)
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
        context["categories"] = Category.objects.all()
        context["tags"] = Tag.objects.all()
        context["current_sort"] = self.request.GET.get("sort", "latest")
        context["show_sidebar"] = True
        return context


class PostDetailView(PopularPostsMixin, BasePostView, DetailView):
    template_name = "blog/post_detail.html"

    def get_object(self):
        obj = super().get_object()
        if obj.is_deleted:
            raise Http404("존재하지 않는 게시글입니다.")
        obj.view_count += 1
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        content_html = markdown2.markdown(
            post.content, extras=["fenced-code-blocks", "tables"]
        )
        content_with_links = re.sub(
            r"#(\w+)",
            lambda m: f'<a href="{reverse("tag_posts", kwargs={"slug": m.group(1)})}" class="tag-link">#{m.group(1)}</a>',
            content_html,
        )
        context["content"] = content_with_links
        return context


class PostCreateView(LoginRequiredMixin, BasePostView, CreateView):
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


class PostUpdateView(LoginRequiredMixin, BasePostView, UpdateView):
    form_class = CustomPostForm
    template_name = "blog/post_form.html"

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.pk})


class PostDeleteView(LoginRequiredMixin, BasePostView, DeleteView):
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.is_deleted = True
        self.object.deleted_at = timezone.now()
        self.object.save()
        return redirect(success_url)


class PostSearchView(BasePostView, ListView):
    template_name = "blog/post_search.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        search_type = self.request.GET.get("type", "all")

        if query:
            if search_type == "title":
                return Post.objects.filter(title__icontains=query)
            elif search_type == "tag":
                return Post.objects.filter(tags__name__icontains=query).distinct()
            elif search_type == "category":
                return Post.objects.filter(category__name__icontains=query).distinct()
            else:
                return Post.objects.filter(
                    Q(title__icontains=query)
                    | Q(content__icontains=query)
                    | Q(tags__name__icontains=query)
                    | Q(category__name__icontains=query)
                ).distinct()
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        context["search_type"] = self.request.GET.get("type", "all")
        context["categories"] = Category.objects.all()
        return context


class PostLikeToggleView(BasePostView, View):
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


class CategoryListView(BaseCategoryView, ListView):
    template_name = "blog/category_list.html"
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.annotate(post_count=Count("post"))
        return context


class CategoryPostListView(ListView):
    model = Post
    template_name = "blog/category_posts.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        return Post.objects.filter(category=self.category).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context


class TagListView(BaseTagView, ListView):
    template_name = "blog/tag_list.html"
    context_object_name = "tags"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = Tag.objects.annotate(post_count=Count("post")).filter(post_count__gt=0)
        context["tags"] = tags
        return context


class TagPostListView(ListView):
    model = Post
    template_name = "blog/tag_posts.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        tag_slug = self.kwargs.get("slug")
        if not tag_slug:
            return Post.objects.none()
        self.tag = get_object_or_404(Tag, slug=tag_slug)
        return Post.objects.filter(tags=self.tag).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = getattr(self, "tag", None)
        return context


class TagDetailView(BaseTagView, DetailView):
    template_name = "blog/tag_detail.html"
    context_object_name = "tag"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(tags=self.object)
        return context
