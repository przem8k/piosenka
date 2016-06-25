from django.test import TestCase
from django.core.urlresolvers import reverse

from base import testing
from articles.models import Article
from blog.models import Post
from events.models import Event
from songs.models import Song


class SiteUrlTest(TestCase):

    def test_site_urls(self):
        response = testing.get_public_client().get(reverse('index'))
        self.assertEqual(200, response.status_code)
        response = testing.get_public_client().get(reverse('about'))
        self.assertEqual(200, response.status_code)

    def test_to_review(self):
        login_url = reverse('hello') + '?next=' + reverse('to_review')
        response = testing.get_public_client().get(reverse('to_review'))
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, login_url)

        response = testing.get_user_client().get(reverse('to_review'))
        self.assertEqual(403, response.status_code)

        user = testing.create_user(perms=['content.review'])
        response = testing.get_user_client(user).get(reverse('to_review'))
        self.assertEqual(200, response.status_code)

    def test_public_menu(self):
        response = testing.get_public_client().get(reverse('index'))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, reverse('hello'), html=False)
        self.assertNotContains(response, reverse('goodbye'), html=False)

    def test_user_menu(self):
        response = testing.get_user_client().get(reverse('index'))
        self.assertEqual(200, response.status_code)
        self.assertNotContains(response, reverse('hello'), html=False)
        self.assertContains(response, reverse('goodbye'), html=False)
        self.assertNotContains(response, reverse('add_article'), html=False)
        self.assertNotContains(response, reverse('add_event'), html=False)
        self.assertNotContains(response, reverse('add_post'), html=False)
        self.assertNotContains(response, reverse('add_song'), html=False)

        user = testing.create_user(perms=[Article.permstring()])
        response = testing.get_user_client(user).get(reverse('index'))
        self.assertEqual(200, response.status_code)
        self.assertNotContains(response, reverse('hello'), html=False)
        self.assertContains(response, reverse('goodbye'), html=False)
        self.assertContains(response, reverse('add_article'), html=False)
        self.assertNotContains(response, reverse('add_event'), html=False)
        self.assertNotContains(response, reverse('add_post'), html=False)
        self.assertNotContains(response, reverse('add_song'), html=False)

        user = testing.create_user(perms=[Event.permstring()])
        response = testing.get_user_client(user).get(reverse('index'))
        self.assertEqual(200, response.status_code)
        self.assertNotContains(response, reverse('hello'), html=False)
        self.assertContains(response, reverse('goodbye'), html=False)
        self.assertNotContains(response, reverse('add_article'), html=False)
        self.assertContains(response, reverse('add_event'), html=False)
        self.assertNotContains(response, reverse('add_post'), html=False)
        self.assertNotContains(response, reverse('add_song'), html=False)

        user = testing.create_user(perms=[Post.permstring()])
        response = testing.get_user_client(user).get(reverse('index'))
        self.assertEqual(200, response.status_code)
        self.assertNotContains(response, reverse('hello'), html=False)
        self.assertContains(response, reverse('goodbye'), html=False)
        self.assertNotContains(response, reverse('add_article'), html=False)
        self.assertNotContains(response, reverse('add_event'), html=False)
        self.assertContains(response, reverse('add_post'), html=False)
        self.assertNotContains(response, reverse('add_song'), html=False)

        user = testing.create_user(perms=[Song.permstring()])
        response = testing.get_user_client(user).get(reverse('index'))
        self.assertEqual(200, response.status_code)
        self.assertNotContains(response, reverse('hello'), html=False)
        self.assertContains(response, reverse('goodbye'), html=False)
        self.assertNotContains(response, reverse('add_article'), html=False)
        self.assertNotContains(response, reverse('add_event'), html=False)
        self.assertNotContains(response, reverse('add_post'), html=False)
        self.assertContains(response, reverse('add_song'), html=False)

        user = testing.create_user(perms=[Article.permstring(),
                                          Event.permstring(), Post.permstring(),
                                          Song.permstring()])
        response = testing.get_user_client(user).get(reverse('index'))
        self.assertEqual(200, response.status_code)
        self.assertNotContains(response, reverse('hello'), html=False)
        self.assertContains(response, reverse('goodbye'), html=False)
        self.assertContains(response, reverse('add_article'), html=False)
        self.assertContains(response, reverse('add_event'), html=False)
        self.assertContains(response, reverse('add_post'), html=False)
        self.assertContains(response, reverse('add_song'), html=False)
