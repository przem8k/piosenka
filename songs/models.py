from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases

from artists.models import Artist, Band

saved_file.connect(generate_aliases)


def validate_capo_fret(value):
    if value < 0 or value > 11:
        raise ValidationError(u'Capo fret has to be in range [0, 11]')


class Song(models.Model):
    CAPO_TO_ROMAN = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
    title = models.CharField(max_length=100)
    disambig = models.CharField(max_length=100, null=True, blank=True,
                                help_text="Disambiguation for multiple songs with the same title.")
    original_title = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True,
                            help_text="Used in urls, has to be unique.")
    artists = models.ManyToManyField(Artist, null=True, blank=True, through='ArtistContribution')
    bands = models.ManyToManyField(Band, null=True, blank=True, through='BandContribution')
    link_youtube = models.URLField(null=True, blank=True)
    link_wrzuta = models.URLField(null=True, blank=True)
    score1 = models.ImageField(null=True, blank=True, upload_to='scores')
    score2 = models.ImageField(null=True, blank=True, upload_to='scores')
    score3 = models.ImageField(null=True, blank=True, upload_to='scores')
    key = models.CharField(max_length=100, null=True, blank=True,
                           help_text="Deprecated - use capo_fret instead", editable=False)
    capo_fret = models.IntegerField(default=0, validators=[validate_capo_fret],
                                    help_text="Set to 0 if no capo")
    lyrics = models.TextField(null=True)
    has_extra_chords = models.BooleanField(blank=True, editable=False,
                                           help_text="True iff the lyrics contain repeated chords.")
    published = models.BooleanField(default=True, help_text="Only admins see not-published songs")
    related_songs = models.ManyToManyField("self", null=True, blank=True, symmetrical=True,
                                           help_text="E.g. different translations or different "
                                                     "compositions of the same text.")
    author = models.ForeignKey(User, null=True, editable=False)
    date = models.DateTimeField(null=True, editable=False)

    class Meta:
        ordering = ["title", "disambig"]

    def __str__(self):
        if self.disambig:
            return "%s (%s)" % (self.title, self.disambig,)
        else:
            return self.title

    @models.permalink
    def get_absolute_url(self):
        """ each Song object may have multiple absolute urls, each for every contributing entity
            this method returns one of them """
        return ("song", (), {"artist_slug": self.head_entity().slug, "song_slug": self.slug})

    @models.permalink
    def get_absolute_url_print(self):
        return ("song-print", (), {"artist_slug": self.head_entity().slug, "song_slug": self.slug})

    def clean(self):
        try:
            from songs.lyrics import parse_lyrics
            from songs.lyrics import contain_extra_chords
            from songs.transpose import transpose_lyrics
            parsed_lyrics = parse_lyrics(self.lyrics)
            transpose_lyrics(parsed_lyrics, 0)
        except SyntaxError as m:
            raise ValidationError(u'Lyrics syntax is incorrect: ' + str(m))
        self.has_extra_chords = contain_extra_chords(parsed_lyrics)

    def save(self, *args, **kwargs):
        if not self.date and self.published:
            self.date = datetime.datetime.now()
        super(Song, self).save(*args, **kwargs)

    def capo(self, transposition=0):
        return Song.CAPO_TO_ROMAN[(self.capo_fret + 12 - transposition) % 12]

    def external_links(self):
        """ returns list of (label, url) tuples describing links associated with the song """
        ytpart = [("Nagranie (Youtube)", self.link_youtube, )] if self.link_youtube else []
        wrzutapart = [("Nagranie (Wrzuta)", self.link_wrzuta, )] if self.link_wrzuta else []
        return ytpart + wrzutapart + [
            (x.artist, x.artist.website) for x in
            ArtistContribution.objects.filter(song=self).select_related('artist') if
            x.artist.website is not None and len(x.artist.website) > 0
        ] + [
            (x.band, x.band.website) for x in
            BandContribution.objects.filter(song=self).select_related('band') if
            x.band.website is not None and len(x.band.website) > 0
        ]

    def text_authors(self):
        return [x.artist for x in ArtistContribution.objects.filter(song=self, texted=True)]

    def composers(self):
        return [x.artist for x in ArtistContribution.objects.filter(song=self, composed=True)]

    def translators(self):
        return [x.artist for x in ArtistContribution.objects.filter(song=self, translated=True)]

    def performers(self):
        return [
            x.artist for x in ArtistContribution.objects.filter(song=self, performed=True)
        ] + [
            x.band for x in BandContribution.objects.filter(song=self, performed=True)
        ]

    def head_entity(self):
        """ any artist or band associated with the song, used to construct default urls """
        try:
            return (self.performers() + self.text_authors())[0]
        except IndexError:
            return None


class ArtistContribution(models.Model):
    song = models.ForeignKey(Song)
    artist = models.ForeignKey(Artist)
    performed = models.BooleanField()
    texted = models.BooleanField()
    translated = models.BooleanField()
    composed = models.BooleanField()

    def __str__(self):
        return self.artist.firstname + " " + self.artist.lastname + " - " + self.song.title


class BandContribution(models.Model):
    song = models.ForeignKey(Song)
    band = models.ForeignKey(Band)
    performed = models.BooleanField()

    def __str__(self):
        return self.band.name + " - " + self.song.title
