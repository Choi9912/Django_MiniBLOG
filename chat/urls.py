from django.urls import path

from .views import (
    ConversationListView,
    RoomView,
    StartConversationView,
    DeleteConversationView,
    get_chat_messages,
)

app_name = "chat"

urlpatterns = [
    path("", ConversationListView.as_view(), name="conversation_list"),
    path("room/<str:room_name>/", RoomView.as_view(), name="room"),
    path(
        "start/<str:username>/",
        StartConversationView.as_view(),
        name="start_conversation",
    ),
    path(
        "delete/<int:pk>/", DeleteConversationView.as_view(), name="delete_conversation"
    ),
    path("messages/<int:room_id>/", get_chat_messages, name="get_chat_messages"),
]
