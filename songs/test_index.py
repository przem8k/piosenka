from django.test import TestCase
from django.urls import reverse

from base import testing
from songs.models import Artist, EntityContribution, Song


class IndexTest(TestCase):
    def add_contribution(
        self,
        song,
        artist,
        performed=False,
        texted=False,
        translated=False,
        composed=False,
    ):
        contribution = EntityContribution()
        contribution.song = song
        contribution.artist = artist
        contribution.performed = performed
        contribution.texted = texted
        contribution.translated = translated
        contribution.composed = composed
        contribution.save()

    def test_songbook_index(self):
        response = testing.get_public_client().get(reverse("songbook"))
        self.assertEqual(200, response.status_code)

    def test_entity_index(self):
        author = testing.create_user()
        jack_white = Artist.create_for_testing(author)
        jack_white.featured = True
        jack_white.save()

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
        response = testing.get_public_client().get(jack_white.get_absolute_url())
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.context["songs"]))

        # The author should see both.
        response = testing.get_user_client(author).get(jack_white.get_absolute_url())
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context["songs"]))

        # Any logged-in user should see both, too.
        response = testing.get_user_client().get(jack_white.get_absolute_url())
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context["songs"]))
