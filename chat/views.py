from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction

from .models import Conversation, Message
from .forms import StartConversationForm


class ConversationListView(LoginRequiredMixin, ListView):
    model = Conversation
    template_name = "chat/conversation_list.html"
    context_object_name = "conversations"

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user).order_by(
            "-updated_at"
        )


class ConversationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Conversation
    template_name = "chat/conversation_detail.html"
    context_object_name = "conversation"

    def test_func(self):
        conversation = self.get_object()
        return self.request.user in conversation.participants.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conversation = self.get_object()
        context["messages"] = conversation.messages.order_by("timestamp")
        other_participants = conversation.participants.exclude(id=self.request.user.id)
        context["other_participant"] = (
            other_participants.first() if other_participants.exists() else None
        )
        return context

    def post(self, request, *args, **kwargs):
        conversation = self.get_object()
        content = request.POST.get("content")
        if content:
            message = Message.objects.create(
                conversation=conversation, sender=request.user, content=content
            )
            message.read_by.add(request.user)
        return redirect(self.request.path_info)


class StartConversationView(LoginRequiredMixin, CreateView):
    form_class = StartConversationForm
    template_name = "chat/start_conversation.html"
    success_url = reverse_lazy("chat:conversation_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        participant = form.cleaned_data["participant"]
        conversation = form.save()
        conversation.participants.add(self.request.user, participant)
        return redirect("chat:conversation_detail", pk=conversation.pk)


class ConversationDeleteView(LoginRequiredMixin, DeleteView):
    model = Conversation
    success_url = reverse_lazy("chat:conversation_list")

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)


@login_required
@require_POST
def send_message(request, conversation_id):
    conversation = get_object_or_404(
        Conversation, id=conversation_id, participants=request.user
    )
    content = request.POST.get("content")
    if content:
        message = Message.objects.create(
            conversation=conversation, sender=request.user, content=content
        )
        return JsonResponse(
            {
                "status": "success",
                "message_id": message.id,
                "content": message.content,
                "timestamp": message.timestamp.isoformat(),
                "sender": request.user.username,
            }
        )
    return JsonResponse(
        {"status": "error", "message": "Content is required"}, status=400
    )
