""" Views for handling obsolete url redirects. """
from django.shortcuts import get_object_or_404
from django.http import HttpResponsePermanentRedirect

from songs.models import Song


def obsolete_song(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    return HttpResponsePermanentRedirect(song.get_absolute_url())
