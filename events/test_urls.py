from django.core.urlresolvers import reverse

from events.models import Event, Venue
from piosenka.url_test_case import UrlTestCase


class EventUrlTest(UrlTestCase):
    def setUp(self):
        self.user_mark = self.create_user_for_testing()
        self.user_john = self.create_user_for_testing()

    def new_event(self, venue, author_user):
        event = Event.create_for_testing()
        event.venue = venue
        event.author = author_user
        event.save()
        return event

    def new_venue(self):
        venue = Venue.create_for_testing();
        venue.save()
        return venue

    def test_event_index(self):
        response = self.get(reverse('event_index'))
        self.assertEqual(200, response.status_code)

        venue = self.new_venue()

        event_a = self.new_event(venue, self.user_mark)
        event_a.reviewed = True
        event_a.save()

        event_b = self.new_event(venue, self.user_mark)
        event_b.reviewed = False
        event_b.save()


        response = self.get(reverse('event_index'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.context['events']))

        response = self.get(reverse('event_index'), self.user_mark)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context['events']))

        response = self.get(reverse('event_index'), self.user_john)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context['events']))
