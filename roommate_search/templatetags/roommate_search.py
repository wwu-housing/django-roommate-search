from ..models import Profile
from django.template import Library


register = Library()

@register.filter
def screen_name(user):
    """
    A filter for getting the screen name of a user in a template.

    {{ request.user|screen_name }}
    """
    try:
        profile = Profile.objects.get(user=user)
        return profile.screen_name
    except Profile.DoesNotExist:
        return "(Unknown)"
