from django.conf.urls import patterns, url

from events.views import *

urlpatterns = patterns(
    '',
    url(r'^$', EventIndex.as_view(), name="event_index"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', MonthArchiveRedirect.as_view(),
        name="event_month_redirect"),
    url(r'^(?P<year>\d{4})/$', YearArchive.as_view(),
        name="event_year"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        EventDetail.as_view(), name="event_detail"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/edytuj/$',
        EditEvent.as_view(), name="edit_event"),
    url(r'^dodaj/$', AddEvent.as_view(), name="add_event"),
    url(r'^wykonawca/(?P<slug>[-\w]+)/$', EntityDetail.as_view(), name="entity_gigs"),
    url(r'^(?P<slug>[-\w]+)/$', VenueDetail.as_view(), name="venue_detail"),
)
