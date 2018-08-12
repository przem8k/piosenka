from django.contrib import admin

from events.models import ExternalEvent, Performer

admin.site.register(Performer)
admin.site.register(ExternalEvent)
