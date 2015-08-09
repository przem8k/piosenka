from django.core.urlresolvers import reverse
from django.test import TestCase

from artists.models import Entity
from base import testing
from content.scenarios import TestScenariosMixin
from songs.models import EntityContribution, Song


class SongUrlTest(TestScenariosMixin, TestCase):
    def add_contribution(self, song, entity, performed=False, texted=False,
                         translated=False, composed=False):
        contribution = EntityContribution()
        contribution.song = song
        contribution.entity = entity
        contribution.performed = performed
        contribution.texted = texted
        contribution.translated = translated
        contribution.composed = composed
        contribution.save()

    def test_songbook_index(self):
        response = testing.get_public_client().get(reverse('songbook'))
        self.assertEqual(200, response.status_code)

    def test_entity_index(self):
        author = testing.create_user()
        jack_white = Entity.create_for_testing()
        seven_nations_army = Song.create_for_testing(author)
        self.add_contribution(seven_nations_army, jack_white, True)
        jolene = Song.create_for_testing(author)
        self.add_contribution(jolene, jack_white, True)

        # Approve only Jolene.
        seven_nations_army.reviewed = False
        seven_nations_army.save()
        jolene.reviewed = True
        jolene.save()

        # General public should see only Jolene.
        response = testing.get_public_client().get(
            jack_white.get_absolute_url())
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.context['songs']))

        # The author should see both.
        response = testing.get_user_client(author).get(
            jack_white.get_absolute_url())
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context['songs']))

        # Any logged-in user should see both, too.
        response = testing.get_user_client().get(jack_white.get_absolute_url())
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context['songs']))

    def test_add_song(self):
        # General public can't access the add_song view.
        response = testing.get_public_client().get(reverse('add_song'))
        self.assertEqual(302, response.status_code)

        # Signed in user should be able to access it just fine.
        response = testing.get_user_client().get(reverse('add_song'))
        self.assertEqual(200, response.status_code)

    def test_view_new_song(self):
        author = testing.create_user()
        entity = Entity.create_for_testing()
        song = Song.create_for_testing(author)
        self.add_contribution(song, entity, True, True)
        song.save()

        # Verify that the general public can't access the song.
        self.assertFalse(song.is_live())
        response = testing.get_public_client().get(song.get_absolute_url())
        self.assertEqual(404, response.status_code)

        # Verify what happens when the author does.
        response = testing.get_user_client(author).get(song.get_absolute_url())
        self.assertEqual(200, response.status_code)

        # Verify what happens when another user does.
        response = testing.get_user_client().get(song.get_absolute_url())
        self.assertEqual(200, response.status_code)

    def test_edit_song(self):
        author = testing.create_user()
        entity = Entity.create_for_testing()
        song = Song.create_for_testing(author)
        self.add_contribution(song, entity, True, True)
        song.save()

        response = testing.get_public_client().get(song.get_edit_url())
        self.assertEqual(302, response.status_code)

        response = testing.get_user_client(author).get(song.get_edit_url())
        self.assertEqual(200, response.status_code)

    def test_review_song(self):
        self.content_review(Song)

    def test_approve_song(self):
        self.content_approve(Song)
