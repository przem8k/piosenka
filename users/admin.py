from users.models import Profile
from django.contrib import admin


class ProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'activation_key', ]

admin.site.register(Profile, ProfileAdmin)
