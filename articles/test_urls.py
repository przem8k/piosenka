from django.core.urlresolvers import reverse

from articles.models import Article
from piosenka.url_test_case import UrlTestCase


class ArticleUrlTest(UrlTestCase):
    def setUp(self):
        self.user_mark = self.create_user_for_testing()
        self.user_john = self.create_user_for_testing()

    def new_article(self, author_user):
        article = Article.create_for_testing()
        article.author = author_user
        article.save()
        return article

    def test_article_index(self):
        response = self.get(reverse('articles'))
        self.assertEqual(200, response.status_code)

        article_a = self.new_article(self.user_mark)
        article_a.reviewed = True
        article_a.save()

        article_b = self.new_article(self.user_mark)
        article_b.reviewed = False
        article_b.save()


        response = self.get(reverse('articles'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.context['articles']))

        response = self.get(reverse('articles'), self.user_mark)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context['articles']))

        response = self.get(reverse('articles'), self.user_john)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context['articles']))
