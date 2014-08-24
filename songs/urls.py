from django.conf.urls import patterns, url
from django.views.generic import RedirectView

from songs.views import IndexView, EntityView, SongRedirectView

urlpatterns = patterns(
    'songs.views',
    url(r'^$', IndexView.as_view(), name="songbook"),
    url(r'^(?P<slug>[-\w]+)/$', EntityView.as_view(), name="songbook_entity"),
    # Obsolete url redirects.
    url(r'^(?P<entity_slug>[-\w]+)/(?P<song_slug>[-\w]+)/$', SongRedirectView.as_view()),
    url(r'^(?P<entity_slug>[-\w]+)/(?P<song_slug>[-\w]+)/drukuj/$',
        RedirectView.as_view(url='/spiewnik/%(entity_slug)s/%(song_slug)s/'), name="song-print"),
)
