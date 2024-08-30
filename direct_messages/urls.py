from django.urls import path
from .views import InboxView, SendMessageView, MessageDetailView

app_name = "direct_messages"

urlpatterns = [
    path("inbox/", InboxView.as_view(), name="inbox"),
    path("send/", SendMessageView.as_view(), name="send_message"),
    path("detail/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
]
