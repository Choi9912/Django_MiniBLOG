from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .models import Conversation
from .forms import StartConversationForm
from . import service


class ConversationListView(LoginRequiredMixin, ListView):
    model = Conversation
    template_name = "chat/conversation_list.html"
    context_object_name = "conversations"

    def get_queryset(self):
        return service.get_user_conversations(self.request.user)


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
        context["messages"], context["other_participant"] = (
            service.get_conversation_details(conversation, self.request.user)
        )
        return context

    def post(self, request, *args, **kwargs):
        conversation = self.get_object()
        content = request.POST.get("content")
        if content:
            service.create_message(conversation, request.user, content)
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
        conversation = service.start_conversation(self.request.user, participant)
        return redirect("chat:conversation_detail", pk=conversation.pk)


class StartConversationWithView(LoginRequiredMixin, View):
    def get(self, request, username):
        conversation = service.get_or_create_conversation(request.user, username)
        return redirect("chat:conversation_detail", pk=conversation.pk)


class ConversationDeleteView(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy("chat:conversation_list")

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def delete(self, request, *args, **kwargs):
        service.delete_conversation(request.user, self.kwargs["pk"])
        return super().delete(request, *args, **kwargs)


@login_required
@require_POST
def send_message(request, conversation_id):
    content = request.POST.get("content")
    message = service.send_message(request.user, conversation_id, content)
    if message:
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
