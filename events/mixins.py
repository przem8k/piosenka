from artists.models import Entity
from events.models import Venue


class EventMenuMixin(object):
    """ Populates the context needed for events/menu.html. """
    VENUE_COUNT = 15
    ENTITY_COUNT = 15

    def get_context_data(self, **kwargs):
        context = super(EventMenuMixin, self).get_context_data(**kwargs)
        from django.db.models import Count
        context['popular_venues'] = Venue.objects.all() \
            .annotate(event_count=Count('event')) \
            .order_by('-event_count')[:EventMenuMixin.VENUE_COUNT]
        context['active_entities'] = Entity.objects.all() \
            .annotate(event_count=Count('entityperformance')) \
            .order_by('-event_count')[:EventMenuMixin.ENTITY_COUNT]
        return context
