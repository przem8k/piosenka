import json

from django.conf.urls import url
from django.http import HttpResponse
from django.views.decorators.cache import cache_control
from django.views.generic.base import View

from songs.models import Artist, Song


class JSONSearchIndexMixin:
    @cache_control(max_age=300)
    def render_to_response(self, context):
        return self.get_json_response(json.dumps(context["index"]))

    def get_json_response(self, content, **httpresponse_kwargs):
        return HttpResponse(
            content, content_type="application/json", **httpresponse_kwargs
        )


class ArtistSearchIndex(JSONSearchIndexMixin, View):
    def get(self, request, *args, **kwargs):
        index = []
        for artist in Artist.objects.filter(featured=True):
            index.append(
                {
                    "name": artist.__str__(),
                    "value": artist.__str__(),
                    "tokens": artist.__str__().split(),
                    "url": artist.get_absolute_url(),
                }
            )
        return self.render_to_response({"index": index})


class SongSearchIndex(JSONSearchIndexMixin, View):
    def get(self, request, *args, **kwargs):
        index = []
        for song in Song.items_live():
            index.append(
                {
                    "name": song.__str__(),
                    "value": song.__str__(),
                    "tokens": song.__str__().split(),
                    "url": song.get_absolute_url(),
                }
            )
        return self.render_to_response({"index": index})


urlpatterns = [
    url(r"^artists$", ArtistSearchIndex.as_view(), name="search_index_artists"),
    url(r"^songs$", SongSearchIndex.as_view(), name="search_index_songs"),
]
