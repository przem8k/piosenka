import uuid

from django import urls
from django.core.exceptions import ValidationError
from django.db import models
from easy_thumbnails.signal_handlers import generate_aliases
from easy_thumbnails.signals import saved_file

from base.overrides import overrides
from content import url_scheme
from content.models import ContentItem, Note
from content.slug import SlugFieldMixin, SlugLogicMixin
from content.trevor import put_text_in_trevor
from songs.lyrics import parse_lyrics
from songs.transpose import transpose_lyrics

saved_file.connect(generate_aliases)


class Artist(SlugFieldMixin):
    HELP_NAME = "Imię i nazwisko wykonawcy lub nazwa zespołu."
    HELP_FEATURED = "Czy podmiot ma figurować w spisie treści."
    HELP_EPIGONE = "Czy podmiot ma osobną listę piosenek epigońskich."
    HELP_CATEGORY = "Kategoria w spisie treści śpiewnika."
    HELP_WEBSITE = "Strona internetowa artysty."
    HELP_IMAGE = "Ilustracja - zdjęcie artysty."
    HELP_IMAGE_URL = "Źródło zdjęcia (adres www)."
    HELP_IMAGE_AUTHOR = "Źródło zdjęcia (autor)."
    HELP_DESCRIPTION = "Krótki opis podmiotu w stylu encyklopedycznym."
    HELP_BORN_ON = "Data urodzin."
    HELP_DIED_ON = "Data śmierci."
    HELP_COVER_NOTE = "Notka której ilustracja może służyć za okładkę."

    CAT_TEXTER = 1
    CAT_COMPOSER = 2
    CAT_FOREIGN = 3
    CAT_BAND = 4
    CAT_POLISH = 5
    CAT_COMMUNITY = 6
    FEATURED_CATEGORIES = (
        (CAT_TEXTER, "(deprecated) Wykonawca własnych tekstów"),
        (CAT_COMPOSER, "(deprecated) Kompozytor"),
        (CAT_FOREIGN, "Twórca zagraniczny"),
        (CAT_BAND, "(deprecated) Zespół"),
        (CAT_POLISH, "Twórca polski"),
        (CAT_COMMUNITY, "Środowisko"),
    )

    name = models.CharField(max_length=50, help_text=HELP_NAME)
    featured = models.BooleanField(default=False, help_text=HELP_FEATURED)
    epigone = models.BooleanField(default=False, help_text=HELP_EPIGONE)
    category = models.IntegerField(
        choices=FEATURED_CATEGORIES, null=True, blank=True, help_text=HELP_CATEGORY
    )
    website = models.URLField(null=True, blank=True, help_text=HELP_WEBSITE)
    born_on = models.DateField(blank=True, null=True, help_text=HELP_BORN_ON)
    died_on = models.DateField(blank=True, null=True, help_text=HELP_DIED_ON)
    cover_note = models.ForeignKey(
        "ArtistNote",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="artists_covered",
        help_text=HELP_COVER_NOTE,
    )

    class Meta:
        ordering = ["name"]

    @staticmethod
    def create_for_testing(author):
        artist = Artist()
        artist.author = author
        artist.name = str(uuid.uuid4())
        artist.full_clean()
        artist.save()
        return artist

    def __str__(self):
        return self.name

    def get_url_params(self):
        return {"slug": self.slug}

    def get_absolute_url(self):
        return urls.reverse("view_artist", kwargs=self.get_url_params())

    def get_edit_url(self):
        return urls.reverse("edit_artist", kwargs=self.get_url_params())

    def get_add_note_url(self):
        return urls.reverse("add_artist_note", kwargs=self.get_url_params())

    @overrides(SlugFieldMixin)
    def get_slug_elements(self):
        return [self.name]


class ArtistNote(url_scheme.EditReviewApprove, Note):
    artist = models.ForeignKey(Artist, blank=True, on_delete=models.CASCADE)

    class Meta(ContentItem.Meta):
        pass

    @staticmethod
    def create_for_testing(author):
        note = ArtistNote()
        note.author = author
        note.artist = Artist.create_for_testing(author)
        note.artist.featured = True
        note.artist.save()
        note.title = str(uuid.uuid4()).replace("-", "")
        note.text_trevor = put_text_in_trevor("Abc")
        note.full_clean()
        note.save()
        return note

    def get_url_params(self):
        return {"slug": self.slug}

    @overrides(url_scheme.EditReviewApprove)
    def get_url_name(self):
        return "artist_note"

    def get_parent(self):
        return self.artist


def validate_capo_fret(value):
    if value < 0 or value > 11:
        raise ValidationError(u"Capo fret has to be in range [0, 11]")


class Song(SlugLogicMixin, url_scheme.ViewEditReviewApprove, ContentItem):
    CAPO_TO_ROMAN = [
        "",
        "I",
        "II",
        "III",
        "IV",
        "V",
        "VI",
        "VII",
        "VIII",
        "IX",
        "X",
        "XI",
        "XII",
    ]

    HELP_DISAMBIG = "Adnotacja rozróżniająca piosenki o tym samym tytule."
    HELP_TITLE = "Tytuł piosenki."
    HELP_EPIGONE = "Czy piosenka jest kompozycją epigońską, bez porozumienia z autorem tekstu."
    HELP_ORIGINAL_TITLE = "Tytuł oryginalnej piosenki w przypadku tłumaczenia."
    HELP_LINK_YOUTUBE = "Link do nagrania piosenki w serwisie YouTube."
    HELP_CAPO_FRET = "Liczba od 0 do 11, 0 oznacza brak kapodastra."
    HELP_SLUG = "Used in urls, has to be unique."
    HELP_HAS_EXTRA_CHORDS = "True iff the lyrics contain repeated chords."

    title = models.CharField(max_length=100, help_text=HELP_TITLE)
    disambig = models.CharField(
        max_length=100, null=True, blank=True, help_text=HELP_DISAMBIG
    )
    original_title = models.CharField(
        max_length=100, null=True, blank=True, help_text=HELP_ORIGINAL_TITLE
    )
    epigone = models.BooleanField(default=False, help_text=HELP_EPIGONE)
    link_youtube = models.URLField(null=True, blank=True, help_text=HELP_LINK_YOUTUBE)
    score1 = models.ImageField(null=True, blank=True, upload_to="scores")
    score2 = models.ImageField(null=True, blank=True, upload_to="scores")
    score3 = models.ImageField(null=True, blank=True, upload_to="scores")
    capo_fret = models.IntegerField(
        default=0, validators=[validate_capo_fret], help_text=HELP_CAPO_FRET
    )
    lyrics = models.TextField()
    # This is a bit of a hack - this field is set in the creation view
    # so that the head artist name is part of the slug.
    artist_for_slug = models.CharField(max_length=100, null=False, blank=True)

    slug = models.SlugField(
        max_length=200,
        unique=True,
        null=False,
        blank=False,
        editable=False,
        help_text=HELP_SLUG,
    )
    # unused now, to be deleted
    has_extra_chords = models.BooleanField(
        default=False, blank=True, editable=False, help_text=HELP_HAS_EXTRA_CHORDS
    )

    class Meta(ContentItem.Meta):
        ordering = ["title", "disambig"]
        unique_together = ["title", "disambig"]

    @staticmethod
    def create_for_testing(author):
        song = Song()
        song.author = author
        song.title = str(uuid.uuid4()).replace("-", "")
        song.lyrics = "Abc"
        song.full_clean()
        song.save()
        return song

    def __str__(self):
        if self.disambig:
            return "%s (%s)" % (self.title, self.disambig,)
        else:
            return self.title

    def get_url_params(self):
        return {"slug": self.slug}

    def get_add_note_url(self):
        if not self.reviewed:
            return None
        return urls.reverse("add_song_note", kwargs=self.get_url_params())

    def clean(self):
        try:
            parsed_lyrics = parse_lyrics(self.lyrics)
            transpose_lyrics(parsed_lyrics, 0)
        except SyntaxError as m:
            raise ValidationError("Niepoprawny format treści piosenki: " + str(m))
        return super().clean()

    @overrides(SlugLogicMixin)
    def get_slug_elements(self):
        return [self.artist_for_slug, self.title] + (
            [self.disambig] if self.disambig else []
        )

    @overrides(url_scheme.ViewEditReviewApprove)
    def get_url_name(self):
        return "song"

    def capo(self, transposition=0):
        return Song.CAPO_TO_ROMAN[(self.capo_fret + 12 - transposition) % 12]

    def youtube_id(self):
        YT_ID_PATTERN = "watch?v="
        if not self.link_youtube or self.link_youtube.find(YT_ID_PATTERN) < 0:
            return None
        url = self.link_youtube
        return url[url.find(YT_ID_PATTERN) + len(YT_ID_PATTERN) :]

    def set_youtube_id(self, yt_id):
        self.link_youtube = "https://www.youtube.com/watch?v=" + yt_id

    def text_authors(self):
        return [
            x.artist for x in EntityContribution.objects.filter(song=self, texted=True)
        ]

    def composers(self):
        return [
            x.artist
            for x in EntityContribution.objects.filter(song=self, composed=True)
        ]

    def translators(self):
        return [
            x.artist
            for x in EntityContribution.objects.filter(song=self, translated=True)
        ]

    def performers(self):
        return [
            x.artist
            for x in EntityContribution.objects.filter(song=self, performed=True)
        ]


class EntityContribution(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, verbose_name="artysta")
    performed = models.BooleanField(default=False, verbose_name="wyk.")
    texted = models.BooleanField(default=False, verbose_name="tekst")
    translated = models.BooleanField(default=False, verbose_name="tł.")
    composed = models.BooleanField(default=False, verbose_name="muz.")

    class Meta:
        unique_together = (("song", "artist"),)

    def __str__(self):
        return self.artist.__str__() + " - " + self.song.title

    def clean(self):
        if (
            not self.performed
            and not self.texted
            and not self.translated
            and not self.composed
        ):
            raise ValidationError("Zaznacz co najmniej jedną rolę artysty.")

    @staticmethod
    def head_contribution(contributions):
        candidates = (
            [x for x in contributions if x.texted]
            + [x for x in contributions if x.performed]
            + [x for x in contributions if x.composed]
            + [x for x in contributions if x.translated]
        )
        for cand in candidates:
            if cand.artist.featured:
                return cand
        for cand in candidates:
            return cand
        return None


class SongNote(url_scheme.EditReviewApprove, Note):
    HELP_DATE = "Data wydarzenia, do którego odnosi się notka"
    HELP_DATE_DESCRIPTION = "Opis wydarzenia, do którego odnosi się notka"
    song = models.ForeignKey(Song, blank=True, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True, help_text=HELP_DATE)
    date_description = models.CharField(
        null=True, blank=True, max_length=100, help_text=HELP_DATE_DESCRIPTION
    )

    class Meta(ContentItem.Meta):
        pass

    @staticmethod
    def create_for_testing(author):
        note = SongNote()
        note.author = author
        note.song = Song.create_for_testing(author)
        note.song.reviewed = True
        note.song.save()
        note.title = str(uuid.uuid4()).replace("-", "")
        note.text_trevor = put_text_in_trevor("Abc")
        note.full_clean()
        note.save()
        return note

    def get_url_params(self):
        return {"slug": self.slug}

    @overrides(url_scheme.EditReviewApprove)
    def get_url_name(self):
        return "song_note"

    def get_parent(self):
        return self.song
