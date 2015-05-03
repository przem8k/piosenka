from django.contrib.auth.models import User
from django.test import TestCase

from articles.models import Article
from content.trevor import put_text_in_trevor


class ArticleTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="bob", email="bob@example.com",
                                             password="secret")
        self.user.save()

    def test_slug(self):
        article = self.make_test_article()
        article.title = "Krótka historia pewnej piosenki"

        # Verify that the slug is empty before saving.
        self.assertEqual("", article.slug)

        # Save and verify that the slug was correctly set.
        article.save()
        self.assertEqual("krotka-historia-pewnej-piosenki", article.slug)

        # Change the title and verify that the slug didn't change.
        article.title = "Zupełnie inny tytuł"
        article.save()
        self.assertEqual("krotka-historia-pewnej-piosenki", article.slug)

    def test_pub_date(self):
        article = self.make_test_article()

        self.assertIsNone(article.pub_date)
        article.save()
        self.assertIsNotNone(article.pub_date)

    def make_test_article(self):
        article = Article()
        article.title = "Article on something."
        article.lead_text_trevor = put_text_in_trevor("abc")
        article.main_text_trevor = put_text_in_trevor("abc")
        article.author = self.user
        return article
