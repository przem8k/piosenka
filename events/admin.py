from events.models import Event, Venue, EntityPerformance, Performer
from django.contrib import admin


class EntityPerformanceInlineAdmin(admin.TabularInline):
    model = EntityPerformance
    extra = 1


class EventAdmin(admin.ModelAdmin):
    inlines = (EntityPerformanceInlineAdmin, )


class PerformerAdmin(admin.ModelAdmin):
    pass


class VenueAdmin(admin.ModelAdmin):
    pass

admin.site.register(Performer, PerformerAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Venue, VenueAdmin)
