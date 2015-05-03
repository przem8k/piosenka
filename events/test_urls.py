from django.core.urlresolvers import reverse

from events.models import Event
from piosenka.testing import PiosenkaTestCase


class EventUrlTest(PiosenkaTestCase):
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

    def test_approve_event(self):
        venue = self.new_venue()
        event = self.new_event(venue, self.user_alice)

        # Verify that the general public can't access the event.
        self.assertFalse(event.is_live())
        response = self.get(event.get_absolute_url())
        self.assertEqual(404, response.status_code)

        # Try to approve the event - Alice can't, she's the author.
        response = self.get(event.get_approve_url(), self.user_alice)
        self.assertEqual(404, response.status_code)
        event = Event.objects.get(id=event.id)  # Refresh from db.
        self.assertFalse(event.is_live())

        # Try to approve the event - Bob can't, he's not staff.
        response = self.get(event.get_approve_url(), self.user_bob)
        self.assertEqual(404, response.status_code)
        event = Event.objects.get(id=event.id)  # Refresh from db.
        self.assertFalse(event.is_live())

        # Try to approve the event - approver can and does.
        response = self.get(event.get_approve_url(), self.user_approver_zoe)
        self.assertEqual(302, response.status_code)
        event = Event.objects.get(id=event.id)  # Refresh from db.
        self.assertTrue(event.is_live())

        # Verify what happens now that the event is approved.
        response = self.get(event.get_absolute_url())
        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context['can_edit'])
        self.assertFalse(response.context['can_approve'])
