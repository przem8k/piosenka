from django.contrib.auth.models import User
from django.test import TestCase

from articles.models import Article, SongMention
from content.trevor import put_text_in_trevor
from songs.models import Song


class ArticleTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="bob", email="bob@example.com", password="secret"
        )
        self.user.save()

    def test_slug(self):
        article = self.make_test_article()
        article.title = "Krótka historia pewnej piosenki"

        # Verify that the slug is empty before saving.
        self.assertEqual("", article.slug)

        # Save and verify that the slug was correctly set.
        article.full_clean()
        article.save()
        self.assertEqual("krotka-historia-pewnej-piosenki", article.slug)

        # Change the title and verify that the slug didn't change.
        article.title = "Zupełnie inny tytuł"
        article.save()
        self.assertEqual("krotka-historia-pewnej-piosenki", article.slug)

    def test_pub_date(self):
        article = self.make_test_article()

        # TODO: re-enable after default is removed from content/models.py
        # self.assertIsNone(article.pub_date)
        article.save()
        self.assertIsNotNone(article.pub_date)

    def test_song_mentions(self):
        article = Article.create_for_testing(self.user)
        self.assertEqual(self.get_song_mentions_count(), 0)

        # Mentions should not be added until the article is public.
        song_a = Song.create_for_testing(self.user)
        link_a = "[song_a](https://example.com/opracowanie/%s)" % song_a.slug
        article.main_text_trevor = put_text_in_trevor(link_a)
        article.full_clean()
        article.save()
        self.assertEqual(self.get_song_mentions_count(), 0)

        article.reviewed = True
        article.full_clean()
        article.save()
        self.assertEqual(self.get_song_mentions_count(), 1)

        article.main_text_trevor = put_text_in_trevor(link_a + " " + link_a)
        article.full_clean()
        article.save()
        self.assertEqual(self.get_song_mentions_count(), 1)

        song_b = Song.create_for_testing(self.user)
        link_b = "[song_a](https://example.com/opracowanie/%s)" % song_b.slug
        article.main_text_trevor = put_text_in_trevor(link_a + " " + link_b)
        article.save()
        self.assertEqual(self.get_song_mentions_count(), 2)

        song_c = Song.create_for_testing(self.user)
        # This time with a trailing slash.
        link_c = "[song_a](https://example.com/opracowanie/%s/)" % song_c.slug
        article.main_text_trevor = put_text_in_trevor(link_a + " " + link_c)
        article.save()
        self.assertEqual(self.get_song_mentions_count(), 2)

        article.main_text_trevor = put_text_in_trevor("nothing")
        article.save()
        self.assertEqual(self.get_song_mentions_count(), 0)

    def get_song_mentions_count(self):
        return len(SongMention.objects.all())

    def make_test_article(self):
        article = Article()
        article.title = "Article on something."
        article.lead_text_trevor = put_text_in_trevor("abc")
        article.main_text_trevor = put_text_in_trevor("abc")
        article.author = self.user
        return article
