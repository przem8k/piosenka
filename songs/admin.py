from songs.models import Song, ArtistContribution, BandContribution
from django.contrib import admin

class ArtistContributionInline(admin.TabularInline):
	model = ArtistContribution
	extra = 1
	
class BandContributionInline(admin.TabularInline):
	model = BandContribution
	extra = 1

class SongAdmin(admin.ModelAdmin):
	inlines = (ArtistContributionInline,BandContributionInline,)
	prepopulated_fields = { 'slug' : ['title', 'disambig'] }
	fieldsets = [
		('Identification', 				{'fields': ['title', 'original_title', 'disambig', 'slug', 'published']}),
		('Content', 				{'fields': ['capo_fret', 'lyrics',]}),
		('Additional', 				{'fields': ['link_youtube', 'link_wrzuta', 'score1', 'score2', 'score3']}),
	]
	

admin.site.register(Song, SongAdmin)


