from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.ConversationListView.as_view(), name='conversation_list'),
    path('<str:room_name>/', views.RoomView.as_view(), name='room'),
    path('start/', views.StartConversationView.as_view(), name='start_conversation'),
    path('<int:room_id>/messages/', views.get_chat_messages, name='get_chat_messages'),

    path('delete/<int:pk>/', views.DeleteConversationView.as_view(), name='delete_conversation'),
]