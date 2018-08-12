from django.contrib import admin

from songs.models import Artist, ArtistNote, EntityContribution, Song, SongNote


class EntityContributionInline(admin.TabularInline):
    model = EntityContribution
    extra = 1


class SongAdmin(admin.ModelAdmin):
    inlines = (EntityContributionInline,)


admin.site.register(Artist)
admin.site.register(ArtistNote)
admin.site.register(Song, SongAdmin)
admin.site.register(SongNote)
