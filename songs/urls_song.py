from django.conf.urls import include, url

from content import url_scheme
from songs import views

urlpatterns = [
    url(r'^dodaj/$', views.AddSong.as_view(),
        name='add_song'),
    url(r'^(?P<slug>[-\w]+)/',
        include(url_scheme.view_edit_review_approve(
            'song', views.ViewSong, views.EditSong, views.ReviewSong,
            views.ApproveSong) + [
                url(r'^transpose/(?P<transposition>\d+)/$',
                    views.ViewSong.as_view(),
                    name='song-transposition'),
                url(r'^dodaj-adnotacje/$',
                    views.AddAnnotation.as_view(),
                    name='add_annotation'),
            ])),
]
