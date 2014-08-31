from songs.models import Song, EntityContribution
from django.contrib import admin


class EntityContributionInline(admin.TabularInline):
    model = EntityContribution
    extra = 1


class SongAdmin(admin.ModelAdmin):
    inlines = (EntityContributionInline, )

admin.site.register(Song, SongAdmin)
