import uuid

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse_lazy
from django.db import models

from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases

from content.models import ContentItem
from content.slug import SlugLogicMixin, SlugFieldMixin
from content.trevor import render_trevor, put_text_in_trevor
from songs.lyrics import contain_extra_chords
from songs.lyrics import parse_lyrics
from songs.transpose import transpose_lyrics

saved_file.connect(generate_aliases)


class Artist(SlugFieldMixin, models.Model):
    HELP_NAME = """Imię i nazwisko wykonawcy lub nazwa zespołu."""
    HELP_FEATURED = """Czy artysta powinien być wyświetlany w spisie treści
śpiewnika."""
    HELP_CATEGORY = """W której części spisu treści artysta ma być wyświetlony.
"""
    CAT_TEXTER = 1
    CAT_COMPOSER = 2
    CAT_FOREIGN = 3
    CAT_BAND = 4
    FEATURED_CATEGORIES = (
        (CAT_TEXTER, 'Wykonawca własnych tekstów'),
        (CAT_COMPOSER, 'Kompozytor'),
        (CAT_FOREIGN, 'Bard zagraniczny'),
        (CAT_BAND, 'Zespół'),
    )

    name = models.CharField(max_length=50, help_text=HELP_NAME)
    featured = models.BooleanField(default=False, help_text=HELP_FEATURED)
    category = models.IntegerField(choices=FEATURED_CATEGORIES, null=True,
                                   blank=True, help_text=HELP_CATEGORY)
    website = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ['name']

    @staticmethod
    def create_for_testing():
        artist = Artist()
        artist.name = str(uuid.uuid4())
        artist.save()
        return artist

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return('view_artist', (), {
            'slug': self.slug,
        })

    # SlugFieldMixin:
    def get_slug_elements(self):
        return [self.name]


def validate_capo_fret(value):
    if value < 0 or value > 11:
        raise ValidationError(u'Capo fret has to be in range [0, 11]')


class Song(SlugLogicMixin, ContentItem):
    CAPO_TO_ROMAN = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX",
                     "X", "XI", "XII"]

    HELP_DISAMBIG = """\
Opcjonalna adnotacja rozróżniająca piosenki o tym samym tytule."""
    HELP_TITLE = """\
Tytuł piosenki."""
    HELP_ORIGINAL_TITLE = """\
Tytuł oryginalnej piosenki w przypadku tłumaczenia, np. 'Mourir pour des \
idées'."""
    HELP_LINK_YOUTUBE = """\
Link do nagrania piosenki w serwisie YouTube."""
    HELP_LINK_WRZUTA = """\
Link do nagrania piosenki w serwisie Wrzuta."""
    HELP_CAPO_FRET = """\
Liczba od 0 do 11, 0 oznacza brak kapodastra."""
    HELP_OLD_SLUG = """\
Old slug kept to maintain redirects."""
    HELP_SLUG = """\
Used in urls, has to be unique."""
    HELP_HAS_EXTRA_CHORDS = """\
True iff the lyrics contain repeated chords."""

    title = models.CharField(
        max_length=100, help_text=HELP_TITLE)
    disambig = models.CharField(
        max_length=100, null=True, blank=True, help_text=HELP_DISAMBIG)
    original_title = models.CharField(
        max_length=100, null=True, blank=True, help_text=HELP_ORIGINAL_TITLE)
    link_youtube = models.URLField(
        null=True, blank=True, help_text=HELP_LINK_YOUTUBE)
    link_wrzuta = models.URLField(
        null=True, blank=True, help_text=HELP_LINK_WRZUTA)
    score1 = models.ImageField(null=True, blank=True, upload_to='scores')
    score2 = models.ImageField(null=True, blank=True, upload_to='scores')
    score3 = models.ImageField(null=True, blank=True, upload_to='scores')
    capo_fret = models.IntegerField(
        default=0, validators=[validate_capo_fret], help_text=HELP_CAPO_FRET)
    lyrics = models.TextField()

    old_slug = models.SlugField(
        max_length=100, unique=True, null=True, blank=True, editable=False,
        help_text=HELP_OLD_SLUG)
    slug = models.SlugField(
        max_length=200, unique=True, null=False, blank=False, editable=False,
        help_text=HELP_SLUG)
    has_extra_chords = models.BooleanField(
        default=False, blank=True, editable=False,
        help_text=HELP_HAS_EXTRA_CHORDS)

    class Meta(ContentItem.Meta):
        ordering = ["title", "disambig"]
        unique_together = ["title", "disambig"]

    @staticmethod
    def create_for_testing(author):
        song = Song()
        song.author = author
        song.title = str(uuid.uuid4()).replace("-", "")
        song.lyrics = "Abc"
        song.save()
        return song

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slug_prepend_elements = []

    def __str__(self):
        if self.disambig:
            return "%s (%s)" % (self.title, self.disambig,)
        else:
            return self.title

    def get_url_params(self):
        return {
            'slug': self.slug
        }

    @staticmethod
    def get_add_url():
        return str(reverse_lazy('add_song'))

    @models.permalink
    def get_absolute_url(self):
        return ('view_song', (), self.get_url_params())

    @models.permalink
    def get_edit_url(self):
        return ('edit_song', (), self.get_url_params())

    @models.permalink
    def get_review_url(self):
        return ('review_song', (), self.get_url_params())

    @models.permalink
    def get_approve_url(self):
        return ('approve_song', (), self.get_url_params())

    @models.permalink
    def get_add_annotation_url(self):
        return ('add_annotation', (), self.get_url_params())

    def clean(self):
        try:
            parsed_lyrics = parse_lyrics(self.lyrics)
            transpose_lyrics(parsed_lyrics, 0)
        except SyntaxError as m:
            raise ValidationError("Lyrics syntax is incorrect: " + str(m))

    def set_slug_prepend_elements(self, elements):
        self.slug_prepend_elements = elements

    # SlugLogicMixin:
    def get_slug_elements(self):
        return self.slug_prepend_elements + [self.title] + ([self.disambig]
                                                            if self.disambig
                                                            else [])

    def save(self, *args, **kwargs):
        self.has_extra_chords = contain_extra_chords(parse_lyrics(self.lyrics))
        super().save(*args, **kwargs)

    def capo(self, transposition=0):
        return Song.CAPO_TO_ROMAN[(self.capo_fret + 12 - transposition) % 12]

    def external_links(self):
        """ returns list of (label, url) describing links associated with the
        song """
        links = []
        if self.link_youtube:
            links.append(("Nagranie (Youtube)", self.link_youtube))
        if self.link_wrzuta:
            links.append(("Nagranie (Wrzuta)", self.link_wrzuta))
        return links

    def text_authors(self):
        return [x.artist for x in
                EntityContribution.objects.filter(song=self, texted=True)]

    def composers(self):
        return [x.artist for x in
                EntityContribution.objects.filter(song=self, composed=True)]

    def translators(self):
        return [x.artist for x in
                EntityContribution.objects.filter(song=self, translated=True)]

    def performers(self):
        return [x.artist for x in
                EntityContribution.objects.filter(song=self, performed=True)]


class EntityContribution(models.Model):
    song = models.ForeignKey(Song)
    artist = models.ForeignKey(Artist, verbose_name='artysta')
    performed = models.BooleanField(default=False, verbose_name="wyk.")
    texted = models.BooleanField(default=False, verbose_name="tekst")
    translated = models.BooleanField(default=False, verbose_name="tł.")
    composed = models.BooleanField(default=False, verbose_name="muz.")

    class Meta:
        unique_together = (('song', 'artist'),)

    def __str__(self):
        return self.entity.__str__() + " - " + self.song.title

    def clean(self):
        if (not self.performed and not self.texted and not self.translated and
                not self.composed):
            raise ValidationError("Zaznacz co najmniej jedną rolę artysty.")

    @staticmethod
    def head_contribution(contributions):
        candidates = ([x for x in contributions if x.texted] +
                      [x for x in contributions if x.performed] +
                      [x for x in contributions if x.composed] +
                      [x for x in contributions if x.translated])
        for cand in candidates:
            if cand.entity.featured:
                return cand
        for cand in candidates:
            return cand
        return None


class Annotation(SlugLogicMixin, ContentItem):
    is_card = True

    HELP_TITLE = """\
Tytuł adnotacji, np. "Aspazja" lub "Fortepian Chopina"."""
    HELP_IMAGE = """\
Ilustracja adnotacji. Pamiętaj o wskazaniu źródła tak samo jak w przypadku
treści zawartych w tekście adnotacji."""
    HELP_SOURCE_URL = """\
Link do źródła informacji, jeśli źródłem jest strona internetowa."""
    HELP_SOURCE_REF = """\
Tytuł i autor publikacji źródłowej, jeśli adnotacja jest oparta na
publikacjii."""
    HELP_SLUG = """\
Used in urls, has to be unique."""

    title = models.CharField(max_length=100, help_text=HELP_TITLE)
    text_trevor = models.TextField()
    image = models.ImageField(null=True, blank=True,
                              upload_to='song_annotations',
                              help_text=HELP_IMAGE)
    source_url1 = models.URLField(null=True, blank=True,
                                  help_text=HELP_SOURCE_URL)
    source_url2 = models.URLField(null=True, blank=True,
                                  help_text=HELP_SOURCE_URL)
    source_ref1 = models.TextField(null=True, blank=True,
                                   help_text=HELP_SOURCE_REF)
    source_ref2 = models.TextField(null=True, blank=True,
                                   help_text=HELP_SOURCE_REF)

    song = models.ForeignKey(Song, editable=False)
    slug = models.SlugField(max_length=200, unique=True, editable=False,
                            help_text=HELP_SLUG)
    text_html = models.TextField(editable=False)

    class Meta(ContentItem.Meta):
        pass

    @staticmethod
    def create_for_testing(author):
        annotation = Annotation()
        annotation.author = author
        annotation.song = Song.create_for_testing(author)
        annotation.song.reviewed = True
        annotation.song.save()
        annotation.title = str(uuid.uuid4()).replace("-", "")
        annotation.text_trevor = put_text_in_trevor("Abc")
        annotation.save()
        return annotation

    def __str__(self):
        return "%s - adnotacja do piosenki %s" % (self.title, self.song.title)

    def get_id(self):
        return self.slug

    def get_url_params(self):
        return {
            'slug': self.slug
        }

    def get_absolute_url(self):
        return self.song.get_absolute_url()

    @models.permalink
    def get_edit_url(self):
        return ('edit_annotation', (), self.get_url_params())

    @models.permalink
    def get_review_url(self):
        return ('review_annotation', (), self.get_url_params())

    @models.permalink
    def get_approve_url(self):
        return ('approve_annotation', (), self.get_url_params())

    # SlugLogicMixin:
    def get_slug_elements(self):
        return [self.title, self.song.slug]

    def save(self, *args, **kwargs):
        self.text_html = render_trevor(self.text_trevor)
        super().save(*args, **kwargs)
