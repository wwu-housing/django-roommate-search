from django.core.urlresolvers import reverse
from django.template import Library

from ..models import Profile


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


@register.filter
def public_profile_url(user):
    obj = Profile.objects.get(user=user)
    return reverse("roommate_search_public_profile",
                   kwargs={"pk": obj.id})
