from artists.models import Artist, Band, Entity
from django.contrib import admin


class ArtistAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['firstname', 'lastname']}
    fieldsets = [
        (None, {'fields': ['firstname', 'lastname', 'slug', 'kind', 'display']}),
        ("Additional", {'fields': ['website']}),
    ]


class BandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}
    fieldsets = [
        (None, {'fields': ['name', 'slug', 'members', 'display']}),
        ("Additional", {'fields': ['website']}),
    ]

class EntityAdmin(admin.ModelAdmin):
    pass

admin.site.register(Artist, ArtistAdmin)
admin.site.register(Band, BandAdmin)
admin.site.register(Entity, EntityAdmin)
