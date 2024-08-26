from django import forms

from .models import Post, Tag
import re
from django_summernote.widgets import SummernoteWidget


class CustomPostForm(forms.ModelForm):
    content = forms.CharField(
        widget=SummernoteWidget(
            attrs={
                "summernote": {
                    "width": "100%",
                    "height": "400px",
                    "toolbar": [
                        ["style", ["style"]],
                        ["font", ["bold", "underline", "clear"]],
                        ["color", ["color"]],
                        ["para", ["ul", "ol", "paragraph"]],
                        ["table", ["table"]],
                        ["insert", ["link", "picture", "video"]],
                        ["view", ["fullscreen", "codeview", "help"]],
                    ],
                }
            }
        )
    )
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter tags like #travel, #food",
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = Post
        fields = ["title", "content", "category", "head_image", "file_upload", "tags"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "head_image": forms.ClearableFileInput(
                attrs={"class": "form-control-file"}
            ),
            "file_upload": forms.ClearableFileInput(
                attrs={"class": "form-control-file"}
            ),
        }

    def clean_tags(self):
        tag_string = self.cleaned_data.get("tags", "")
        tag_names = re.findall(r"#(\w+)", tag_string)
        return tag_names

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

            tag_names = self.cleaned_data.get("tags", [])
            instance.tags.clear()
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                instance.tags.add(tag)

        return instance
