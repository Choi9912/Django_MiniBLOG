from django.urls import path
from .views import (
    FollowToggleView,
    ProfileUpdateView,
    ProfileDetailView,
    CustomLoginView,
    user_dashboard,
    share_post,
)

app_name = "accounts"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="account_login"),
    path("profile/update/", ProfileUpdateView.as_view(), name="profile_update"),
    path("profile/<str:username>/", ProfileDetailView.as_view(), name="profile_view"),
    path("follow/<str:username>/", FollowToggleView.as_view(), name="follow_toggle"),
    path("share/<int:post_id>/", share_post, name="share_post"),
    path("dashboard/", user_dashboard, name="user_dashboard"),
]
