from django import forms

from models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("screen_name", "bio", "status")
        widgets = {
            "status": forms.RadioSelect(),
        }


class SearchForm(forms.Form):
    q = forms.CharField(label='Roommate Search:',
                        max_length=256,
                        required=False)


class FilterForm(forms.Form):
    FILTER_CHOICES = (("starred", "Starred profiles"),)
    filters = forms.MultipleChoiceField(choices=FILTER_CHOICES,
                                        required=False,
    )#                                    widget=forms.CheckboxInput)
