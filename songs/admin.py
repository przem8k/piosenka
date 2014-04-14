from songs.models import Song, ArtistContribution, BandContribution
from django.contrib import admin


class ArtistContributionInline(admin.TabularInline):
    model = ArtistContribution
    extra = 1


class BandContributionInline(admin.TabularInline):
    model = BandContribution
    extra = 1


class SongAdmin(admin.ModelAdmin):
    inlines = (ArtistContributionInline, BandContributionInline,)
    prepopulated_fields = {'slug': ['title', 'disambig']}
    fieldsets = [
        ('Identification',
            {'fields': ['title', 'original_title', 'disambig', 'slug', 'published']}),
        ('Content', {'fields': ['capo_fret', 'lyrics', ]}),
        ('Additional',
            {'fields': ['link_youtube', 'link_wrzuta', 'score1', 'score2', 'score3',
                        'related_songs']}),
    ]
    filter_horizontal = ['related_songs']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

admin.site.register(Song, SongAdmin)
