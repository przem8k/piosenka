from django.core.urlresolvers import reverse

from content.scenarios import ContentTestScenarios
from songs.models import Song
from piosenka.testing import PiosenkaTestCase


class SongUrlTest(ContentTestScenarios, PiosenkaTestCase):
    def test_songbook_index(self):
        response = self.get(reverse('songbook'))
        self.assertEqual(200, response.status_code)

    def test_entity_index(self):
        jack_white = self.new_entity()
        seven_nations_army = self.new_song(self.user_bob)
        self.add_contribution(seven_nations_army, jack_white, True)
        jolene = self.new_song(self.user_bob)
        self.add_contribution(jolene, jack_white, True)

        # Approve only Jolene.
        seven_nations_army.reviewed = False
        seven_nations_army.save()
        jolene.reviewed = True
        jolene.save()

        # General public should see only Jolene.
        response = self.get(jack_white.get_absolute_url())
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.context['songs']))

        # Any logged-in used should see both.
        response = self.get(jack_white.get_absolute_url(), self.user_bob)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context['songs']))

        # Ditto.
        response = self.get(jack_white.get_absolute_url(), self.user_alice)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context['songs']))

    def test_add_song(self):
        # General public can't access the add_song view.
        response = self.get(reverse('add_song'))
        self.assertEqual(302, response.status_code)

        # Signed in author should be able to access it just fine.
        alice_client = self.get_client(self.user_alice)
        response = alice_client.get(reverse('add_song'))
        self.assertEqual(200, response.status_code)

    def test_view_new_song(self):
        entity = self.new_entity()
        song = self.new_song(self.user_alice)
        self.add_contribution(song, entity, True, True)
        song.save()

        # Verify that the general public can't access the song.
        self.assertFalse(song.is_live())
        response = self.get(song.get_absolute_url())
        self.assertEqual(404, response.status_code)

        # Verify what happens when the author does.
        response = self.get(song.get_absolute_url(), self.user_alice)
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.context['can_edit'])
        self.assertFalse(response.context['can_approve'])

        # Verify what happens when another author does.
        response = self.get(song.get_absolute_url(), self.user_bob)
        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context['can_edit'])
        self.assertFalse(response.context['can_approve'])

    def test_edit_song(self):
        entity = self.new_entity()
        song = self.new_song(self.user_alice)
        self.add_contribution(song, entity, True, True)
        song.save()

        response = self.get(song.get_edit_url())
        self.assertEqual(302, response.status_code)

        response = self.get(song.get_edit_url(), self.user_alice)
        self.assertEqual(200, response.status_code)

    def test_review_song(self):
        self.content_review(Song)

    def test_approve_song(self):
        self.content_approve(Song)
