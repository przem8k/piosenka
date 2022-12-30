from django.urls import include, re_path

from content import url_scheme
from songs import views

urlpatterns = [
    re_path(
        r"^piosenka/(?P<slug>[-\w]+)/",
        include(
            url_scheme.edit_review_approve(
                "song_note",
                views.EditSongNote,
                views.ReviewSongNote,
                views.ApproveSongNote,
            )
        ),
    ),
    re_path(
        r"^artysta/(?P<slug>[-\w]+)/",
        include(
            url_scheme.edit_review_approve(
                "artist_note",
                views.EditArtistNote,
                views.ReviewArtistNote,
                views.ApproveArtistNote,
            )
        ),
    ),
]
