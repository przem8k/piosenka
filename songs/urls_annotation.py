from django.conf.urls import include, url

from content import url_scheme
from songs import views

urlpatterns = [
    url(r'^piosenka/(?P<slug>[-\w]+)/', include(url_scheme.edit_review_approve(
        'song_note', views.EditSongNote, views.ReviewSongNote,
        views.ApproveSongNote))),
    url(r'^piosenka-dawniej/(?P<slug>[-\w]+)/', include(url_scheme.edit_review_approve(
        'annotation', views.EditAnnotation, views.ReviewAnnotation,
        views.ApproveAnnotation))),
    url(r'^artysta/(?P<slug>[-\w]+)/', include(url_scheme.edit_review_approve(
        'artist_note', views.EditArtistNote, views.ReviewArtistNote,
        views.ApproveArtistNote))),
]
