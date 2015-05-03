from django.core.urlresolvers import reverse

from content.scenarios import ContentTestScenarios
from events.models import Event
from piosenka.testing import PiosenkaTestCase


class EventUrlTest(ContentTestScenarios, PiosenkaTestCase):
    def test_event_visibility(self):
        response = self.get(reverse('event_index'))
        self.assertEqual(200, response.status_code)

        venue = self.new_venue()

        event_a = self.new_event(venue, self.user_alice)
        event_a.reviewed = True
        event_a.save()

        event_b = self.new_event(venue, self.user_alice)
        event_b.reviewed = False
        event_b.save()

        # The general public should see only the reviewed event.
        response = self.get(reverse('event_index'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.context['events']))

        response = self.get(venue.get_absolute_url())
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.context['events']))

        # The author should see both.
        response = self.get(reverse('event_index'), self.user_alice)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context['events']))

        response = self.get(venue.get_absolute_url(), self.user_alice)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context['events']))

        # Another user should also see both.
        response = self.get(reverse('event_index'), self.user_bob)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context['events']))

        response = self.get(venue.get_absolute_url(), self.user_bob)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context['events']))

    def test_review_event(self):
        self.content_review(Event)

    def test_approve_event(self):
        self.content_approve(Event)
