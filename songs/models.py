from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from artists.models import Artist, Band

def validate_capo_fret(value):
    if value < 0 or value > 11:
        raise ValidationError(u'Capo fret has to be in range [0, 11]')

def validate_lyrics(value):
    try:
        from songs.views import parse_lyrics;
        parse_lyrics(value)
    except SyntaxError, m:
        raise ValidationError(u'Lyrics syntax is incorrect: ' + m)


class Song(models.Model):
    title = models.CharField(max_length=100)
    disambig = models.CharField(max_length=100, null=True,blank=True, help_text="Disambiguation for multiple songs with the same title.")
    original_title = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, help_text="Used in urls, has to be unique.");
    artists = models.ManyToManyField(Artist, null=True,blank=True, through='ArtistContribution')
    bands = models.ManyToManyField(Band, null=True,blank=True, through='BandContribution')
    link_youtube = models.URLField(null=True, blank=True)
    link_wrzuta = models.URLField(null=True, blank=True)
    score1 = models.ImageField(null=True, blank=True, upload_to='scores')
    score2 = models.ImageField(null=True, blank=True, upload_to='scores')
    score3 = models.ImageField(null=True, blank=True, upload_to='scores')
    key = models.CharField(max_length=100, null=True,blank=True, help_text="Deprecated - use capo_fret instead")
    capo_fret = models.IntegerField(default=0, validators=[validate_capo_fret,], help_text="Set to 0 if no capo")
    lyrics = models.TextField(null=True,blank=True)
    lyrics_html_for_display = models.TextField(null=True,blank=True,editable=False)
    lyrics_html_text_only = models.TextField(null=True,blank=True,editable=False)
    lyrics_html_basic_chords = models.TextField(null=True,blank=True,editable=False)
    lyrics_html_all_chords = models.TextField(null=True,blank=True,editable=False)
    lyrics_contain_extra_chords = models.BooleanField(blank=True, editable=False)
    published = models.BooleanField(default=True, help_text="Only admins see not-published songs")
    def save(self, force_insert=False, force_update=False):
        super(Song, self).save(force_insert, force_update)
    def get_absolute_url(self):
        return "/piosenki/%s" % self.slug
    def __unicode__(self):
        return self.title
    class Meta:
        ordering = ["title",]
		
class ArtistContribution(models.Model):
    song = models.ForeignKey(Song)
    artist = models.ForeignKey(Artist)
    performed = models.BooleanField()
    texted = models.BooleanField()
    translated = models.BooleanField()
    composed = models.BooleanField()	
    def __unicode__(self):
        return self.artist.firstname + " " + self.artist.lastname + " - " + self.song.title
    def songid(self):
        return self.song.id
    def songtitle(self):
        return self.song.title
		
class BandContribution(models.Model):
    song = models.ForeignKey(Song)
    band = models.ForeignKey(Band)
    performed = models.BooleanField()	
    def __unicode__(self):
        return self.band.name + " - " + self.song.title
    def songid(self):
        return self.song.id
    def songtitle(self):
        return self.song.title
        
class UserCategory(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    
class UserSubscription(models.Model):
    user = models.ForeignKey(User)
    song = models.ForeignKey(Song)
    category = models.ForeignKey(UserCategory, blank=True, null=True)
