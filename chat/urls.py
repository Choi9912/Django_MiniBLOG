from django.urls import path
from . import views

app_name = "chat"
urlpatterns = [
    path("", views.ConversationListView.as_view(), name="conversation_list"),
    path(
        "conversation/<int:pk>/",
        views.ConversationDetailView.as_view(),
        name="conversation_detail",
    ),
    path("start/", views.StartConversationView.as_view(), name="start_conversation"),
    path(
        "send_message/<int:conversation_id>/", views.send_message, name="send_message"
    ),
    path(
        "conversation/<int:pk>/delete/",
        views.ConversationDeleteView.as_view(),
        name="conversation_delete",
    ),
]
