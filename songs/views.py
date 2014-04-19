import json

from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from artists.models import Artist, Band
from songs.lyrics import render_lyrics
from songs.models import Song, ArtistContribution, BandContribution


def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


class BaseMenuView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(BaseMenuView, self).get_context_data(**kwargs)
        context["bards"] = Artist.objects.filter(display=True, kind=Artist.KIND_TEXTER)
        context["composers"] = Artist.objects.filter(display=True, kind=Artist.KIND_COMPOSER)
        context["translators"] = Artist.objects.filter(display=True, kind=Artist.KIND_TRANSLATOR)
        context["performers"] = Artist.objects.filter(display=True, kind=Artist.KIND_PERFORMER)
        context["foreigners"] = Artist.objects.filter(display=True, kind=Artist.KIND_FOREIGN)
        context["bands"] = Band.objects.filter(display=True)
        return context


class IndexView(BaseMenuView):
    template_name = "songs/index.html"


class ArtistView(BaseMenuView):
    """ Lists the songs associated with the given Artist or Band object. """
    template_name = "songs/list.html"

    def get_context_data(self, **kwargs):
        slug = kwargs['slug']
        try:
            entity = Artist.objects.get(slug=slug)
            songs = [x.song for x in (ArtistContribution.objects.filter(artist=entity,
                                                                        song__published=True)
                                      .select_related('song')
                                      .order_by('song__title'))]
        except Artist.DoesNotExist:
            entity = get_object_or_404(Band, slug=slug)
            songs = [x.song for x in (BandContribution.objects.filter(band=entity,
                                                                      song__published=True)
                                      .select_related('song')
                                      .order_by('song__title'))]
        context = super(ArtistView, self).get_context_data(**kwargs)
        context['songs'] = songs
        context['entity'] = entity
        return context


class SongView(TemplateView):
    """ Displays a songs by default, returns transposed lyrics part in json if asked. """
    template_name = 'songs/song.html'

    def get_context_data(self, **kwargs):
        artist_slug = kwargs['artist_slug']
        song_slug = kwargs['song_slug']

        song = get_object_or_404(Song, slug=song_slug)
        artist = get_or_none(Artist, slug=artist_slug)
        band = get_or_none(Band, slug=artist_slug)

        # verify that the song was reached via proper artist or band
        if ((artist is None or
             ArtistContribution.objects.filter(song=song, artist=artist).count() == 0
             ) and
            (band is None or
             BandContribution.objects.filter(song=song, band=band).count() == 0)):
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
