from django import forms
from .models import Post, Profile, Tag


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "profile_photo"]


class CustomPostForm(forms.ModelForm):
    tags_input = forms.CharField(
        label="Tags",
        widget=forms.TextInput(attrs={"placeholder": "Enter tags separated by commas"}),
    )

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "category",
            "head_image",
            "file_upload",
            "tags_input",
        ]

    def clean_tags_input(self):
        tags_input = self.cleaned_data.get("tags_input", "")
        tag_names = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
        return tag_names

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

            tag_names = self.cleaned_data.get("tags_input", [])
            instance.tags.clear()
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                instance.tags.add(tag)

        return instance
