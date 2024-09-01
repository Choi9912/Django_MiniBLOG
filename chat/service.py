from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Conversation, Message

User = get_user_model()


def get_user_conversations(user):
    return Conversation.objects.filter(participants=user).order_by('-updated_at')


def get_or_create_conversation(user1, username2):
    user2 = User.objects.get(username=username2)
    conversation = Conversation.objects.filter(participants=user1).filter(participants=user2).first()

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(user1, user2)

    return conversation


def create_message(conversation, user, content):
    message = Message.objects.create(
        conversation=conversation,
        sender=user,
        content=content
    )
    conversation.updated_at = message.timestamp
    conversation.save()
    return message

# ... 기타 필요한 함수들 ...