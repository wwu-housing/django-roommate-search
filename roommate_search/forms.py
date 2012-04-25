from django import forms

from roommate_search.models import Profile


class ProfileAdminForm(forms.ModelForm):
    screen_name = forms.RegexField(max_length=128,
        regex=r"^[\w.@+-]+$",
        help_text="""Required. 128 characters or fewer. Letters, digits and
                  @/./+/-/_ only.""",
        error_messages = {
            "invalid": "This value may contain only letters, numbers and @/./+/-/_ characters."})

    class Meta:
        model = Profile
        widgets = {
            "status": forms.RadioSelect(),
        }


class ProfileForm(ProfileAdminForm):
    """
    Extend the profile admin form, override the Meta class to only include the
    needed fields.
    """
    class Meta:
        model = Profile
        fields = ("screen_name", "bio", "status")
        widgets = {
            "status": forms.RadioSelect(),
        }


class SearchForm(forms.Form):
    q = forms.CharField(label="Bio Search:",
                        max_length=256,
                        required=False)


class FilterForm(forms.Form):
    FILTER_CHOICES = (("starred", "Starred profiles"),)
    filters = forms.MultipleChoiceField(choices=FILTER_CHOICES,
                                        required=False,
                                        widget=forms.CheckboxSelectMultiple)
