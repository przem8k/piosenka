from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from songs.models import EntityContribution, Song
from artists.models import Entity


class SongUrlTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="bobfan", email="example@example.com", password="secret")

        self.bob = Entity()
        self.bob.name = "Dulann"
        self.bob.first_name = "Bob"
        self.bob.slug = "bob-dulann"
        self.bob.save()

        self.song_by_bob = Song()
        self.song_by_bob.title = "Oh, Mary!"
        self.song_by_bob.lyrics = "Da da da da da da"
        self.song_by_bob.author = self.user
        self.song_by_bob.save()

        self.add_contribution(self.song_by_bob, self.bob, performed=True, texted=True)

    def test_songbook_index(self):
        self.go(reverse('songbook'))

    def test_entity_index(self):
        self.go(reverse('songbook_entity', kwargs={'slug': self.bob.slug}))

    def test_song_view(self):
        self.go(reverse('song', kwargs={'slug': self.song_by_bob.slug}))

    def test_edit_song_noone(self):
        c = Client()
        response = c.get(reverse('edit_song', kwargs={'slug': self.song_by_bob.slug}))
        self.assertEqual(302, response.status_code)

    def test_edit_song_author(self):
        c = Client()
        c.login(username="bobfan", password="secret")
        response = c.get(reverse('edit_song', kwargs={'slug': self.song_by_bob.slug}))
        self.assertEqual(200, response.status_code)

    def go(self, url):
        c = Client()
        response = c.get(url)
        self.assertEqual(200, response.status_code)

    def add_contribution(self, song, entity, performed=False, texted=False, translated=False,
                         composed=False):
        contribution = EntityContribution()
        contribution.song = song
        contribution.entity = entity
        contribution.performed = performed
        contribution.texted = texted
        contribution.translated = translated
        contribution.composed = composed
        contribution.save()
