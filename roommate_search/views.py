from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DetailView, TemplateView,
                                  UpdateView)

from forms import ProfileForm
from models import Profile


class GetProfileObject(object):
    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def get_form_class(self):
        return ProfileForm

    def get_success_url(self):
        return reverse("roommate_search_profile")

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Profile.DoesNotExist:
            return redirect(reverse("roommate_search_add_profile"))

        return super(GetProfileObject, self).get(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(GetProfileObject, self).dispatch(request, *args, **kwargs)


class ProfileCreateView(GetProfileObject, CreateView):
    model = Profile

    def get_object(self):
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return None

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        return super(ProfileCreateView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object:
            return redirect(reverse("roommate_search_profile"))

        return super(ProfileCreateView, self).get(request, *args, **kwargs)


class ProfileDetailView(GetProfileObject, DetailView):
    pass


class ProfileUpdateView(GetProfileObject, UpdateView):
    pass


class SearchView(TemplateView):
    """roommate search search view"""

    template_name = "roommate_search/search.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # Redirect a user to the profile page if they don't have a profile
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return redirect(reverse("roommate_search_profile"))

        # Redirect a user to the profile page if they are not looking for a
        # roommate
        if profile.status != "looking":
            return redirect(reverse("roommate_search_profile"))

        return super(SearchView, self).dispatch(*args, **kwargs)
