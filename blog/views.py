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
from django.db.models import Count

from .models import Post, Category, Tag
from .forms import CustomPostForm
from .service import PostService


class PopularPostsMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_posts"] = PostService.get_popular_posts()
        context["weekly_ranking"] = PostService.get_weekly_ranking()
        return context


class SortPostsMixin:
    def get_queryset(self):
        sort_by = self.request.GET.get("sort", "latest")
        return PostService.get_sorted_posts(sort_by, self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_sort"] = self.request.GET.get("sort", "latest")
        return context


class PostListView(SortPostsMixin, PopularPostsMixin, ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 6

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
        PostService.increase_view_count(self.object)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        context["view_count"] = post.view_count
        context["likes_count"] = post.likes.count()
        if self.request.user.is_authenticated:
            context["user_has_liked"] = post.likes.filter(
                user=self.request.user
            ).exists()
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
        return PostService.search_posts(query, search_type)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        context["search_type"] = self.request.GET.get("type", "all")
        return context


class PostLikeToggleView(View):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "login_required"}, status=401)

        post = get_object_or_404(Post, pk=pk)
        liked, likes_count = PostService.toggle_like(request.user, post)

        return JsonResponse({"liked": liked, "likes_count": likes_count})


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
        queryset = (
            super().get_queryset().filter(category=self.category, is_deleted=False)
        )
        sort_by = self.request.GET.get("sort", "latest")
        return PostService.get_sorted_posts(sort_by, self.request.user).filter(
            category=self.category
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context


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
        queryset = super().get_queryset().filter(tags=self.tag, is_deleted=False)
        sort_by = self.request.GET.get("sort", "latest")
        return PostService.get_sorted_posts(sort_by, self.request.user).filter(
            tags=self.tag
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.tag
        return context
