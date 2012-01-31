import simplejson

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (CreateView, DetailView, ListView,
    TemplateView, UpdateView)

from forms import (FilterForm, ProfileForm, SearchForm)
from models import Profile


class GetProfileObject(object):
    def get_object(self):
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return None

    def get_search_set(self):
        profile = self.get_object()

        # default filter of profiles
        profile_list = Profile.objects.exclude(user=self.request.user)
        profile_list = profile_list.filter(clusters__in=profile.clusters.all())
        profile_list = profile_list.filter(status="looking")
        return profile_list

    def get_form_class(self):
        return ProfileForm

    def get_success_url(self):
        return reverse("roommate_search_profile")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object:
            messages.info(request, "Please complete your profile.")
            return redirect(reverse("roommate_search_add_profile"))

        return super(GetProfileObject, self).get(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(GetProfileObject, self).dispatch(request, *args, **kwargs)


class ProfileCreateView(GetProfileObject, CreateView):
    model = Profile

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        return super(ProfileCreateView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object:
            return redirect(reverse("roommate_search_edit_profile"))

        return CreateView.get(self, request, *args, **kwargs)


class ProfileDetailView(GetProfileObject, DetailView):
    pass


# TODO: make PublicProfileDetailView to limit a user to viewing search set
# profiles.
class PublicProfileDetailView(DetailView):
    model = Profile

    def get_context_data(self, **kwargs):
        context = super(PublicProfileDetailView, self).get_context_data(**kwargs)

        # determine if the user has this profile starred
        profile = Profile.objects.get(user=self.request.user)
        starred = profile.stars.filter(id=self.get_object().id)

        context["starred"] = starred
        return context


class ProfileUpdateView(GetProfileObject, UpdateView):
    pass


class SearchView(GetProfileObject, ListView):
    def get_search_form(self):
        get_data = self.request.GET or None
        return SearchForm(get_data)

    def get_filter_form(self):
        get_data = self.request.GET or None
        return FilterForm(get_data)

    def get_queryset(self):
        queryset = self.get_search_set()
        search_form = self.get_search_form()
        if search_form.is_valid():
            search_query = search_form.cleaned_data.get("q")
            if search_query:
                search_words = search_query.split(" ")
                query = None
                for word in search_words:
                    if not query:
                        query = Q(bio__icontains=word)
                    else:
                        query |= Q(bio__icontains=word)
                if query:
                    queryset = queryset.filter(query)

        profile = self.get_object()
        filter_form = self.get_filter_form()
        if filter_form.is_valid():
            filters = filter_form.cleaned_data.get("filters")
            if "starred" in filters:
                queryset = queryset & profile.stars.all()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        profile = self.get_object()
        context["starred"] = profile.stars.all()
        context["search_form"] = self.get_search_form()
        context["filter_form"] = self.get_filter_form()
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        profile = self.get_object()
        # Redirect a user to the profile page if they don't have a profile
        if not profile:
            messages.error(request, "To search for a roommate, you must complete your profile.")
            return redirect(reverse("roommate_search_add_profile"))
        # Redirect a user to the profile page if they are not looking for a
        # roommate
        elif profile.status != "looking":
            messages.error(request, "To search for a roommate, you must choose \"Looking for a roommate\" as your status.")
            return redirect(reverse("roommate_search_edit_profile"))

        return super(SearchView, self).dispatch(request, *args, **kwargs)


class StarsView(GetProfileObject, TemplateView):
    def get(self, request, action, object_id, *args, **kwargs):
        if not (action == "add" or action == "remove"):
            return HttpResponseForbidden()

        target_profile = get_object_or_404(Profile, id=int(object_id))
        user_profile = self.get_object()
        if target_profile not in self.get_search_set().all():
            raise Http404()
        else:
            # Do actual add/remove
            getattr(user_profile.stars, action)(target_profile)

            if request.is_ajax():
                return HttpResponse(simplejson.dumps({"message": "Success"}),
                                    mimetype="application/json")
            else:
                return redirect(reverse("roommate_search_public_profile",
                                        kwargs={"pk": object_id}))

        # never called
        #return super(StarsView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(StarsView, self).dispatch(request, *args, **kwargs)
