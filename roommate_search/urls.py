from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from views import (ProfileCreateView, ProfileDetailView, ProfileUpdateView,
                   PublicProfileDetailView, SearchView, StarsView)
from models import Profile


urlpatterns = patterns("",
    # index
    url(r"^$", TemplateView.as_view(template_name="roommate_search/index.html"),
        name="roommate_search_index"),

    # stars
    url(r"^stars/(?P<action>\w+)/(?P<object_id>\d+)/$", StarsView.as_view(), name="roommate_search_stars"),

    # profile
    url(r"^profile/$", ProfileDetailView.as_view(), name="roommate_search_profile"),
    url(r"^profile/(?P<pk>\d+)/$", PublicProfileDetailView.as_view(), name="roommate_search_public_profile"),
    url(r"^profile/add/$", ProfileCreateView.as_view(), name="roommate_search_add_profile"),
    url(r"^profile/edit/$", ProfileUpdateView.as_view(), name="roommate_search_edit_profile"),

    # search
    url(r"^search/$", SearchView.as_view(), name="roommate_search_search"),

    # django-messages
    url(r"^messages/compose/$", "roommate_search.django_messages_override.compose", name="messages_compose"),
    url(r"^messages/compose/(?P<recipient>[\w.@+-]+)/$", "roommate_search.django_messages_override.compose", name="messages_compose_to"),
    url(r"^messages/reply/(?P<message_id>[\d]+)/$", "roommate_search.django_messages_override.reply", name="messages_reply"),
    (r"^messages/", include("django_messages.urls")),
)
