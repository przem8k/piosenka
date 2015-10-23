from django.conf.urls import include, url

from songs import views
from songs import redirects

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='songbook'),
    url(r'^(?P<slug>[-\w]+)/$', views.ArtistView.as_view(),
        name='view_artist'),
    # Obsolete url redirects.
    url(r'^(?P<entity_slug>[-\w]+)/(?P<slug>[-\w]+)/', include([
        url(r'^$', redirects.SongRedirectView.as_view()),
        url(r'^drukuj/$', redirects.SongRedirectView.as_view()),
        ])),
]
