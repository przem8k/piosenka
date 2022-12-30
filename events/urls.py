from django.urls import include, re_path

from content import url_scheme
from events import views

urlpatterns = [
    re_path(r"^$", views.EventIndex.as_view(), name="event_index"),
    re_path(r"^dodaj/$", views.AddExternalEvent.as_view(), name="add_external_event"),
    re_path(
        r"^(?P<pk>\d+)/edytuj",
        views.EditExternalEvent.as_view(),
        name="edit_external_event",
    ),
    re_path(
        r"^(?P<pk>\d+)/usun",
        views.DeleteExternalEvent.as_view(),
        name="delete_external_event",
    ),
]
