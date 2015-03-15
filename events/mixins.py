from datetime import datetime

from django.db.models import Count

from artists.models import Entity
from events.models import Event
from events.models import Venue


class EventMenuMixin(object):
    """ Populates the context needed for events/menu.html. """
    VENUE_COUNT = 10
    ENTITY_COUNT = 10

    def get_year_span(self):
        cur = datetime.now().year
        earliest = Event.objects.first().datetime.year if Event.objects.first() else cur
        return [x for x in range(cur, earliest - 1, -1)]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['years'] = EventMenuMixin.get_year_span(self)
        context['popular_venues'] = Venue.objects.all() \
            .annotate(event_count=Count('event')) \
            .order_by('-event_count')[:EventMenuMixin.VENUE_COUNT]
        context['active_entities'] = Entity.objects.all() \
            .annotate(event_count=Count('entityperformance')) \
            .order_by('-event_count')[:EventMenuMixin.ENTITY_COUNT]
        return context
