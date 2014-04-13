from songs.models import Song, ArtistContribution, BandContribution
from artists.models import Artist, Band
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from songs.lyrics import render_lyrics


def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


def songs_context(request):
    context = {}
    context["url"] = request.path
    context["bards"] = Artist.objects.filter(display=True, kind=Artist.KIND_TEXTER)
    context["composers"] = Artist.objects.filter(display=True, kind=Artist.KIND_COMPOSER)
    context["translators"] = Artist.objects.filter(display=True, kind=Artist.KIND_TRANSLATOR)
    context["performers"] = Artist.objects.filter(display=True, kind=Artist.KIND_PERFORMER)
    context["foreigners"] = Artist.objects.filter(display=True, kind=Artist.KIND_FOREIGN)
    context["bands"] = Band.objects.filter(display=True)
    return context


class IndexView(TemplateView):
    template_name = "songs/index.html"


class ArtistView(TemplateView):
    """ Lists the songs associated with the given Artist or Band object. """
    template_name = "songs/list.html"

    def get_context_data(self, **kwargs):
        slug = kwargs['slug']
        try:
            entity = Artist.objects.get(slug=slug)
            songs = [x.song for x in (ArtistContribution.objects.filter(artist=entity)
                                      .select_related('song')
                                      .order_by('song__title'))]
        except Artist.DoesNotExist:
            entity = get_object_or_404(Band, slug=slug)
            songs = [x.song for x in (BandContribution.objects.filter(band=entity)
                                      .select_related('song')
                                      .order_by('song__title'))]
        context = super(ArtistView, self).get_context_data(**kwargs)
        context['songs'] = songs
        context['entity'] = entity
        return context


class SongView(TemplateView):
    """ Displays a song. """
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

        if self.request.method == "GET" and "t" in self.request.GET:
            try:
                t = int(self.request.GET["t"])
                if t >= 0 and t < 12:
                    transposition = t
                else:
                    transposition = 0
            except ValueError:
                transposition = 0
        else:
            transposition = 0
        trans_up = (transposition + 1) % 12
        trans_down = (transposition + 11) % 12

        context = super(SongView, self).get_context_data(**kwargs)
        context['song'] = song
        context['trans'] = transposition
        context['trans_up'] = trans_up
        context['trans_down'] = trans_down
        context['lyrics'] = render_lyrics(song.lyrics, transposition)
        return context
