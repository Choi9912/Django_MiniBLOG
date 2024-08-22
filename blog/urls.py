from django.urls import path
from . import views
from .views import CustomLoginView, ProfileUpdateView, ProfileView

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("profile/", views.ProfileView.as_view(), name="profile_view"),
    path("profile/<str:username>/", ProfileView.as_view(), name="profile_view"),
    path("profile/update/", views.ProfileUpdateView.as_view(), name="profile_update"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("post/new/", views.PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/edit/", views.PostUpdateView.as_view(), name="post_update"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
    path("login/", CustomLoginView.as_view(), name="account_login"),
    path("search/", views.PostSearchView.as_view(), name="post_search"),
    path(
        "post/<int:post_pk>/comment/new/",
        views.CommentCreateView.as_view(),
        name="comment_create",
    ),
    path(
        "comment/<int:pk>/edit/",
        views.CommentUpdateView.as_view(),
        name="comment_update",
    ),
    path(
        "comment/<int:pk>/delete/",
        views.CommentDeleteView.as_view(),
        name="comment_delete",
    ),
    path(
        "post/<int:pk>/like/",
        views.PostLikeToggleView.as_view(),
        name="post_like_toggle",
    ),
    path(
        "comment/<int:pk>/like/",
        views.CommentLikeToggleView.as_view(),
        name="comment_like_toggle",
    ),
    path(
        "comment/<int:comment_pk>/reply/new/",
        views.ReplyCreateView.as_view(),
        name="reply_create",
    ),
    path("categories/", views.CategoryListView.as_view(), name="category_list"),
    path("tags/", views.TagListView.as_view(), name="tag_list"),
    path(
        "category/<str:slug>/",
        views.CategoryPostListView.as_view(),
        name="category_posts",
    ),
    path("tag/<str:slug>/", views.TagPostListView.as_view(), name="tag_posts"),
]
