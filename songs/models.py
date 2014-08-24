import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases
from unidecode import unidecode

from artists.models import Entity

saved_file.connect(generate_aliases)


def validate_capo_fret(value):
    if value < 0 or value > 11:
        raise ValidationError(u'Capo fret has to be in range [0, 11]')


class PublishedSongManager(models.Manager):
    def get_queryset(self):
        return super(PublishedSongManager, self).get_queryset().filter(published=True)


class Song(models.Model):
    objects = models.Manager()
    po = PublishedSongManager()

    CAPO_TO_ROMAN = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
    title = models.CharField(max_length=100)
    disambig = models.CharField(max_length=100, null=True, blank=True,
                                help_text="Disambiguation for multiple songs with the same title.")
    original_title = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True,
                            help_text="Old slug, kept to maintain redirects.")
    new_slug = models.SlugField(max_length=200, unique=True, null=True, blank=True,
                                help_text="Used in urls, has to be unique.")
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
    published = models.BooleanField(default=True, help_text="Unpublish instead of deleting.")
    author = models.ForeignKey(User, editable=False)
    date = models.DateTimeField(editable=False)

    class Meta:
        ordering = ["title", "disambig"]

    def __str__(self):
        if self.disambig:
            return "%s (%s)" % (self.title, self.disambig,)
        else:
            return self.title

    @models.permalink
    def get_absolute_url(self):
        return ("song", (), {"song_slug": self.new_slug})

    @models.permalink
    def get_edit_url(self):
        return ('edit_song', (), {"song_slug": self.new_slug})

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
        if not self.date:
            self.date = datetime.datetime.now()
        if not self.new_slug and self.head_entity():
            # We need to save a newly added song before saving the contributions. Hence the slug is
            # not assigned on the first save.
            max_len = Song._meta.get_field('new_slug').max_length
            entity_part = unidecode(self.head_entity().__str__())[:(max_len / 2)]
            song_part = unidecode(self.title + " " + self.disambig)[:(max_len / 2)]
            self.new_slug = slugify(entity_part + " " + song_part)[:max_len]
        super(Song, self).save(*args, **kwargs)

    def capo(self, transposition=0):
        return Song.CAPO_TO_ROMAN[(self.capo_fret + 12 - transposition) % 12]

    def external_links(self):
        """ returns list of (label, url) tuples describing links associated with the song """
        ytpart = [("Nagranie (Youtube)", self.link_youtube, )] if self.link_youtube else []
        wrzutapart = [("Nagranie (Wrzuta)", self.link_wrzuta, )] if self.link_wrzuta else []
        return ytpart + wrzutapart + [
            (x.entity, x.entity.website) for x in
            EntityContribution.objects.filter(song=self).select_related('entity')
            if x.entity.website
        ]

    def text_authors(self):
        return [x.entity for x in EntityContribution.objects.filter(song=self, texted=True)]

    def composers(self):
        return [x.entity for x in EntityContribution.objects.filter(song=self, composed=True)]

    def translators(self):
        return [x.entity for x in EntityContribution.objects.filter(song=self, translated=True)]

    def performers(self):
        return [x.entity for x in EntityContribution.objects.filter(song=self, performed=True)]

    def head_entity(self):
        """ any artist or band associated with the song, used to construct default urls """
        entities = self.text_authors() + self.performers() + self.composers() + self.translators()
        for entity in entities:
            if entity.featured:
                return entity
        if entities:
            return entities[0]
        return None


class EntityContribution(models.Model):
    song = models.ForeignKey(Song)
    entity = models.ForeignKey(Entity, verbose_name="artysta")
    performed = models.BooleanField(verbose_name="wyk.")
    texted = models.BooleanField(verbose_name="tekst")
    translated = models.BooleanField(verbose_name="tł.")
    composed = models.BooleanField(verbose_name="muz.")

    def __str__(self):
        return self.entity.__str__() + " - " + self.song.title
