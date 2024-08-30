import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Conversation, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name = f"chat_{self.conversation_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.save_message(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": self.scope["user"].username,
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]

        await self.send(text_data=json.dumps({"message": message, "sender": sender}))

    @database_sync_to_async
    def save_message(self, message):
        conversation = Conversation.objects.get(id=self.conversation_id)
        Message.objects.create(
            conversation=conversation, sender=self.scope["user"], content=message
        )
