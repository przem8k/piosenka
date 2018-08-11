from django.conf.urls import include, url

from content import url_scheme
from events import views

urlpatterns = [
    url(r'^$', views.EventIndex.as_view(), name='event_index'),
    url(r'^(?P<year>\d{4})/',
        include([
            url(r'^$', views.YearArchiveRedirect.as_view(), name='event_year'),
            url(r'^(?P<month>\d{2})/',
                include([
                    url(
                        r'^$',
                        views.MonthArchiveRedirect.as_view(),
                        name='event_month_redirect'),
                    url(r'^(?P<day>\d{2})/(?P<slug>[-\w]+)/',
                        include(
                            url_scheme.view_edit_review_approve(
                                'event', views.ViewEvent, views.EditEvent,
                                views.ReviewEvent, views.ApproveEvent))),
                ])),
        ])),
    url(r'^dodaj-pelne/$', views.AddEvent.as_view(), name='add_event'),
    url(
        r'^dodaj/$',
        views.AddExternalEvent.as_view(),
        name='add_external_event'),
    url(r'^(?P<pk>\d+)/edytuj', views.EditExternalEvent.as_view(),
        name='edit_external_event'),
    url(r'^(?P<pk>\d+)/usun', views.DeleteExternalEvent.as_view(),
        name='delete_external_event'),
    url(
        r'^wykonawca/(?P<slug>[-\w]+)/$',
        views.ViewPerformerRedirect.as_view(),
        name='view_performer'),
    url(
        r'^(?P<slug>[-\w]+)/$',
        views.VenueDetailRedirect.as_view(),
        name='venue_detail'),
]
