from events.models import Event, Venue, EntityPerformance
from django.contrib import admin


class EntityPerformanceInlineAdmin(admin.TabularInline):
    model = EntityPerformance
    extra = 1


class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}
    fieldsets = [
        ('What', {'fields': ['name', 'slug', 'price', 'description_trevor', 'website']}),
        ('When', {'fields': ['datetime']}),
        ('Where', {'fields': ['venue']}),
    ]
    inlines = (EntityPerformanceInlineAdmin, )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()


class VenueAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name', 'town']}

admin.site.register(Event, EventAdmin)
admin.site.register(Venue, VenueAdmin)
