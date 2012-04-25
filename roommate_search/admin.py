from django.contrib import admin

from roommate_search.forms import ProfileAdminForm
from roommate_search.models import Cluster, Profile


admin.site.register(Cluster)

class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm
admin.site.register(Profile, ProfileAdmin)
