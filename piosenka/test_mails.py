from django.core import mail

from piosenka.testing import PiosenkaTestCase
from piosenka.mail import send_new_to_review_mails


class EventUrlTest(PiosenkaTestCase):
    def test_new_to_review_mails(self):
        # There are two reviewers, both should receive an email about the new
        # article added by Alice.
        article = self.new_article(self.user_alice)
        send_new_to_review_mails(article)
        self.assertEqual(len(mail.outbox), 2)

        # Only one email should be sent when an approver adds a new article -
        # only the other one can review it.
        article = self.new_article(self.user_approver_zoe)
        send_new_to_review_mails(article)
        self.assertEqual(len(mail.outbox), 3)

