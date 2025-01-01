import json
import logging

from django.contrib import messages
from django.db.models import Count, Exists, OuterRef
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView

from articles.models import SongMention
from content.models import filter_visible_to_user
from content.views import (AddContentView, ApproveContentView, EditContentView,
                           ReviewContentView, ViewContentView)
from songs import forms
from songs.lyrics import render_lyrics
from songs.models import Artist, ArtistNote, EntityContribution, Song, SongNote

INITIAL_LYRICS = """\
#zw
Pierwszy wers zwrotki [C G F E]
Drugi wers zwrotki [a C]
Trzeci wers zwrotki [a C]
Czwarty wers zwrotki [F E]

#ref
>Obława, obława, na młode wilki obława [a C G C]
>Te dzikie, zapalczywe, w gęstym lesie wychowane [F E]
>Krąg w śniegu wydeptany, w tym kręgu plama krwawa [a C G C]
>Ciała wilcze kłami gończych psów szarpane! [F E]

@zw
Druga zwrotka o tych samych akordach
Co pierwsza zwrotka
Kolejny wers, kolejny wers
I jeszcze jeden i jeszcze raz
"""


class GetSongMixin:
    def get_object(self):
        return get_object_or_404(Song, slug=self.kwargs["slug"])


class GetArtistMixin:
    def get_object(self):
        return get_object_or_404(Artist, slug=self.kwargs["slug"])


class SongbookMenuMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["foreign"] = Artist.objects.filter(
            featured=True, category=Artist.CAT_FOREIGN
        )
        context["polish"] = Artist.objects.filter(
            featured=True, category=Artist.CAT_POLISH
        )
        context["community"] = Artist.objects.filter(
            featured=True, category=Artist.CAT_COMMUNITY
        )
        return context


class IndexView(SongbookMenuMixin, TemplateView):
    template_name = "songs/index.html"
    HERO_ARTIST_COUNT = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hero_artists = (
            Artist.objects.filter(cover_note__isnull=False, cover_note__reviewed=True)
            .exclude(cover_note__image="")
            .annotate(num_songs=Count("entitycontribution"))
            .order_by("-num_songs")[: IndexView.HERO_ARTIST_COUNT]
        )
        context["hero_artists"] = hero_artists
        return context


class CalendarView(TemplateView):
    template_name = "songs/calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notes = (
            filter_visible_to_user(SongNote.objects.all(), self.request.user)
            .filter(date__isnull=False)
            .exclude(date_description="")
            .exclude(image="")
            .order_by("-date")
        )
        context["notes"] = notes
        return context


class ViewArtist(GetArtistMixin, SongbookMenuMixin, DetailView):
    """Lists the songs associated with the given artist."""

    model = Artist
    context_object_name = "artist"
    template_name = "songs/artist.html"

    def dispatch(self, *args, **kwargs):
        artist = self.get_object()
        if not artist.featured and not self.request.user.is_authenticated:
            return HttpResponsePermanentRedirect(reverse("songbook"))
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        artist = self.get_object()
        relevant_contributions = EntityContribution.objects.filter(
            song=OuterRef("pk"), artist=artist
        )
        songs = (
            filter_visible_to_user(Song.objects.all(), self.request.user)
            .annotate(relevant=Exists(relevant_contributions))
            .filter(relevant=True)
            .annotate(num_notes=Count("songnote"))
            .order_by("title")
        )
        if artist.epigone:
            songs = songs.filter().filter(epigone=False)
        context = super().get_context_data(**kwargs)
        context["songs"] = songs
        if artist.epigone:
            context["epigone_songs"] = (
                filter_visible_to_user(Song.objects.all(), self.request.user)
                .annotate(relevant=Exists(relevant_contributions))
                .filter(relevant=True)
                .filter(epigone=True)
                .annotate(num_notes=Count("songnote"))
                .order_by("title")
            )
        context["artist"] = artist
        context["notes"] = ArtistNote.items_visible_to(self.request.user).filter(
            artist=self.object
        )
        return context


class AddArtist(CreateView):
    model = Artist
    form_class = forms.ArtistForm
    template_name = "songs/add_edit_artist.html"

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        ret = super().form_valid(form)
        messages.add_message(self.request, messages.INFO, "Artysta dodany.")
        logging.info("%s added artist %s" % (self.request.user, form.instance))
        return ret


class EditArtist(GetArtistMixin, UpdateView):
    model = Artist
    form_class = forms.ArtistForm
    template_name = "songs/add_edit_artist.html"

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        ret = super().form_valid(form)
        messages.add_message(self.request, messages.INFO, "Zmiany zostały zapisane.")
        logging.info("%s edited artist %s" % (self.request.user, form.instance))
        return ret


class ViewSong(GetSongMixin, ViewContentView):
    """Displays a song by default, returns transposed lyrics part in json if
    asked."""

    model = Song
    context_object_name = "song"
    template_name = "songs/song.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "transposition" in self.kwargs:
            context["json"] = True
            transposition = int(self.kwargs["transposition"])
            context["transposition"] = transposition
        else:
            transposition = 0
        context["lyrics"] = render_lyrics(self.object.lyrics, transposition)
        context["notes"] = SongNote.items_visible_to(self.request.user).filter(
            song=self.object
        )
        context["mentions"] = SongMention.objects.filter(song=self.object)
        return context

    def render_to_response(self, context):
        if context.get("json"):
            return self.get_lyrics_as_json(context)
        return super().render_to_response(context)

    def get_lyrics_as_json(self, context):
        payload = {
            "lyrics": context["lyrics"],
            "transposition": context["transposition"],
        }
        return HttpResponse(json.dumps(payload), content_type="application/json")


class ContributionFormsetMixin:
    """Manages inline formset of song contributions."""

    def dispatch(self, *args, **kwargs):
        if self.request.method == "POST":
            self.formset = forms.ContributionFormSet(
                self.request.POST, instance=self.get_object()
            )
        else:
            self.formset = forms.ContributionFormSet(instance=self.get_object())
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entitycontribution"] = self.formset
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        formset = self.formset

        # This updates |instance| fields in the formset with parsed objects.
        if not formset.is_valid():
            return self.form_invalid(form)

        # Pick head contribution to put into the slug.
        head = EntityContribution.head_contribution([x.instance for x in self.formset])
        assert head
        form.set_artist_for_slug(head.artist.__str__())

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        ret = super().form_valid(form)
        self.formset.instance = form.instance
        self.formset.save()
        return ret


class AddSong(ContributionFormsetMixin, AddContentView):
    model = Song
    form_class = forms.SongForm
    template_name = "songs/add_edit_song.html"

    def get_initial(self):
        return {"lyrics": INITIAL_LYRICS}

    def get_success_url(self):
        return self.object.get_absolute_url()


class EditSong(GetSongMixin, ContributionFormsetMixin, EditContentView):
    model = Song
    form_class = forms.SongForm
    template_name = "songs/add_edit_song.html"

    def get_success_url(self):
        return self.object.get_absolute_url()


class ReviewSong(GetSongMixin, ReviewContentView):
    pass


class ApproveSong(GetSongMixin, ApproveContentView):
    pass


class AddArtistNote(AddContentView):
    model = ArtistNote
    form_class = forms.ArtistNoteForm
    template_name = "songs/add_edit_artist_note.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.artist = None

    def dispatch(self, *args, **kwargs):
        self.artist = get_object_or_404(Artist, slug=self.kwargs["slug"])
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["artist"] = self.artist
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.set_artist(self.artist)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return self.artist.get_absolute_url()


class GetArtistNoteMixin:
    def get_object(self):
        return get_object_or_404(ArtistNote, slug=self.kwargs["slug"])


class EditArtistNote(GetArtistNoteMixin, EditContentView):
    model = ArtistNote
    form_class = forms.ArtistNoteForm
    template_name = "songs/add_edit_artist_note.html"

    # TODO: deduplicate w/ above
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.set_artist(self.get_object().get_parent())

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return self.get_object().get_parent().get_absolute_url()


class ReviewArtistNote(GetArtistNoteMixin, ReviewContentView):
    pass


class ApproveArtistNote(GetArtistNoteMixin, ApproveContentView):
    pass


class AddSongNote(AddContentView):
    model = SongNote
    form_class = forms.SongNoteForm
    template_name = "songs/add_edit_song_note.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.song = None

    def dispatch(self, *args, **kwargs):
        self.song = get_object_or_404(Song, slug=self.kwargs["slug"])
        if not self.song.reviewed:
            raise Http404(
                "Nie można dodać notki do piosenki zanim piosenka "
                "nie zostanie zatwierdzona."
            )
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["song"] = self.song
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.set_song(self.song)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return self.song.get_absolute_url()


class GetSongNoteMixin:
    def get_object(self):
        return get_object_or_404(SongNote, slug=self.kwargs["slug"])


class EditSongNote(GetSongNoteMixin, EditContentView):
    model = SongNote
    form_class = forms.SongNoteForm
    template_name = "songs/add_edit_song_note.html"

    # TODO: deduplicate w/ above
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.set_song(self.get_object().get_parent())

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return self.get_object().get_parent().get_absolute_url()


class ReviewSongNote(GetSongNoteMixin, ReviewContentView):
    pass


class ApproveSongNote(GetSongNoteMixin, ApproveContentView):
    pass
