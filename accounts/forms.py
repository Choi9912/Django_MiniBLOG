from django import forms
from django.contrib.auth.models import User

from .models import Profile


class ProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    birthday = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), required=False
    )

    class Meta:
        model = Profile
        fields = ["bio", "images", "birthday", "location"]

    def clean_username(self):
        username = self.cleaned_data["username"]
        if (
            User.objects.filter(username=username)
            .exclude(pk=self.instance.user.pk)
            .exists()
        ):
            raise forms.ValidationError("이미 사용 중인 사용자 이름입니다.")
        return username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields["username"].initial = self.instance.user.username

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.username = self.cleaned_data["username"]
        if commit:
            user.save()
            profile.save()
        return profile
