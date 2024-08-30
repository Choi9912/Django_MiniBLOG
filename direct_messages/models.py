from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_direct_messages"
    )

    recipient = models.ForeignKey(
        User, related_name="received_messages", on_delete=models.CASCADE
    )
    subject = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender} to {self.recipient}: {self.subject}"

    class Meta:
        ordering = ["-timestamp"]
