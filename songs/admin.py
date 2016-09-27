from songs.models import (Artist, ArtistNote, Annotation, Song,
                          EntityContribution)
from django.contrib import admin


class EntityContributionInline(admin.TabularInline):
    model = EntityContribution
    extra = 1


class SongAdmin(admin.ModelAdmin):
    inlines = (EntityContributionInline,)


admin.site.register(Artist)
admin.site.register(ArtistNote)
admin.site.register(Annotation)
admin.site.register(Song, SongAdmin)
