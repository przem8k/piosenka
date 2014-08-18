import json

from django.core.urlresolvers import reverse_lazy
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from unidecode import unidecode

from artists.models import Entity
from frontpage.views import CheckAuthorshipMixin, CheckLoginMixin
from songs.forms import SongForm, ContributionFormSet
from songs.lyrics import render_lyrics
from songs.models import Song, EntityContribution


def get_song_by_entity_or_404(song_slug, entity_slug):
    song = get_object_or_404(Song, slug=song_slug)
    entity = get_object_or_404(Entity, slug=entity_slug)
    # verify that the song was reached via proper artist or band
    if EntityContribution.objects.filter(song=song, entity=entity).count() == 0:
        raise Http404()
    return song


class BaseMenuView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(BaseMenuView, self).get_context_data(**kwargs)
        context["bards"] = Entity.objects.filter(featured=True, kind=Entity.TYPE_TEXTER)
        context["composers"] = Entity.objects.filter(featured=True, kind=Entity.TYPE_COMPOSER)
        context["translators"] = Entity.objects.filter(featured=True, kind=Entity.TYPE_TRANSLATOR)
        context["performers"] = Entity.objects.filter(featured=True, kind=Entity.TYPE_PERFORMER)
        context["foreigners"] = Entity.objects.filter(featured=True, kind=Entity.TYPE_FOREIGN)
        context["bands"] = Entity.objects.filter(featured=True, kind=Entity.TYPE_BAND)
        return context


class IndexView(BaseMenuView):
    template_name = "songs/index.html"


class EntityView(BaseMenuView):
    """ Lists the songs associated with the given Entity object. """
    template_name = "songs/list.html"

    def get_context_data(self, **kwargs):
        slug = kwargs['slug']
        entity = get_object_or_404(Entity, slug=slug)
        songs = [x.song for x in (EntityContribution.objects.filter(entity=entity,
                                                                    song__published=True)
                                  .select_related('song')
                                  .order_by('song__title'))]
        if not songs:
            raise Http404()
        context = super(EntityView, self).get_context_data(**kwargs)
        context['songs'] = songs
        context['entity'] = entity
        return context


class SongView(TemplateView):
    """ Displays a songs by default, returns transposed lyrics part in json if asked. """
    template_name = 'songs/song.html'

    def get_context_data(self, **kwargs):
        context = super(SongView, self).get_context_data(**kwargs)
        song = get_song_by_entity_or_404(kwargs['song_slug'], kwargs['entity_slug'])
        if 'transposition' in kwargs:
            context['json'] = True
            transposition = int(kwargs['transposition'])
            context['transposition'] = transposition
        else:
            transposition = 0
        context['song'] = song
        context['lyrics'] = render_lyrics(song.lyrics, transposition)
        return context

    def render_to_response(self, context):
        if context.get('json'):
            return self.get_lyrics_as_json(context)
        return super(SongView, self).render_to_response(context)

    def get_lyrics_as_json(self, context):
        payload = {'lyrics': context['lyrics'],
                   'transposition': context['transposition']}
        return HttpResponse(json.dumps(payload),
                            content_type='application/json')


class ManageContributionsMixin(object):
    def get_contributions_formset(self):
        if self.request.POST:
            return ContributionFormSet(self.request.POST, instance=self.object)
        else:
            return ContributionFormSet(instance=self.object)

    def get_context_data(self, **kwargs):
        context = super(ManageContributionsMixin, self).get_context_data(**kwargs)
        context['contributions'] = self.get_contributions_formset()
        return context

    def form_valid(self, form):
        contributions = self.get_contributions_formset()
        if not contributions.is_valid():
            raise RuntimeError()
        contributions.instance = form.instance

        ret = super(ManageContributionsMixin, self).form_valid(form)
        contributions.save()
        return ret


class AddSong(CheckLoginMixin, ManageContributionsMixin, CreateView):
    model = Song
    form_class = SongForm
    template_name = "songs/add_edit_song.html"
    success_url = reverse_lazy('songbook')

    def form_valid(self, form):
        contributions = super(AddSong, self).get_contributions_formset()
        if not contributions.is_valid():
            return self.form_invalid(form)

        form.instance.slug = slugify(unidecode(form.cleaned_data['title'] + " " +
                                     form.cleaned_data['disambig']))
        form.instance.author = self.request.user
        return super(AddSong, self).form_valid(form)


class EditSong(CheckAuthorshipMixin, ManageContributionsMixin, UpdateView):
    model = Song
    form_class = SongForm
    template_name = "songs/add_edit_song.html"

    def get_object(self):
        return get_song_by_entity_or_404(self.kwargs['song_slug'], self.kwargs['entity_slug'])

    def form_valid(self, form):
        contributions = super(EditSong, self).get_contributions_formset()
        if not contributions.is_valid():
            return self.form_invalid(form)
        return super(EditSong, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()
