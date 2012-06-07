from django.conf.urls.defaults import *
from events.views import *
from events.models import Event

events_index_setup = {
    'queryset': Event.current.all(),
    'template_object_name': 'event',
}

urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^$', 'object_list', events_index_setup, name='current-events'),
)

events_date_setup = {
    'queryset': Event.objects.all(),
    'date_field': 'datetime',
    'allow_future': True,
    'month_format': "%m",
    'template_object_name': 'event',
}

urlpatterns += patterns('django.views.generic.date_based',
    url(r'^(?P<year>\d{4})/$', 'archive_year', events_date_setup, name="events-yearly-archive"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'archive_month', events_date_setup, name="events-monthly-archive"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 'object_detail', events_date_setup, name="event"),
)
