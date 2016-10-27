import json
import logging

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView

from content.views import (AddContentView, EditContentView, ApproveContentView,
                           ReviewContentView, ViewContentView)
from songs import forms
from songs.lyrics import render_lyrics
from songs.models import Artist, ArtistNote, Song, SongNote, EntityContribution


_action_logger = logging.getLogger('actions')

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


class GetSongMixin(object):

    def get_object(self):
        return get_object_or_404(Song, slug=self.kwargs['slug'])


class GetArtistMixin(object):

    def get_object(self):
        return get_object_or_404(Artist, slug=self.kwargs['slug'])


class SongbookMenuMixin(object):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bards'] = Artist.objects.filter(featured=True,
                                                 category=Artist.CAT_TEXTER)
        context['composers'] = Artist.objects.filter(
            featured=True, category=Artist.CAT_COMPOSER)
        context['foreigners'] = Artist.objects.filter(
            featured=True, category=Artist.CAT_FOREIGN)
        context['bands'] = Artist.objects.filter(featured=True,
                                                 category=Artist.CAT_BAND)
        return context


class IndexView(SongbookMenuMixin, TemplateView):
    template_name = 'songs/index.html'


class ViewArtist(GetArtistMixin, SongbookMenuMixin, DetailView):
    """Lists the songs associated with the given artist."""
    model = Artist
    context_object_name = 'artist'
    template_name = 'songs/artist.html'

    def dispatch(self, *args, **kwargs):
        artist = self.get_object()
        if not artist.featured and not self.request.user.is_authenticated():
            return HttpResponsePermanentRedirect(reverse('songbook'))
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        artist = self.get_object()
        contributions = EntityContribution.objects.filter(
            artist=artist).select_related('song').order_by('song__title')
        songs = [contribution.song for contribution in contributions
                 if contribution.song.can_be_seen_by(self.request.user)]
        context = super().get_context_data(**kwargs)
        context['songs'] = songs
        context['artist'] = artist
        context['notes'] = ArtistNote.items_visible_to(
            self.request.user).filter(artist=self.object)
        return context


class AddArtist(CreateView):
    model = Artist
    form_class = forms.ArtistForm
    template_name = 'songs/add_edit_artist.html'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        ret = super().form_valid(form)
        messages.add_message(self.request, messages.INFO,
                             'Artysta dodany.')
        _action_logger.info('%s added artist %s' % (self.request.user,
                                                    form.instance))
        return ret


class EditArtist(GetArtistMixin, UpdateView):
    model = Artist
    form_class = forms.ArtistForm
    template_name = 'songs/add_edit_artist.html'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        ret = super().form_valid(form)
        messages.add_message(self.request, messages.INFO,
                             'Zmiany zostały zapisane.')
        _action_logger.info('%s edited artist %s' % (self.request.user,
                                                     form.instance))
        return ret


class ViewSong(GetSongMixin, ViewContentView):
    """ Displays a song by default, returns transposed lyrics part in json if
    asked. """
    model = Song
    context_object_name = 'song'
    template_name = 'songs/song.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'transposition' in self.kwargs:
            context['json'] = True
            transposition = int(self.kwargs['transposition'])
            context['transposition'] = transposition
        else:
            transposition = 0
        context['lyrics'] = render_lyrics(self.object.lyrics, transposition)
        context['notes'] = SongNote.items_visible_to(
            self.request.user).filter(song=self.object)
        return context

    def render_to_response(self, context):
        if context.get('json'):
            return self.get_lyrics_as_json(context)
        return super().render_to_response(context)

    def get_lyrics_as_json(self, context):
        payload = {'lyrics': context['lyrics'],
                   'transposition': context['transposition']}
        return HttpResponse(
            json.dumps(payload),
            content_type='application/json')


class ContributionFormsetMixin(object):
    """Manages inline formset of song contributions."""

    def dispatch(self, *args, **kwargs):
        if self.request.method == 'POST':
            self.formset = forms.ContributionFormSet(self.request.POST,
                                                     instance=self.get_object())
        else:
            self.formset = forms.ContributionFormSet(instance=self.get_object())
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entitycontribution'] = self.formset
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        formset = self.formset

        if form.is_valid() and formset.is_valid():
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
    template_name = 'songs/add_edit_song.html'

    def form_valid(self, form):
        # Pick head contribution to put into the slug.
        head = EntityContribution.head_contribution([x.instance
                                                     for x in self.formset])
        assert head
        form.instance.set_slug_prepend_elements([head.artist.__str__()])
        return super().form_valid(form)

    def get_initial(self):
        return {'lyrics': INITIAL_LYRICS}

    def get_success_url(self):
        return self.object.get_absolute_url()


class EditSong(GetSongMixin, ContributionFormsetMixin, EditContentView):
    model = Song
    form_class = forms.SongForm
    template_name = 'songs/add_edit_song.html'

    def get_success_url(self):
        return self.object.get_absolute_url()


class ReviewSong(GetSongMixin, ReviewContentView):
    pass


class ApproveSong(GetSongMixin, ApproveContentView):
    pass


class AddArtistNote(AddContentView):
    model = ArtistNote
    form_class = forms.ArtistNoteForm
    template_name = 'songs/add_edit_artist_note.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.artist = None

    def dispatch(self, *args, **kwargs):
        self.artist = get_object_or_404(Artist, slug=self.kwargs['slug'])
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['artist'] = self.artist
        return context

    def form_valid(self, form):
        form.instance.artist = self.artist
        return super().form_valid(form)

    def get_success_url(self):
        return self.artist.get_absolute_url()


class GetArtistNoteMixin(object):

    def get_object(self):
        return get_object_or_404(ArtistNote, slug=self.kwargs['slug'])


class EditArtistNote(GetArtistNoteMixin, EditContentView):
    model = ArtistNote
    form_class = forms.ArtistNoteForm
    template_name = 'songs/add_edit_artist_note.html'

    def get_success_url(self):
        return self.get_object().get_parent().get_absolute_url()


class ReviewArtistNote(GetArtistNoteMixin, ReviewContentView):
    pass


class ApproveArtistNote(GetArtistNoteMixin, ApproveContentView):
    pass


class AddSongNote(AddContentView):
    model = SongNote
    form_class = forms.SongNoteForm
    template_name = 'songs/add_edit_song_note.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.song = None

    def dispatch(self, *args, **kwargs):
        self.song = get_object_or_404(Song, slug=self.kwargs['slug'])
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['song'] = self.song
        return context

    def form_valid(self, form):
        form.instance.song = self.song
        return super().form_valid(form)

    def get_success_url(self):
        return self.song.get_absolute_url()


class GetSongNoteMixin(object):

    def get_object(self):
        return get_object_or_404(SongNote, slug=self.kwargs['slug'])


class EditSongNote(GetSongNoteMixin, EditContentView):
    model = SongNote
    form_class = forms.SongNoteForm
    template_name = 'songs/add_edit_song_note.html'

    def get_success_url(self):
        return self.get_object().get_parent().get_absolute_url()


class ReviewSongNote(GetSongNoteMixin, ReviewContentView):
    pass


class ApproveSongNote(GetSongNoteMixin, ApproveContentView):
    pass
