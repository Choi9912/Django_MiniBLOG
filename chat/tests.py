# chat/tests.py
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from chat.models import Conversation, Message

User = get_user_model()


class ChatTests(TestCase):
    def setUp(self):
        # Setup users
        self.user1 = User.objects.create_user(username="user1", password="12345")
        self.user2 = User.objects.create_user(username="user2", password="12345")
        self.client = Client()
        self.conversation = Conversation.objects.create()
        self.conversation.participants.add(self.user1, self.user2)
        self.message = Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            content="Hello user2",
        )

    def test_conversation_list_view(self):
        self.client.login(username="user1", password="12345")
        response = self.client.get(reverse("chat:conversation_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, self.user2.username
        )  # Check if the participant's username is rendered in the template

    def test_room_view_access(self):
        self.client.login(username="user1", password="12345")
        response = self.client.get(reverse("chat:room", args=[self.conversation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello user2")

    def test_start_conversation_view(self):
        self.client.login(username="user1", password="12345")
        response = self.client.get(
            reverse("chat:start_conversation", kwargs={"username": "user2"})
        )
        self.assertRedirects(
            response, reverse("chat:room", kwargs={"room_name": self.conversation.id})
        )

    def test_delete_conversation_view(self):
        self.client.login(username="user1", password="12345")
        response = self.client.post(
            reverse("chat:delete_conversation", kwargs={"pk": self.conversation.id})
        )
        self.assertRedirects(response, reverse("chat:conversation_list"))
        self.assertFalse(Conversation.objects.filter(id=self.conversation.id).exists())

    def test_get_chat_messages(self):
        self.client.login(username="user1", password="12345")
        response = self.client.get(
            reverse("chat:get_chat_messages", kwargs={"room_id": self.conversation.id})
        )
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertEqual(len(json_response), 1)
        self.assertEqual(json_response[0]["content"], "Hello user2")


if __name__ == "__main__":
    TestCase.main()
