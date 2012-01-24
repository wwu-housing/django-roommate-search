from django import forms

from models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("screen_name", "bio", "status")
        widgets = {
            "status": forms.RadioSelect(),
        }

