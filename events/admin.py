from events.models import Event, Venue
from django.contrib import admin


class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}
    fieldsets = [
        ('What', {'fields': ['name', 'slug', 'artists', 'bands', 'price', 'description',
                             'description_trevor', 'website']}),
        ('When', {'fields': ['datetime']}),
        ('Where', {'fields': ['venue']}),
    ]
    filter_horizontal = ['artists', 'bands']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()


class VenueAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name', 'town']}

admin.site.register(Event, EventAdmin)
admin.site.register(Venue, VenueAdmin)
