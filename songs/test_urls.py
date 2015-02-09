from django.core.urlresolvers import reverse

from songs.models import EntityContribution, Song
from artists.models import Entity
from piosenka.models import ContentItem
from piosenka.url_test_case import UrlTestCase


class SongUrlTest(UrlTestCase):
    def setUp(self):
        self.user_alice = self.create_user_for_testing()
        self.user_bob = self.create_user_for_testing()

    def new_song(self, author_user):
        song = Song.create_for_testing()
        song.author = author_user
        song.save()
        return song

    def new_entity(self):
        entity = Entity.create_for_testing()
        entity.save()
        return entity

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
        response = self.get(reverse('songbook_entity',
                                    kwargs={'slug': jack_white.slug}))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.context['songs']))

        # Any logged-in used should see both.
        response = self.get(reverse('songbook_entity',
                                    kwargs={'slug': jack_white.slug}),
                            self.user_bob)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context['songs']))

        # Ditto.
        response = self.get(reverse('songbook_entity',
                                    kwargs={'slug': jack_white.slug}),
                            self.user_alice)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context['songs']))

    def test_view_new_song(self):
        entity = self.new_entity()
        song = self.new_song(self.user_alice)
        self.add_contribution(song, entity, True, True)
        song.save()

        # Verify that the general public can't access the song.
        self.assertFalse(song.is_live())
        response = self.get(reverse('song', kwargs={'slug': song.slug}))
        self.assertEqual(404, response.status_code)

        # Verify what happens when the author does.
        response = self.get(reverse('song', kwargs={'slug': song.slug}),
                            self.user_alice)
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.context['can_edit'])
        self.assertFalse(response.context['can_moderate'])

        # Verify what happens when another author does.
        response = self.get(reverse('song', kwargs={'slug': song.slug}),
                            self.user_bob)
        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context['can_edit'])
        self.assertFalse(response.context['can_moderate'])

        # Approve the song and verify that it's accessible to anyone.
        song.reviewed = True
        song.save()
        response = self.get(reverse('song', kwargs={'slug': song.slug}))
        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context['can_edit'])
        self.assertFalse(response.context['can_moderate'])

    def test_edit_song(self):
        entity = self.new_entity()
        song = self.new_song(self.user_alice)
        self.add_contribution(song, entity, True, True)
        song.save()

        response = self.get(reverse('edit_song',
                                    kwargs={'slug': song.slug}))
        self.assertEqual(302, response.status_code)

        response = self.get(reverse('edit_song',
                                    kwargs={'slug': song.slug}),
                            self.user_alice)
        self.assertEqual(200, response.status_code)
