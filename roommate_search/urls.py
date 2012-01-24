from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, TemplateView

from views import (ProfileCreateView, ProfileDetailView, ProfileUpdateView,
                   SearchView)


urlpatterns = patterns("",
    # index
    url(r"^$", TemplateView.as_view(template_name="roommate_search/index.html"),
        name="roommate_search_index"),

    # profile
    url(r"^profile/$", ProfileDetailView.as_view(), name="roommate_search_profile"),

    # TODO: make PublicProfileDetailView to limit a user to viewing search set profiles.
    url(r"^profile/(?P<pk>\d+)/$", DetailView.as_view(model=Profile), name="roommate_search_public_profile"),
    url(r"^profile/add/$", ProfileCreateView.as_view(), name="roommate_search_add_profile"),
    url(r"^profile/edit/$", ProfileUpdateView.as_view(), name="roommate_search_edit_profile"),

    # search
    url(r"^search/$", SearchView.as_view(), name="roommate_search_search"),

    # django-messages
    (r"^messages/", include("django_messages.urls")),
)
