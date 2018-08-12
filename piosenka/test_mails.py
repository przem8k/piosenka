from django.core import mail
from django.test import TestCase

from articles.models import Article
from base import testing
from piosenka.mail import send_item_approved_mail, send_new_to_review_mails


class MailTest(TestCase):

    def test_new_to_review_mails(self):
        author = testing.create_user()
        reviewer_a = testing.create_user(perms=['content.review'])
        testing.create_user(perms=['content.review'])

        # There are two reviewers, both should receive an email about the new
        # article added by Alice.
        article = Article.create_for_testing(author)
        send_new_to_review_mails(article)
        self.assertEqual(len(mail.outbox), 2)

        # Only one email should be sent when an approver adds a new article -
        # only the other one can review it.
        article = Article.create_for_testing(reviewer_a)
        send_new_to_review_mails(article)
        self.assertEqual(len(mail.outbox), 3)

        # https://github.com/ppiet/piosenka/issues/8
        # Set the first reviewers's email to empty - they should now be skipped,
        # but the other reviewer should be notified.
        reviewer_a.email = ''
        reviewer_a.save()
        article = Article.create_for_testing(author)
        send_new_to_review_mails(article)
        self.assertEqual(len(mail.outbox), 4)

    def test_item_approved_mail(self):
        author = testing.create_user()
        reviewer = testing.create_user(perms=['content.review'])
        self.assertEqual(len(mail.outbox), 0)
        article = Article.create_for_testing(author)
        send_item_approved_mail(article, reviewer)
        self.assertEqual(len(mail.outbox), 1)
