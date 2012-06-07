from django.conf.urls.defaults import *
from songs.views import *
from haystack.views import search_view_factory
from haystack.forms import SearchForm

urlpatterns = patterns('songs.views',
    url(r'^(?P<slug>[-\w]+)/$', artist, name="songs-by-artist"),
    url(r'^szukaj/(?P<song_slug>[-\w]+)/$', redirect_to_song),
    url(r'^(?P<artist_slug>[-\w]+)/(?P<song_slug>[-\w]+)/$', artist_song, { 'mode' : SongMode.DISPLAY }, name="display-song" ),
    url(r'^(?P<artist_slug>[-\w]+)/(?P<song_slug>[-\w]+)/drukuj/tylko-tekst/$', artist_song, { 'mode' : SongMode.PRINT_TEXT_ONLY } , name="print-song-text-only"),
    url(r'^(?P<artist_slug>[-\w]+)/(?P<song_slug>[-\w]+)/drukuj/$', artist_song, { 'mode' : SongMode.PRINT_BASIC_CHORDS } , name="print-song-basic-chords"),
    url(r'^(?P<artist_slug>[-\w]+)/(?P<song_slug>[-\w]+)/drukuj/wszystkie-akordy/$', artist_song, { 'mode' : SongMode.PRINT_ALL_CHORDS } , name="print-song-all-chords"),
    url(r'^$', search_view_factory(
        view_class=SongSearchView,
        template='songs_search.html',
        form_class=SearchForm,
    )),
)
