from django.conf.urls import patterns, url

from events.views import AddEvent, EventIndex, EventMonthArchive, EventDetail, VenueDetail

urlpatterns = patterns(
    '',
    url(r'^$', EventIndex.as_view(), name="event_index"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', EventMonthArchive.as_view(),
        name="event_month_archive"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        EventDetail.as_view(), name="event_detail"),
    url(r'^dodaj/$', AddEvent.as_view(), name="add_event"),
    url(r'^(?P<slug>[-\w]+)/$', VenueDetail.as_view(), name="venue_detail"),
)
