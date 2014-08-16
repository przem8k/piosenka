from django.conf.urls import patterns, url
from django.views.generic import RedirectView

from songs.views import IndexView, EntityView, SongView

urlpatterns = patterns(
    'songs.views',
    url(r'^(?P<slug>[-\w]+)/$', EntityView.as_view(), name="songbook_entity"),
    url(r'^(?P<entity_slug>[-\w]+)/(?P<song_slug>[-\w]+)/$', SongView.as_view(), name="song"),
    url(r'^(?P<entity_slug>[-\w]+)/(?P<song_slug>[-\w]+)/transpose/(?P<transposition>\d+)/$',
        SongView.as_view(), name="song-transposition"),
    # Separate print view is obsolete, redirect to song.
    url(r'^(?P<entity_slug>[-\w]+)/(?P<song_slug>[-\w]+)/drukuj/$',
        RedirectView.as_view(url='/spiewnik/%(entity_slug)s/%(song_slug)s/'), name="song-print"),
    url(r'^$', IndexView.as_view()),
)
