from django.contrib import admin

from .forms import ProfileAdminForm
from .models import Cluster, Profile


admin.site.register(Cluster)

class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm
admin.site.register(Profile, ProfileAdmin)
