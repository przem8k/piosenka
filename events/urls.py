from django.conf.urls import include, url

from content import url_scheme
from events import views

urlpatterns = [
    url(r'^$', views.EventIndex.as_view(), name='event_index'),
    url(
        r'^dodaj/$',
        views.AddExternalEvent.as_view(),
        name='add_external_event'),
    url(
        r'^(?P<pk>\d+)/edytuj',
        views.EditExternalEvent.as_view(),
        name='edit_external_event'),
    url(
        r'^(?P<pk>\d+)/usun',
        views.DeleteExternalEvent.as_view(),
        name='delete_external_event'),
]
