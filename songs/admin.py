from songs.models import Song, ArtistContribution, BandContribution
from songs.models import Translation, ArtistContributionToTranslation, BandContributionToTranslation
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
        ('Identification',              {'fields': ['title', 'original_title', 'disambig', 'slug', 'published']}),
        ('Content',                 {'fields': ['capo_fret', 'lyrics', ]}),
        ('Additional',              {'fields': ['link_youtube', 'link_wrzuta', 'score1', 'score2', 'score3']}),
    ]

admin.site.register(Song, SongAdmin)


class ArtistContributionToTranslationInline(admin.TabularInline):
    model = ArtistContributionToTranslation
    extra = 1


class BandContributionToTranslationInline(admin.TabularInline):
    model = BandContributionToTranslation
    extra = 1


class TranslationAdmin(admin.ModelAdmin):
    inlines = (ArtistContributionToTranslationInline, BandContributionToTranslationInline,)
    fieldsets = [
        ('Identification',          {'fields': ['title', 'original_song']}),
        ('Content',                 {'fields': ['capo_fret', 'lyrics', ]}),
        ('Additional',              {'fields': ['link_youtube', 'link_wrzuta', 'score1', 'score2', 'score3']}),
    ]

admin.site.register(Translation, TranslationAdmin)
