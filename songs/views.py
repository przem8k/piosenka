import json

from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, RedirectView
from django.views.generic.edit import CreateView, UpdateView

from artists.models import Entity
from content.mixins import ContentItemEditMixin, ContentItemAddMixin
from content.mixins import ManageInlineFormsetMixin
from content.views import ApproveContentView
from content.views import ReviewContentView
from content.views import ViewContentView
from songs.forms import AnnotationForm, SongForm, ContributionFormSet
from songs.lyrics import render_lyrics
from songs.models import Annotation, Song, EntityContribution


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


def get_song_by_entity_or_404(song_slug, entity_slug):
    song = get_object_or_404(Song, core_slug=song_slug)
    entity = get_object_or_404(Entity, slug=entity_slug)
    # verify that the song was reached via proper artist or band
    if EntityContribution.objects.filter(song=song, entity=entity).count() == 0:
        raise Http404()
    return song


class SongRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        song = get_song_by_entity_or_404(kwargs['slug'], kwargs['entity_slug'])
        return song.get_absolute_url()


class BaseMenuView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bards"] = Entity.objects.filter(
            featured=True, kind=Entity.TYPE_TEXTER)
        context["composers"] = Entity.objects.filter(
            featured=True, kind=Entity.TYPE_COMPOSER)
        context["translators"] = Entity.objects.filter(
            featured=True, kind=Entity.TYPE_TRANSLATOR)
        context["performers"] = Entity.objects.filter(
            featured=True, kind=Entity.TYPE_PERFORMER)
        context["foreigners"] = Entity.objects.filter(
            featured=True, kind=Entity.TYPE_FOREIGN)
        context["bands"] = Entity.objects.filter(
            featured=True, kind=Entity.TYPE_BAND)
        return context


class IndexView(BaseMenuView):
    template_name = "songs/index.html"


class EntityView(BaseMenuView):
    """ Lists the songs associated with the given Entity object. """
    template_name = "songs/list.html"

    def get_context_data(self, **kwargs):
        slug = kwargs['slug']
        entity = get_object_or_404(Entity, slug=slug)
        contributions = EntityContribution.objects.filter(
            entity=entity).select_related('song').order_by('song__title')
        songs = [contribution.song for contribution in contributions
                 if contribution.song.can_be_seen_by(self.request.user)]
        if not songs and not entity.featured:
            # TODO: maybe one day throws 404 always if not featured? We would
            # only link to the artist from a Song view if they are featured.
            # Issue: we already have a few not featured pages indexed.
            raise Http404()
        context = super().get_context_data(**kwargs)
        context['songs'] = songs
        context['entity'] = entity
        return context


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
        return HttpResponse(json.dumps(payload),
                            content_type='application/json')


class AddSong(ContentItemAddMixin, ManageInlineFormsetMixin, CreateView):
    model = Song
    form_class = SongForm
    template_name = "songs/add_edit_song.html"

    def get_initial(self):
        return {
            'lyrics': INITIAL_LYRICS,
        }

    def get_managed_formset_class(self):
        return ContributionFormSet

    def form_valid(self, form):
        contributions = super().get_managed_formset()
        if not contributions.is_valid():
            return self.form_invalid(form)

        # Pick head contribution to put into the slug.
        head = EntityContribution.head_contribution([x.instance for x in
                                                     contributions])
        assert head
        form.instance.set_slug_prepend_elements([head.entity.__str__()])
        form.instance.author = self.request.user
        # Save the song - this is required before saving the contributions.
        form.instance.save()

        contributions.instance = form.instance
        contributions.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class EditSong(GetSongMixin, ContentItemEditMixin, ManageInlineFormsetMixin,
               UpdateView):
    model = Song
    form_class = SongForm
    template_name = "songs/add_edit_song.html"

    def get_managed_formset_class(self):
        return ContributionFormSet

    def form_valid(self, form):
        contributions = super().get_managed_formset()
        if not contributions.is_valid():
            return self.form_invalid(form)
        contributions.instance = form.save()
        contributions.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class ReviewSong(GetSongMixin, ReviewContentView):
    pass


class ApproveSong(GetSongMixin, ApproveContentView):
    pass


class AddAnnotation(ContentItemAddMixin, CreateView):
    model = Annotation
    form_class = AnnotationForm
    template_name = "songs/add_edit_annotation.html"

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
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.song.get_absolute_url()


class GetAnnotationMixin(object):
    def get_object(self):
        return get_object_or_404(Annotation, slug=self.kwargs['slug'])


class EditAnnotation(GetAnnotationMixin, ContentItemEditMixin,
                     UpdateView):
    model = Annotation
    form_class = AnnotationForm
    template_name = "songs/add_edit_annotation.html"

    def get_success_url(self):
        return self.get_object().song.get_absolute_url()


class ReviewAnnotation(GetAnnotationMixin, ReviewContentView):
    pass


class ApproveAnnotation(GetAnnotationMixin, ApproveContentView):
    pass
