from django.conf.urls import patterns, url

from songs.views import AddSong, ApproveSong, EditSong, SongView

urlpatterns = patterns(
    '',
    url(r'^dodaj/$', AddSong.as_view(), name="add_song"),
    url(r'^(?P<slug>[-\w]+)/$', SongView.as_view(), name="song"),
    url(r'^(?P<slug>[-\w]+)/transpose/(?P<transposition>\d+)/$',
        SongView.as_view(), name="song-transposition"),
    url(r'^(?P<slug>[-\w]+)/edytuj/$', EditSong.as_view(), name="edit_song"),
    url(r'^(?P<slug>[-\w]+)/zatwierdz/$', ApproveSong.as_view(),
        name="approve_song"),
)
