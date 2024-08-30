from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 3}),
        }
        help_texts = {
            "content": "댓글 내용을 입력해주세요. (최대 500자)",
        }
        error_messages = {
            "content": {
                "required": "댓글 내용을 입력해주세요.",
            }
        }

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if not content.strip():
            raise forms.ValidationError("댓글 내용을 입력해주세요.")
        return content
