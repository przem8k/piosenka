from django.test import TestCase
from django.urls import reverse

from base import testing
from base.overrides import overrides
from content.generic_tests import GenericTestsMixin
from songs.models import Artist, EntityContribution, Song


class SongTest(GenericTestsMixin, TestCase):
    item_cls = Song

    @overrides(GenericTestsMixin)
    def get_add_url(self):
        return reverse("add_song")

    def test_add_song(self):
        user = testing.create_user()
        artist = Artist.create_for_testing(user)
        artist.reviewed = True
        artist.save()

        data = {
            "title": "wlazlkotek",
            "capo_fret": 0,
            "lyrics": "wlazl kotek na plotek",
            "entitycontribution_set-TOTAL_FORMS": 1,
            "entitycontribution_set-INITIAL_FORMS": 0,
            "entitycontribution_set-MIN_NUM_FORMS": 1,
            "entitycontribution_set-MAX_NUM_FORMS": 1000,
            "entitycontribution_set-0-artist": artist.pk,
            "entitycontribution_set-0-texted": True,
        }
        response = testing.get_user_client(user=user).post(
            reverse("add_song"), data=data
        )
        self.assertRedirects(response, "/opracowanie/" + artist.name + "-wlazlkotek/")
        song = Song.objects.get(title="wlazlkotek")
        self.assertEqual("wlazl kotek na plotek", song.lyrics)
