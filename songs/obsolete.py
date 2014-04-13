""" Views for handling obsolete url redirects. """
from django.shortcuts import get_object_or_404
from django.http import HttpResponsePermanentRedirect, Http404

from artists.models import Artist, Band
from songs.models import Song, ArtistContribution, BandContribution


def redirect_to_song(request, song_slug):
    piece = get_object_or_404(Song, slug=song_slug)
    artists = ArtistContribution.objects.filter(song=piece)
    bands = BandContribution.objects.filter(song=piece)
    if len(artists) > 0:
        artist = artists[0].artist
    elif len(bands) > 0:
        artist = bands[0].band
    else:
        raise Http404()
    return HttpResponsePermanentRedirect("/spiewnik/%s/%s/" % (artist.slug, piece.slug,))


def obsolete_artist(request, artist_id):
    artist = get_object_or_404(Artist, pk=artist_id)
    return HttpResponsePermanentRedirect("/spiewnik/%s/" % (artist.slug,))


def obsolete_band(request, band_id):
    band = get_object_or_404(Band, pk=band_id)
    return HttpResponsePermanentRedirect("/spiewnik/%s/" % (band.slug,))


def obsolete_song(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    return redirect_to_song(request, song.slug)
