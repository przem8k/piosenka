from events.models import Event, ExternalEvent, Venue, Performer
from django.contrib import admin

admin.site.register(Performer)
admin.site.register(Event)
admin.site.register(ExternalEvent)
admin.site.register(Venue)
