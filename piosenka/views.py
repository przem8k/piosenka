from datetime import date, datetime

from django.contrib.auth.models import User
from django.views.generic import TemplateView

from content.models import filter_visible_to_user
from events.models import get_events_for
from songs.models import Artist, ArtistNote, Song, SongNote


class SiteIndex(TemplateView):
    template_name = "frontpage/index.html"
    SONG_COUNT = 8
    ANNOTATION_COUNT = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = get_events_for(self.request.user)
        context["songs"] = Song.items_visible_to(self.request.user).order_by(
            "-pub_date"
        )[: SiteIndex.SONG_COUNT]
        context["annotation"] = (
            SongNote.items_visible_to(self.request.user).order_by("-pub_date").first()
        )
        song_notes = SongNote.items_visible_to(self.request.user).order_by("-pub_date")[
            : SiteIndex.ANNOTATION_COUNT
        ]
        artist_notes = ArtistNote.items_visible_to(self.request.user).order_by(
            "-pub_date"
        )[: SiteIndex.ANNOTATION_COUNT]
        notes = list(song_notes) + list(artist_notes)
        notes.sort(key=lambda x: x.pub_date, reverse=True)
        context["annotations"] = notes[: SiteIndex.ANNOTATION_COUNT]
        return context


class Search(TemplateView):
    template_name = "search.html"
