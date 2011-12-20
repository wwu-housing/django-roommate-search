from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from forms import ProfileForm
from models import Profile


class ProfileView(SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    """roommate search profile view"""
    template_name = "roommate_search/profile_detail.html"
    model = Profile

    def get_object(self, request):
        try:
            return Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return None

    def get_form_class(self):
        return ProfileForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(request)
        return super(ProfileView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(request)
        return super(ProfileView, self).post(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileView, self).dispatch(request, *args, **kwargs)


class SearchView(TemplateView):
    """roommate search search view"""

    template_name = "roommate_search/search.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SearchView, self).dispatch(*args, **kwargs)
