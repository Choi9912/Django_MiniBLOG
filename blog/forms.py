from django import forms
from .models import Post, Profile, Tag
import re


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "profile_picture", "birth_date", "location"]

    birth_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    location = forms.CharField(max_length=100, required=False)


class CustomPostForm(forms.ModelForm):
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
        widget = (forms.SelectMultiple(attrs={"class": "form-control"}),)

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
