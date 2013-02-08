from django.conf.urls.defaults import *

from events.views import *

urlpatterns = patterns('',
    url(r'^$', EventIndex.as_view(), name="event_index"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', EventMonthArchive.as_view(), name="event_month_archive"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', EventDetail.as_view(), name="event_detail"),
    url(r'^(?P<slug>[-\w]+)/$', VenueDetail.as_view(), name="venue_detail"),
)
