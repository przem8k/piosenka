from django.core.urlresolvers import reverse
from django.test import TestCase

from base import testing
from content.scenarios import TestScenariosMixin
from events.models import Event, Venue


class EventUrlTest(TestScenariosMixin, TestCase):
    def test_event_visibility(self):
        response = testing.get_public_client().get(reverse('event_index'))
        self.assertEqual(200, response.status_code)

        author = testing.create_user()
        venue = Venue.create_for_testing()

        event_a = Event.create_for_testing(author, venue)
        event_a.reviewed = True
        event_a.save()

        event_b = Event.create_for_testing(author, venue)
        event_b.reviewed = False
        event_b.save()

        # The general public should see only the reviewed event.
        response = testing.get_public_client().get(reverse('event_index'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.context['events']))

        response = testing.get_public_client().get(venue.get_absolute_url())
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.context['events']))

        # The author should see both.
        response = testing.get_user_client(author).get(reverse('event_index'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context['events']))

        response = testing.get_user_client(author).get(venue.get_absolute_url())
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context['events']))

        # Another regular user should also see both.
        response = testing.get_user_client().get(reverse('event_index'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context['events']))

        response = testing.get_user_client().get(venue.get_absolute_url())
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context['events']))

    def test_review_event(self):
        self.content_review(Event)

    def test_approve_event(self):
        self.content_approve(Event)
