from django.core.urlresolvers import reverse
from django.test import TestCase

from base import testing
from base.overrides import overrides
from content.scenarios import TestScenariosMixin
from articles.models import Article


class ArticleUrlTest(TestScenariosMixin, TestCase):
    item_cls = Article

    @overrides(TestScenariosMixin)
    def get_add_url(self):
        return reverse('add_article')

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
