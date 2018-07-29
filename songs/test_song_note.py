from django.test import TestCase

from base import testing
from base.overrides import overrides
from content.trevor import put_text_in_trevor
from content.generic_tests import GenericTestsMixin
from songs.models import SongNote, Artist, Song


class SongNoteTest(GenericTestsMixin, TestCase):
    item_cls = SongNote

    @overrides(GenericTestsMixin)
    def get_add_url(self):
        author = testing.create_user()
        artist = Artist.create_for_testing(author)
        artist.reviewed = True
        artist.save()
        song = Song.create_for_testing(author)
        song.reviewed = True
        song.full_clean()
        song.save()
        return song.get_add_note_url()

    @overrides(GenericTestsMixin)
    def assertServedOk(self, item, response):
        self.assertContains(response, item.get_id(), html=False)

    @overrides(GenericTestsMixin)
    def assertNotServedOk(self, item, response):
        self.assertNotContains(response, item.get_id(), html=False)

    def test_add_song_note(self):
        user = testing.create_user()
        artist = Artist.create_for_testing(user)
        artist.reviewed = True
        artist.full_clean()
        artist.save()

        song = Song.create_for_testing(user)
        song.reviewed = True
        song.full_clean()
        song.save()

        data = {
            'title': 'dalsze losy kotka',
            'text_trevor': put_text_in_trevor('Abc')
        }
        self.assertEqual(len(SongNote.objects.all()), 0)
        response = testing.get_user_client(user=user).post(
            song.get_add_note_url(), data=data)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, song.get_absolute_url())
        self.assertEqual(len(SongNote.objects.all()), 1)

    def test_cannot_add_song_note_if_song_not_reviewed(self):
        user = testing.create_user()
        artist = Artist.create_for_testing(user)
        artist.reviewed = True
        artist.full_clean()
        artist.save()

        song = Song.create_for_testing(user)
        song.reviewed = True
        song.full_clean()
        song.save()

        url = song.get_add_note_url()
        song.reviewed = False
        song.full_clean()
        song.save()

        data = {
            'title': 'dalsze losy kotka',
            'text_trevor': put_text_in_trevor('Abc')
        }
        response = testing.get_user_client(user=user).post(url, data=data)
        self.assertEqual(404, response.status_code)
        self.assertEqual(len(SongNote.objects.all()), 0)

    def test_edit_song_note(self):
        author = testing.create_user()
        note = SongNote.create_for_testing(author)

        data = {'title': 'tytul', 'text_trevor': put_text_in_trevor('CDE')}
        response = testing.get_user_client(user=author).post(
            note.get_edit_url(), data=data)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, note.song.get_absolute_url())
