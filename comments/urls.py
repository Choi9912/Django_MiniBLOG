app_name = "comments"

from django.urls import path

from . import views

urlpatterns = [
    path(
        "post/<int:post_pk>/comment/new/",
        views.CommentCreateView.as_view(),
        name="comment_create",
    ),
    path(
        "comment/<int:pk>/update/",
        views.CommentUpdateView.as_view(),
        name="comment_update",
    ),
    path(
        "comment/<int:pk>/delete/",
        views.CommentDeleteView.as_view(),
        name="comment_delete",
    ),
    path(
        "comment/<int:comment_pk>/reply/new/",
        views.ReplyCreateView.as_view(),
        name="reply_create",
    ),
    path(
        "reply/<int:pk>/update/", views.ReplyUpdateView.as_view(), name="reply_update"
    ),
    path(
        "reply/<int:pk>/delete/", views.ReplyDeleteView.as_view(), name="reply_delete"
    ),
]
