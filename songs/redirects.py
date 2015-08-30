"""Views for handling obsolete url redirects."""

from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.generic import RedirectView

from artists.models import Entity
from songs.models import Song, EntityContribution


def _get_song_by_entity_or_404(song_old_slug, entity_slug):
    song = get_object_or_404(Song, core_slug=song_old_slug)
    entity = get_object_or_404(Entity, slug=entity_slug)
    # verify that the song was reached via proper artist or band
    if EntityContribution.objects.filter(song=song, entity=entity).count() == 0:
        raise Http404()
    return song


class SongRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        song = _get_song_by_entity_or_404(kwargs['slug'], kwargs['entity_slug'])
        return song.get_absolute_url()


class SongRedirectByIdView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        song = get_object_or_404(Song, pk=kwargs['song_id'])
        return song.get_absolute_url()
