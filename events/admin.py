from events.models import Event, Venue, EntityPerformance
from django.contrib import admin


class EntityPerformanceInlineAdmin(admin.TabularInline):
    model = EntityPerformance
    extra = 1


class EventAdmin(admin.ModelAdmin):
    inlines = (EntityPerformanceInlineAdmin, )


class VenueAdmin(admin.ModelAdmin):
    pass

admin.site.register(Event, EventAdmin)
admin.site.register(Venue, VenueAdmin)
