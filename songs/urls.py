from django.conf.urls import patterns, url
from django.views.generic import RedirectView

from songs.views import entity, song_or_translation_entry, IndexView

urlpatterns = patterns(
    'songs.views',
    url(r'^(?P<slug>[-\w]+)/$', entity, name="songbook-entity"),
    url(r'^(?P<artist_slug>[-\w]+)/(?P<song_slug>[-\w]+)/$', song_or_translation_entry,
        name="song"),
    # Separate print view is obsolete, redirect to song.
    url(r'^(?P<artist_slug>[-\w]+)/(?P<song_slug>[-\w]+)/drukuj/$',
        RedirectView.as_view(url='/spiewnik/%(artist_slug)s/%(song_slug)s/'), name="song-print"),
    url(r'^$', IndexView.as_view()),
)
