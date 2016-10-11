import json

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from content.views import (AddContentView, EditContentView, ApproveContentView,
                           ReviewContentView, ViewContentView)
from songs.forms import (ArtistForm, ArtistNoteForm, AnnotationForm, SongForm,
                         ContributionFormSet)
from songs.lyrics import render_lyrics
from songs.models import (Annotation, Artist, ArtistNote, Song,
                          EntityContribution)

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


class ViewArtist(GetArtistMixin, SongbookMenuMixin, ViewContentView):
    """Lists the songs associated with the given artist."""
    model = Artist
    context_object_name = 'artist'
    template_name = 'songs/artist.html'

    def get_context_data(self, **kwargs):
        artist = self.get_object()
        contributions = EntityContribution.objects.filter(
            artist=artist).select_related('song').order_by('song__title')
        songs = [contribution.song for contribution in contributions
                 if contribution.song.can_be_seen_by(self.request.user)]
        if not songs and not artist.featured:
            # TODO: maybe one day throws 404 always if not featured? We would
            # only link to the artist from a Song view if they are featured.
            # Issue: we already have a few not featured pages indexed.
            raise Http404()
        context = super().get_context_data(**kwargs)
        context['songs'] = songs
        context['artist'] = artist
        context['notes'] = ArtistNote.items_visible_to(
            self.request.user).filter(artist=self.object)
        return context


class AddArtist(AddContentView):
    model = Artist
    form_class = ArtistForm
    template_name = 'songs/add_edit_artist.html'

    def get_success_url(self):
        return self.object.get_absolute_url()


class EditArtist(GetArtistMixin, EditContentView):
    model = Artist
    form_class = ArtistForm
    template_name = 'songs/add_edit_artist.html'

    def get_success_url(self):
        return self.object.get_absolute_url()


class ReviewArtist(GetArtistMixin, ReviewContentView):
    pass


class ApproveArtist(GetArtistMixin, ApproveContentView):
    pass


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
        context['annotations'] = Annotation.items_visible_to(
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
            self.formset = ContributionFormSet(self.request.POST,
                                               instance=self.get_object())
        else:
            self.formset = ContributionFormSet(instance=self.get_object())
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
    form_class = SongForm
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
    form_class = SongForm
    template_name = 'songs/add_edit_song.html'

    def get_success_url(self):
        return self.object.get_absolute_url()


class ReviewSong(GetSongMixin, ReviewContentView):
    pass


class ApproveSong(GetSongMixin, ApproveContentView):
    pass


class AddAnnotation(AddContentView):
    model = Annotation
    form_class = AnnotationForm
    template_name = 'songs/add_edit_annotation.html'

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


class GetAnnotationMixin(object):

    def get_object(self):
        return get_object_or_404(Annotation, slug=self.kwargs['slug'])


class EditAnnotation(GetAnnotationMixin, EditContentView):
    model = Annotation
    form_class = AnnotationForm
    template_name = 'songs/add_edit_annotation.html'

    def get_success_url(self):
        return self.get_object().song.get_absolute_url()


class ReviewAnnotation(GetAnnotationMixin, ReviewContentView):
    pass


class ApproveAnnotation(GetAnnotationMixin, ApproveContentView):
    pass


class AddArtistNote(AddContentView):
    model = ArtistNote
    form_class = ArtistNoteForm
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
    form_class = ArtistNoteForm
    template_name = 'songs/add_edit_artist_note.html'

    def get_success_url(self):
        return self.get_object().get_parent().get_absolute_url()


class ReviewArtistNote(GetArtistNoteMixin, ReviewContentView):
    pass


class ApproveArtistNote(GetArtistNoteMixin, ApproveContentView):
    pass
