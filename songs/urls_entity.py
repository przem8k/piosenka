from django.conf.urls import include, url

from songs import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='songbook'),
    url(r'^dodaj/$', views.AddArtist.as_view(), name='add_artist'),
    url(r'^(?P<slug>[-\w]+)/',
        include([
            url(r'^$', views.ViewArtist.as_view(), name='view_artist'),
            url(r'^edytuj/$', views.EditArtist.as_view(), name='edit_artist'),
            url(
                r'^dodaj-adnotacje/$',
                views.AddArtistNote.as_view(),
                name='add_artist_note'),
        ])),
]
