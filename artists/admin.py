from artists.models import Entity
from django.contrib import admin


class EntityAdmin(admin.ModelAdmin):
    pass

admin.site.register(Entity, EntityAdmin)
