from django.conf.urls import include, url

from songs import views

urlpatterns = [
    url(r'^dodaj/$', views.AddSong.as_view(), name="add_song"),
    url(r'^(?P<slug>[-\w]+)/', include([
        url(r'^$', views.SongView.as_view(), name="song"),
        url(r'^transpose/(?P<transposition>\d+)/$', views.SongView.as_view(),
            name="song-transposition"),
        url(r'^edytuj/$', views.EditSong.as_view(), name="edit_song"),
        url(r'^zatwierdz/$', views.ApproveSong.as_view(), name="approve_song"),
        ])),
]
