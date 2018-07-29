from django.test import TestCase

from base import testing
from base.overrides import overrides
from content.trevor import put_text_in_trevor
from content.generic_tests import GenericTestsMixin
from songs.models import ArtistNote, Artist


class ArtistNoteTest(GenericTestsMixin, TestCase):
    item_cls = ArtistNote

    @overrides(GenericTestsMixin)
    def get_add_url(self):
        author = testing.create_user()
        artist = Artist.create_for_testing(author)
        artist.featured = True
        artist.save()
        return artist.get_add_note_url()

    @overrides(GenericTestsMixin)
    def assertServedOk(self, item, response):
        self.assertContains(response, item.get_id(), html=False)

    @overrides(GenericTestsMixin)
    def assertNotServedOk(self, item, response):
        self.assertNotContains(response, item.get_id(), html=False)

    def test_add_artist_note(self):
        author = testing.create_user()
        artist = Artist.create_for_testing(author)
        artist.featured = True
        artist.save()

        data = {
            'title': 'cos o artyscie',
            'text_trevor': put_text_in_trevor('Abc')
        }
        self.assertEqual(len(ArtistNote.objects.all()), 0)
        response = testing.get_user_client(user=author).post(
            artist.get_add_note_url(), data=data)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, artist.get_absolute_url())
        self.assertEqual(len(ArtistNote.objects.all()), 1)

    def test_edit_artist_note(self):
        author = testing.create_user()
        note = ArtistNote.create_for_testing(author)

        data = {
            'title': 'cos o artyscie',
            'text_trevor': put_text_in_trevor('CDE')
        }
        response = testing.get_user_client(user=author).post(
            note.get_edit_url(), data=data)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, note.artist.get_absolute_url())
