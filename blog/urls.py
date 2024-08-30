from django.urls import path
from .views import (
    CategoryListView,
    CategoryPostListView,
    TagListView,
    TagPostListView,
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostSearchView,
    PostLikeToggleView,
)

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post/new/", PostCreateView.as_view(), name="create_post"),
    path("post/<int:pk>/edit/", PostUpdateView.as_view(), name="post_update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path("like/<int:pk>/", PostLikeToggleView.as_view(), name="post_like_toggle"),
    path("search/", PostSearchView.as_view(), name="post_search"),
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("category/<str:slug>/", CategoryPostListView.as_view(), name="category_posts"),
    path("tags/", TagListView.as_view(), name="tag_list"),
    path("tag/<str:slug>/", TagPostListView.as_view(), name="tag_posts"),
]
