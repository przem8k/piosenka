from django.core.urlresolvers import reverse

from articles.models import Article
from piosenka.testing import PiosenkaTestCase


class ArticleUrlTest(PiosenkaTestCase):
    def test_article_index(self):
        response = self.get(reverse('articles'))
        self.assertEqual(200, response.status_code)

        article_a = self.new_article(self.user_alice)
        article_a.reviewed = True
        article_a.save()

        article_b = self.new_article(self.user_alice)
        article_b.reviewed = False
        article_b.save()

        response = self.get(reverse('articles'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.context['articles']))

        response = self.get(reverse('articles'), self.user_alice)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context['articles']))

        response = self.get(reverse('articles'), self.user_bob)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context['articles']))

    def test_view_new_article(self):
        article = self.new_article(self.user_alice)

        # Verify that the general public can't access the article.
        self.assertFalse(article.is_live())
        response = self.get(article.get_absolute_url())
        self.assertEqual(404, response.status_code)

        # Verify what happens when the author does.
        response = self.get(article.get_absolute_url(), self.user_alice)
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.context['can_edit'])
        self.assertFalse(response.context['can_approve'])

        # Verify what happens when another author does.
        response = self.get(article.get_absolute_url(), self.user_bob)
        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context['can_edit'])
        self.assertFalse(response.context['can_approve'])

    def test_approve_article(self):
        article = self.new_article(self.user_alice)

        # Verify that the general public can't access the article.
        self.assertFalse(article.is_live())
        response = self.get(article.get_absolute_url())
        self.assertEqual(404, response.status_code)

        # Try to approve the article - Alice can't, she's the author.
        response = self.get(article.get_approve_url(), self.user_alice)
        self.assertEqual(404, response.status_code)
        article = Article.objects.get(id=article.id)  # Refresh from db.
        self.assertFalse(article.is_live())

        # Try to approve the article - Bob can't, he's not staff.
        response = self.get(article.get_approve_url(), self.user_bob)
        self.assertEqual(404, response.status_code)
        article = Article.objects.get(id=article.id)  # Refresh from db.
        self.assertFalse(article.is_live())

        # Try to approve the article - approver can and does.
        response = self.get(article.get_approve_url(), self.user_approver_zoe)
        self.assertEqual(301, response.status_code)
        article = Article.objects.get(id=article.id)  # Refresh from db.
        self.assertTrue(article.is_live())

        # Verify what happens now that the article is approved.
        response = self.get(article.get_absolute_url())
        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context['can_edit'])
        self.assertFalse(response.context['can_approve'])
