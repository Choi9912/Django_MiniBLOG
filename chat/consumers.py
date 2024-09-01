import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import Conversation, Message
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Mark messages as read when user connects
        await self.mark_messages_as_read()

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

        # Update unread count for other participants
        await self.update_unread_count()

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "type": "chat_message",
            "message": message
        }))

    @database_sync_to_async
    def save_message(self, user_id, content, timestamp):
        user = User.objects.get(id=user_id)
        conversation = Conversation.objects.get(id=self.room_name)
        message = Message.objects.create(conversation=conversation, sender=user, content=content, timestamp=timestamp,
                                         is_read=False)
        return {
            "content": message.content,
            "sender_username": message.sender.username,
            "timestamp": message.timestamp
        }

    @database_sync_to_async
    def mark_messages_as_read(self):
        conversation = Conversation.objects.get(id=self.room_name)
        Message.objects.filter(conversation=conversation).exclude(sender=self.user).update(is_read=True)

        # Notify other users that messages have been read
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "messages_read",
                "user": self.user.username
            }
        )

    async def messages_read(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "type": "messages_read",
            "user": event["user"]
        }))

    @database_sync_to_async
    def update_unread_count(self):
        conversation = Conversation.objects.get(id=self.room_name)
        for participant in conversation.participants.exclude(id=self.user.id):
            unread_count = Message.objects.filter(conversation=conversation, sender=self.user, is_read=False).count()
            async_to_sync(self.channel_layer.group_send)(
                f"user_{participant.username}",
                {
                    "type": "unread_count_update",
                    "conversation_id": self.room_name,
                    "unread_count": unread_count
                }
            )


class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.user_group_name = f"user_{self.user.username}"

        # Join user group
        await self.channel_layer.group_add(self.user_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave user group
        await self.channel_layer.group_discard(self.user_group_name, self.channel_name)

    async def unread_count_update(self, event):
        # Send unread count update to WebSocket
        await self.send(text_data=json.dumps({
            "type": "unread_count_update",
            "conversation_id": event["conversation_id"],
            "unread_count": event["unread_count"]
        }))