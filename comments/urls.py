from django.urls import path
from .views import (
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    ReplyCreateView,
    ReplyDeleteView,
)

app_name = "comments"

urlpatterns = [
    path(
        "post/<int:post_pk>/comment/new/",
        CommentCreateView.as_view(),
        name="comment_create",
    ),
    path("comment/<int:pk>/edit/", CommentUpdateView.as_view(), name="comment_update"),
    path(
        "comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment_delete"
    ),
    path(
        "comment/<int:comment_pk>/reply/",
        ReplyCreateView.as_view(),
        name="reply_create",
    ),
    path("reply/<int:pk>/delete/", ReplyDeleteView.as_view(), name="reply_delete"),
]
