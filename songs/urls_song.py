from django.urls import include, re_path

from content import url_scheme
from songs import views

urlpatterns = [
    re_path(r"^dodaj/$", views.AddSong.as_view(), name="add_song"),
    re_path(
        r"^(?P<slug>[-\w]+)/",
        include(
            url_scheme.view_edit_review_approve(
                "song",
                views.ViewSong,
                views.EditSong,
                views.ReviewSong,
                views.ApproveSong,
            )
            + [
                re_path(
                    r"^transpose/(?P<transposition>\d+)/$",
                    views.ViewSong.as_view(),
                    name="song-transposition",
                ),
                re_path(
                    r"^dodaj-adnotacje/$",
                    views.AddSongNote.as_view(),
                    name="add_song_note",
                ),
            ]
        ),
    ),
]
