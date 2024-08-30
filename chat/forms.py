from django import forms
from django.contrib.auth import get_user_model
from .models import Conversation

User = get_user_model()


class StartConversationForm(forms.ModelForm):
    participant = forms.ModelChoiceField(
        queryset=User.objects.none(), label="대화 상대"
    )

    class Meta:
        model = Conversation
        fields = []

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["participant"].queryset = User.objects.exclude(id=user.id)
