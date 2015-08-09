from django.core.urlresolvers import reverse
from django.test import TestCase

from base import testing
from content.scenarios import TestScenariosMixin
from articles.models import Article


class ArticleUrlTest(TestScenariosMixin, TestCase):
    def test_article_index(self):
        response = testing.get_public_client().get(reverse('articles'))
        self.assertEqual(200, response.status_code)

        author = testing.create_user()
        article_a = Article.create_for_testing(author)
        article_a.reviewed = True
        article_a.save()

        article_b = Article.create_for_testing(author)
        article_b.reviewed = False
        article_b.save()

        response = testing.get_public_client().get(reverse('articles'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.context['articles']))

        response = testing.get_user_client(author).get(reverse('articles'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context['articles']))

        response = testing.get_user_client().get(reverse('articles'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context['articles']))

    def test_view_new_article(self):
        author = testing.create_user()
        article = Article.create_for_testing(author)

        # Verify that the general public can't access the article.
        self.assertFalse(article.is_live())
        response = testing.get_public_client().get(article.get_absolute_url())
        self.assertEqual(404, response.status_code)

        # Verify what happens when the author does.
        response = testing.get_user_client(author).get(
            article.get_absolute_url())
        self.assertEqual(200, response.status_code)

        # Verify what happens when another author does.
        response = testing.get_user_client().get(article.get_absolute_url())
        self.assertEqual(200, response.status_code)

    def test_review_article(self):
        self.content_review(Article)

    def test_approve_article(self):
        self.content_approve(Article)
