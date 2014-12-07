from django.contrib.auth.models import User
from django.test import TestCase

from articles.models import Article
from frontpage.trevor import put_text_in_trevor


class ArticleTest(TestCase):
    def test_slug(self):
        author = User.objects.create_user(username="bob", email="bob@example.com",
                                          password="secret")
        author.save()

        article = Article()
        article.title = "Krótka historia pewnej piosenki"
        article.lead_text_trevor = put_text_in_trevor("Lead part.")
        article.main_text_trevor = put_text_in_trevor("Main part.")
        article.author = author

        self.assertEqual("", article.slug)
        article.save()
        self.assertEqual("krotka-historia-pewnej-piosenki", article.slug)

        # Change the title and verify that the slug didn't change.
        article.title = "Zupełnie inny tytuł"
        article.save()
        self.assertEqual("krotka-historia-pewnej-piosenki", article.slug)
