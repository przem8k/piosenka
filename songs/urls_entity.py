from django.urls import include, re_path

from songs import views

urlpatterns = [
    re_path(
        r"^(?P<slug>[-\w]+)/",
        include(
            [
                re_path(r"^$", views.ViewArtist.as_view(), name="view_artist"),
                re_path(r"^edytuj/$", views.EditArtist.as_view(), name="edit_artist"),
                re_path(
                    r"^dodaj-adnotacje/$",
                    views.AddArtistNote.as_view(),
                    name="add_artist_note",
                ),
            ]
        ),
    ),
]
