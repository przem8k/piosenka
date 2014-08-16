import json

from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from artists.models import Entity
from songs.lyrics import render_lyrics
from songs.models import Song, EntityContribution


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
        entity_slug = kwargs['entity_slug']
        song_slug = kwargs['song_slug']

        song = get_object_or_404(Song, slug=song_slug)
        entity = get_object_or_404(Entity, slug=entity_slug)

        # verify that the song was reached via proper artist or band
        if EntityContribution.objects.filter(song=song, entity=entity).count() == 0:
            raise Http404()

        context = super(SongView, self).get_context_data(**kwargs)
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
