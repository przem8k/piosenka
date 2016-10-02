from django.core.urlresolvers import reverse
from django.test import TestCase

from base import testing
from base.overrides import overrides
from content.generic_tests import GenericTestsMixin
from songs.models import Artist, Song, EntityContribution


class SongTest(GenericTestsMixin, TestCase):
    item_cls = Song

    @overrides(GenericTestsMixin)
    def get_add_url(self):
        return reverse('add_song')

    def add_contribution(self,
                         song,
                         artist,
                         performed=False,
                         texted=False,
                         translated=False,
                         composed=False):
        contribution = EntityContribution()
        contribution.song = song
        contribution.artist = artist
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
        jack_white = Artist.create_for_testing(author)
        jack_white.reviewed = True
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
        response = testing.get_public_client().get(jack_white.get_absolute_url(
        ))
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

    def test_add_song_empty_form(self):
        user = testing.create_user(perms=['songs.contribute_song'])
        data = {
            'entitycontribution_set-TOTAL_FORMS': 1,
            'entitycontribution_set-INITIAL_FORMS': 0,
            'entitycontribution_set-MIN_NUM_FORMS': 1,
            'entitycontribution_set-MAX_NUM_FORMS': 1000,
        }
        response = testing.get_user_client(user=user).post(reverse('add_song'),
                                                           data=data)
        self.assertEqual(200, response.status_code)
        self.assertFormError(response, 'form', 'title',
                             'To pole jest wymagane.')
        self.assertFormError(response, 'form', 'capo_fret',
                             'To pole jest wymagane.')
        self.assertFormError(response, 'form', 'lyrics',
                             'To pole jest wymagane.')
        self.assertFormsetError(response, 'entitycontribution',
                                0, 'artist',
                                'To pole jest wymagane.')
        self.assertFormsetError(response, 'entitycontribution',
                                0, None,
                                'Zaznacz co najmniej jedną rolę artysty.')

    def test_add_song(self):
        user = testing.create_user(perms=['songs.contribute_song'])
        artist = Artist.create_for_testing(user)
        artist.reviewed = True
        artist.save()

        data = {
            'title': 'wlazlkotek',
            'capo_fret': 0,
            'lyrics': 'wlazl kotek na plotek',
            'entitycontribution_set-TOTAL_FORMS': 1,
            'entitycontribution_set-INITIAL_FORMS': 0,
            'entitycontribution_set-MIN_NUM_FORMS': 1,
            'entitycontribution_set-MAX_NUM_FORMS': 1000,
            'entitycontribution_set-0-artist': artist.pk,
            'entitycontribution_set-0-texted': True,
        }
        response = testing.get_user_client(user=user).post(reverse('add_song'),
                                                           data=data)
        self.assertRedirects(response, '/opracowanie/' + artist.name +
                             '-wlazlkotek/')
        song = Song.objects.get(title='wlazlkotek')
        self.assertEqual('wlazl kotek na plotek', song.lyrics)
