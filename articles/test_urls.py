from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from articles.models import Article

PASS = "secret"


class SongUrlTest(TestCase):
    def setUp(self):
        self.user_mark = User.objects.create_user(
            username="mark", email="example@example.com", password=PASS)
        self.user_john = User.objects.create_user(
            username="john", email="example@example.com", password=PASS)

    def new_article(self, author_user):
        article = Article.create_for_testing()
        article.author = author_user
        article.save()
        return article

    def get(self, url, user=None):
        c = Client()
        if user:
            c.login(username=user.username, password=PASS)
        return c.get(url)

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
