from songs.models import Annotation, Song, EntityContribution
from django.contrib import admin


class EntityContributionInline(admin.TabularInline):
    model = EntityContribution
    extra = 1


class SongAdmin(admin.ModelAdmin):
    inlines = (EntityContributionInline, )

class AnnotationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Annotation, AnnotationAdmin)
admin.site.register(Song, SongAdmin)
