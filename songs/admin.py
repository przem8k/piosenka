from songs.models import Song, EntityContribution
from django.contrib import admin


class EntityContributionInline(admin.TabularInline):
    model = EntityContribution
    extra = 1


class SongAdmin(admin.ModelAdmin):
    inlines = (EntityContributionInline, )
    prepopulated_fields = {'slug': ['title', 'disambig']}
    fieldsets = [
        ('Identification',
            {'fields': ['title', 'original_title', 'disambig', 'slug', 'new_slug', 'published']}),
        ('Content', {'fields': ['capo_fret', 'lyrics', ]}),
        ('Additional',
            {'fields': ['link_youtube', 'link_wrzuta', 'score1', 'score2', 'score3', ]}),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

admin.site.register(Song, SongAdmin)
