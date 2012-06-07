from events.models import Event, Venue
from django.contrib import admin

class EventAdmin(admin.ModelAdmin):
	prepopulated_fields = { 'slug' : ['name'] }
	fieldsets = [
		('What', 				{'fields': ['name', 'slug', 'artists', 'bands', 'price', 'description', 'website']}),
		('When', 				{'fields': ['datetime',]}),
		('Where', 				{'fields': ['venue']}),
	]

class VenueAdmin(admin.ModelAdmin):
	prepopulated_fields = { 'slug' : ['name', 'town']}
	
admin.site.register(Event, EventAdmin)
admin.site.register(Venue, VenueAdmin)
