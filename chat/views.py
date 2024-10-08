from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, RedirectView, ListView, DeleteView

from .models import Conversation, Message
from .service import (
    get_or_create_conversation,
    get_user_conversations,
    mark_messages_as_read,
)

User = get_user_model()


class ConversationListView(LoginRequiredMixin, ListView):
    template_name = "chat/conversation_list.html"
    context_object_name = "conversations"

    def get_queryset(self):
        return get_user_conversations(self.request.user)


class RoomView(LoginRequiredMixin, TemplateView):
    template_name = "chat/room.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_name = self.kwargs["room_name"]
        conversation = get_object_or_404(Conversation, id=room_name)
        other_participant = conversation.participants.exclude(
            id=self.request.user.id
        ).first()

        mark_messages_as_read(conversation, self.request.user)

        context["room_name"] = room_name
        context["conversation"] = conversation
        context["other_user"] = (
            other_participant.username if other_participant else "Unknown"
        )
        context["initial_messages"] = Message.objects.filter(
            conversation=conversation
        ).order_by("timestamp")
        return context


class StartConversationView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        username = self.kwargs.get("username") or self.request.POST.get("username")
        if not username:
            return reverse("chat:conversation_list")
        conversation = get_or_create_conversation(self.request.user, username)
        return reverse("chat:room", kwargs={"room_name": conversation.id})


class DeleteConversationView(LoginRequiredMixin, DeleteView):
    model = Conversation
    success_url = reverse_lazy("chat:conversation_list")

    def get_queryset(self):
        return self.request.user.conversations.all()

    def delete(self, request, *args, **kwargs):
        conversation = self.get_object()
        conversation.participants.remove(request.user)
        if conversation.participants.count() == 0:
            conversation.delete()
        return HttpResponseRedirect(self.get_success_url())


@login_required
def get_chat_messages(request, room_id):
    conversation = get_object_or_404(
        Conversation, id=room_id, participants=request.user
    )
    messages = conversation.messages.order_by("timestamp").values(
        "content", "sender__username", "timestamp"
    )
    return JsonResponse(
        [
            {
                "content": message["content"],
                "sender": message["sender__username"],
                "timestamp": message["timestamp"].isoformat(),
            }
            for message in messages
        ],
        safe=False,
    )
