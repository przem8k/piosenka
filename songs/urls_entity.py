from django.conf.urls import include, url

from songs import views
from songs import redirects

urlpatterns = [
    url(r'^$', views.IndexView.as_view(),
        name='songbook'),
    url(r'^dodaj/$', views.AddArtist.as_view(),
        name='add_artist'),
    url(r'^(?P<slug>[-\w]+)/',
        include([
            url(r'^$', views.ViewArtist.as_view(),
                name='view_artist'),
            url(r'^edytuj/$',
                views.EditArtist.as_view(),
                name='edit_artist'),
            url(r'^korekta/$',
                views.ReviewArtist.as_view(),
                name='review_artist'),
            url(r'^zatwierdz/$',
                views.ApproveArtist.as_view(),
                name='approve_artist'),
        ])),
    # Obsolete url redirects.
    url(r'^(?P<entity_slug>[-\w]+)/(?P<slug>[-\w]+)/', include([
        url(r'^$', redirects.SongRedirectView.as_view()),
        url(r'^drukuj/$', redirects.SongRedirectView.as_view()),
    ])),
]
