from events.models import Event, FbEvent, Venue, Performer
from django.contrib import admin


admin.site.register(Performer)
admin.site.register(Event)
admin.site.register(FbEvent)
admin.site.register(Venue)
