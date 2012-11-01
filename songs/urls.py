from django.conf.urls.defaults import *
from songs.views import *

urlpatterns = patterns('songs.views',
    url(r'^(?P<slug>[-\w]+)/$', entity, name="songbook-entity"),
    url(r'^(?P<artist_slug>[-\w]+)/(?P<song_slug>[-\w]+)/$', song_or_translation_entry, name="song"),
    url(r'^(?P<artist_slug>[-\w]+)/(?P<song_slug>[-\w]+)/drukuj/$', song_or_translation_entry, {'for_print': True}, name="song-print"),
    url(r'^(?P<artist_slug>[-\w]+)/(?P<song_slug>[-\w]+)/tlumaczenie/(?P<translator_slug>[-\w]+)/$', song_or_translation_entry, name="translation"),
    url(r'^(?P<artist_slug>[-\w]+)/(?P<song_slug>[-\w]+)/tlumaczenie/(?P<translator_slug>[-\w]+)/drukuj/$', song_or_translation_entry, {'for_print': True}, name="translation-print"),
    url(r'^$', IndexView.as_view()),
)
