import json

from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, TemplateView, RedirectView
from django.views.generic.edit import CreateView, UpdateView

from artists.models import Entity
from piosenka.mixins import ContentItemEditMixin, ContentItemAddMixin
from piosenka.mixins import ContentItemViewMixin
from piosenka.mixins import ContentItemApproveMixin
from piosenka.mixins import ManageInlineFormsetMixin
from songs.forms import SongForm, ContributionFormSet
from songs.lyrics import render_lyrics
from songs.models import Song, EntityContribution


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


def get_song_by_entity_or_404(song_slug, entity_slug):
    song = get_object_or_404(Song, core_slug=song_slug)
    entity = get_object_or_404(Entity, slug=entity_slug)
    # verify that the song was reached via proper artist or band
    if EntityContribution.objects.filter(song=song, entity=entity).count() == 0:
        raise Http404()
    return song


class SongRedirectView(RedirectView):
    """ Displays a songs by default, returns transposed lyrics part in json if
    asked. """

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
        if not songs:
            raise Http404()
        context = super().get_context_data(**kwargs)
        context['songs'] = songs
        context['entity'] = entity
        return context


class SongView(ContentItemViewMixin, DetailView):
    """ Displays a song by default, returns transposed lyrics part in json if
    asked. """
    model = Song
    context_object_name = 'song'
    template_name = 'songs/song.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO: why we do self.kwargs and not kwargs here?
        if 'transposition' in self.kwargs:
            context['json'] = True
            transposition = int(self.kwargs['transposition'])
            context['transposition'] = transposition
        else:
            transposition = 0
        context['lyrics'] = render_lyrics(self.object.lyrics, transposition)
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
        form.instance.extra_slug_elements = [head.entity.__str__()]
        # Set the author.
        form.instance.author = self.request.user
        # Save the song - this is required for saving the contributions as they
        # need songs pk.
        # TODO Add test for this prepend_slug_elements hackery.
        form.instance.save(prepend_slug_elements=[head.entity.__str__()])
        contributions.instance = form.instance
        contributions.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class EditSong(ContentItemEditMixin, ManageInlineFormsetMixin, UpdateView):
    model = Song
    form_class = SongForm
    template_name = "songs/add_edit_song.html"

    def get_object(self):
        return get_object_or_404(Song, slug=self.kwargs['slug'])

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


class ApproveSong(ContentItemApproveMixin, RedirectView):
    def get_object(self):
        return get_object_or_404(Song, slug=self.kwargs['slug'])
