from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Conversation, Message

User = get_user_model()


def get_user_conversations(user):
    return Conversation.objects.filter(participants=user).order_by("-updated_at")


def get_conversation_details(conversation, user):
    messages = conversation.messages.order_by("timestamp")
    other_participants = conversation.participants.exclude(id=user.id)
    other_participant = (
        other_participants.first() if other_participants.exists() else None
    )
    return messages, other_participant


def create_message(conversation, user, content):
    message = Message.objects.create(
        conversation=conversation, sender=user, content=content
    )
    message.read_by.add(user)
    return message


def start_conversation(user, participant):
    conversation = Conversation.objects.create()
    conversation.participants.add(user, participant)
    return conversation


def get_or_create_conversation(user, username):
    participant = get_object_or_404(User, username=username)
    conversation = (
        Conversation.objects.filter(participants=user)
        .filter(participants=participant)
        .first()
    )
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(user, participant)
    return conversation


def delete_conversation(user, conversation_id):
    return get_object_or_404(
        Conversation, id=conversation_id, participants=user
    ).delete()


def send_message(user, conversation_id, content):
    conversation = get_object_or_404(
        Conversation, id=conversation_id, participants=user
    )
    if content:
        message = Message.objects.create(
            conversation=conversation, sender=user, content=content
        )
        return message
    return None
