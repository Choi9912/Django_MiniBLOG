import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import Conversation, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        timestamp = timezone.now()

        # Save message to database
        saved_message = await self.save_message(self.user.id, message, timestamp)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": {
                    "content": saved_message["content"],
                    "sender": saved_message["sender_username"],
                    "timestamp": saved_message["timestamp"].isoformat()
                }
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "content": message["content"],
            "sender": message["sender"],
            "timestamp": message["timestamp"]
        }))

    @database_sync_to_async
    def save_message(self, user_id, content, timestamp):
        user = User.objects.get(id=user_id)
        conversation = Conversation.objects.get(id=self.room_name)
        message = Message.objects.create(conversation=conversation, sender=user, content=content, timestamp=timestamp)
        return {
            "content": message.content,
            "sender_username": message.sender.username,
            "timestamp": message.timestamp
        }