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
    search = forms.CharField(label='Search:',
                             initial='bio search',
                             max_length=256)


class FilterForm(forms.Form):
    FILTER_CHOICES = (("starred", "Starred profiles"),)
    #filters = forms.MultipleChoiceField(choices=FILTER_CHOICES)
    filters = forms.ChoiceField(choices=FILTER_CHOICES)
