from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView

from views import ProfileView, SearchView


urlpatterns = patterns("",
    url(r"^$", TemplateView.as_view(template_name="roommate_search/index.html"),
        name="roommate_search_index"),
    url(r"^profile/$", ProfileView.as_view(), name="roommate_search_profile"),
    url(r"^search/$", SearchView.as_view(), name="roommate_search_search"),

)
