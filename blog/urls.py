from django.urls import path
from . import views
from .views import (
    CommentDeleteView,
    CustomLoginView,
    ProfileUpdateView,
    ProfileView,
    ReplyCreateView,
    ReplyDeleteView,
)

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("profile/update/", views.ProfileUpdateView.as_view(), name="profile_update"),
    path("profile/", views.ProfileView.as_view(), name="profile_view"),
    path("profile/<str:username>/", ProfileView.as_view(), name="profile_view"),
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
        "comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment_delete"
    ),
    path("reply/<int:pk>/delete/", ReplyDeleteView.as_view(), name="reply_delete"),
    path(
        "comment/<int:comment_pk>/reply/",
        ReplyCreateView.as_view(),
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
    path("follow/<int:user_id>/", views.follow_toggle, name="follow_toggle"),
    path("share/<int:post_id>/", views.share_post, name="share_post"),
    path("dashboard/", views.user_dashboard, name="user_dashboard"),
]
