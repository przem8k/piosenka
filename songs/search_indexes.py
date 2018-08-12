import datetime

from haystack import site
from haystack.indexes import *
from songs.models import Song


class SongIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Song.objects.all()


site.register(Song, SongIndex)
