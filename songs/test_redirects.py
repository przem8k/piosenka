"""Tests redirects for obsolete song urls."""

from django.core.urlresolvers import reverse
from django.test import TestCase

from base import testing
from artists.models import Entity
from songs.models import Song, EntityContribution


class SongRedirectTest(TestCase):
    def setUp(self):
        author = testing.create_user()
        song = Song.create_for_testing(author)
        entity = Entity.create_for_testing()
        contribution = EntityContribution()
        contribution.song = song
        contribution.entity = entity
        contribution.texted = True
        contribution.save()

        song.core_slug = "some-old-slug"
        song.reviewed = True
        song.save()

        self.song = song
        self.entity = entity

    def test_two_level_url_redirects(self):
        """Tests the old style two-level urls with entity-slug/song-slug."""
        song = self.song
        entity = self.entity

        old_url = "/spiewnik/%s/%s" % (entity.slug, song.core_slug)
        response = testing.get_public_client().get(old_url, follow=True)
        self.assertRedirects(response, song.get_absolute_url(), status_code=301)

        old_url = "/spiewnik/%s/%s/" % (entity.slug, song.core_slug)
        response = testing.get_public_client().get(old_url, follow=True)
        self.assertRedirects(response, song.get_absolute_url(), status_code=301)

        old_url = "/spiewnik/%s/%s/drukuj" % (entity.slug, song.core_slug)
        response = testing.get_public_client().get(old_url, follow=True)
        self.assertRedirects(response, song.get_absolute_url(), status_code=301)

        old_url = "/spiewnik/%s/%s/drukuj/" % (entity.slug, song.core_slug)
        response = testing.get_public_client().get(old_url, follow=True)
        self.assertRedirects(response, song.get_absolute_url(), status_code=301)

    def test_redirect_by_id(self):
        """Tests evel older urls in form "/songs/song/id"."""
        song = self.song

        old_url = "/songs/song/%d" % (song.pk)
        response = testing.get_public_client().get(old_url, follow=True)
        self.assertRedirects(response, song.get_absolute_url(), status_code=301)

        old_url = "/songs/song/%d/" % (song.pk)
        response = testing.get_public_client().get(old_url, follow=True)
        self.assertRedirects(response, song.get_absolute_url(), status_code=301)

        old_url = "/songs/song/%d/print" % (song.pk)
        response = testing.get_public_client().get(old_url, follow=True)
        self.assertRedirects(response, song.get_absolute_url(), status_code=301)

        old_url = "/songs/song/%d/print/" % (song.pk)
        response = testing.get_public_client().get(old_url, follow=True)
        self.assertRedirects(response, song.get_absolute_url(), status_code=301)

    def test_band_redirects(self):
        """Tests for urls in form "/songs/band/id", which we can't handle."""
        old_url = "/songs/band/12"
        response = testing.get_public_client().get(old_url, follow=True)
        self.assertRedirects(response, reverse('songbook'), status_code=301)

        old_url = "/songs/band/12/"
        response = testing.get_public_client().get(old_url, follow=True)
        self.assertRedirects(response, reverse('songbook'), status_code=301)
