from django import forms

from .models import Profile


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
    FILTER_CHOICES = (("starred", "Starred profiles"),("RFR", "New Freshman"), ("RTR", "New Transfer"), ("RR", "Returning Student"), ("RHNC", "Honors Program"), ("RFX", "Fairhaven College"))
    filters = forms.MultipleChoiceField(label="Filter by student status:",
                                        choices=FILTER_CHOICES,
                                        required=False,
                                        widget=forms.CheckboxSelectMultiple)

class RankForm(forms.Form):
    RANK_CHOICES = ((0, "Studying vs Socializing in the room"), (1, "Bedtime on school nights"), (2, "Attitude about alcohol in the room"), (3, "Frequency of visitors in the room"), (4, "Messy, tisy, or in between"),
                    (5, "Tolerance for noise"), (6, "Openness to sharing things"), (7, "Smoking status"))
    choices = forms.MultipleChoiceField(label="Filter by a roommate factor in the housing application:",
                                        choices=RANK_CHOICES,
                                        required=False,
                                        widget=forms.CheckboxSelectMultiple)
