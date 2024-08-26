from django.urls import path
from . import views
from .views import (
    CustomLoginView,
    ProfileView,
    PostView,
    CommentView,
    CategoryView,
    TagView,
    UserInteractionView,
    user_dashboard,
)

urlpatterns = [
    path("", PostView.List.as_view(), name="post_list"),
    path("login/", CustomLoginView.as_view(), name="account_login"),
    # Profile URLs
    path("profile/update/", ProfileView.Update.as_view(), name="profile_update"),
    path("profile/<str:username>/", ProfileView.Detail.as_view(), name="profile_view"),
    # Post URLs
    path("post/<int:pk>/", PostView.Detail.as_view(), name="post_detail"),
    path("post/new/", PostView.Create.as_view(), name="create_post"),
    path(
        "post/<int:pk>/edit/",
        PostView.Update.as_view(),
        name="post_update",
    ),
    path("post/<int:pk>/delete/", PostView.Delete.as_view(), name="post_delete"),
    path("post/<int:pk>/like/", PostView.LikeToggle.as_view(), name="like_post"),
    path("search/", PostView.Search.as_view(), name="post_search"),
    # Comment URLs
    path(
        "post/<int:post_pk>/comment/new/",
        CommentView.Create.as_view(),
        name="comment_create",
    ),
    path("comment/<int:pk>/edit/", CommentView.Update.as_view(), name="comment_update"),
    path(
        "comment/<int:pk>/delete/", CommentView.Delete.as_view(), name="comment_delete"
    ),
    path(
        "comment/<int:comment_pk>/reply/",
        CommentView.ReplyCreate.as_view(),
        name="reply_create",
    ),
    path(
        "reply/<int:pk>/delete/", CommentView.ReplyDelete.as_view(), name="reply_delete"
    ),
    # Category URLs
    path("categories/", CategoryView.List.as_view(), name="category_list"),
    path(
        "category/<str:slug>/", CategoryView.PostList.as_view(), name="category_posts"
    ),
    # Tag URLs
    path("tags/", TagView.List.as_view(), name="tag_list"),
    path("tag/<str:slug>/", TagView.PostList.as_view(), name="tag_posts"),
    path("tag/<str:slug>/detail/", TagView.Detail.as_view(), name="tag_detail"),
    # User Interaction URLs
    path("notifications/", UserInteractionView.notifications, name="notifications"),
    path(
        "follow/<str:username>/",
        UserInteractionView.follow_toggle,
        name="follow_toggle",
    ),
    path("share/<int:post_id>/", UserInteractionView.share_post, name="share_post"),
    path("dashboard/", user_dashboard, name="user_dashboard"),  # 수정된 부분
    # Other URLs
]
