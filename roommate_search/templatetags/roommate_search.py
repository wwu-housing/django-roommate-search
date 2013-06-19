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


@register.simple_tag
def paginator_query_string(page_obj, request, page_arg):
    page_number = None
    if page_arg == "first":
        page_number = page_obj.paginator.page_range[0]
    elif page_arg == "previous":
        page_number = page_obj.previous_page_number()
    elif page_arg == "next":
        page_number = page_obj.next_page_number()
    elif page_arg == "last":
        page_number = page_obj.paginator.num_pages

    query_string = request.GET.copy()

    if page_number:
        query_string["page"] = page_number

    return query_string.urlencode()
