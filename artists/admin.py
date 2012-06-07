from artists.models import Artist, Band
from django.contrib import admin

class ArtistAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ['firstname', 'lastname'] }
    fieldsets = [
        (None, 				{'fields': ['firstname', 'lastname','slug', 'display']}),
        ("Additional", 				{'fields': ['website']}),
    ]
	
class BandAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ['name'] }
    fieldsets = [
        (None, 				{'fields': ['name', 'slug', 'members', 'display']}),
        ("Additional", 				{'fields': ['website']}),
    ]

admin.site.register(Artist, ArtistAdmin)
admin.site.register(Band, BandAdmin)
