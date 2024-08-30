from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Message
from .forms import MessageForm
from django.contrib.auth import get_user_model


class InboxView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "direct_messages/inbox.html"
    context_object_name = "messages"

    def get_queryset(self):
        return Message.objects.filter(recipient=self.request.user)


class SendMessageView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "direct_messages/send_message.html"
    success_url = reverse_lazy("direct_messages:inbox")

    def get_initial(self):
        initial = super().get_initial()
        recipient_username = self.request.GET.get("recipient")
        if recipient_username:
            User = get_user_model()
            try:
                recipient = User.objects.get(username=recipient_username)
                initial["recipient"] = recipient
            except User.DoesNotExist:
                pass
        return initial

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "direct_messages/message_detail.html"
    context_object_name = "message"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.is_read and obj.recipient == self.request.user:
            obj.is_read = True
            obj.save()
        return obj

    def get_queryset(self):
        return Message.objects.filter(recipient=self.request.user)
