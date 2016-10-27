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

    def test_add_song_empty_form(self):
        user = testing.create_user()
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
        user = testing.create_user()
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
