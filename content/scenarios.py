""" Test-scenarios mixins to be shared among tests for concrete content types.
"""

from django.core.urlresolvers import reverse


class ContentTestScenarios(object):

    def content_review(self, cls):
        """ Tests the review helper view. """
        # Add a new item.
        item = cls.create_for_testing()
        item.author = self.user_alice
        item.save()
        self.assertFalse(item.is_live())

        # Verify that anonymous user is redirected to login.
        response = self.get(item.get_review_url())
        self.assertEqual(302, response.status_code)
        self.assertTrue(reverse('hello') in response.url)

        # Alice should be redirected to the actual item with some informative
        # message.
        response = self.get_client(self.user_alice).get(item.get_review_url(),
                                                        follow=True)
        self.assertRedirects(response, item.get_absolute_url())
        self.assertTrue('messages' in response.context)
        self.assertEqual(1, len(response.context['messages']))

        # Bob should be redirected too.
        response = self.get_client(self.user_bob).get(item.get_review_url(),
                                                      follow=True)
        self.assertRedirects(response, item.get_absolute_url())
        self.assertTrue('messages' in response.context)
        self.assertEqual(1, len(response.context['messages']))

        # And the valid approver too.
        response = self.get_client(self.user_approver_zoe).get(
            item.get_review_url(), follow=True)
        self.assertRedirects(response, item.get_absolute_url())
        self.assertTrue('messages' in response.context)
        self.assertEqual(1, len(response.context['messages']))

        # And the valid approver after the item is live too.
        item.reviewed = True
        item.save()
        response = self.get_client(self.user_approver_zoe).get(
            item.get_review_url(), follow=True)
        self.assertRedirects(response, item.get_absolute_url())
        self.assertTrue('messages' in response.context)
        self.assertEqual(1, len(response.context['messages']))

    def content_approve(self, cls):
        """ Tests the review helper view. """
        # Add a new item.
        item = cls.create_for_testing()
        item.author = self.user_alice
        item.save()
        self.assertFalse(item.is_live())

        # Verify that the general public can't access the item.
        response = self.get(item.get_absolute_url())
        self.assertEqual(404, response.status_code)

        # Try to approve the item - Alice can't, she's the author.
        response = self.get(item.get_approve_url(), self.user_alice)
        self.assertEqual(404, response.status_code)
        item.refresh_from_db()
        self.assertFalse(item.is_live())

        # Try to approve the item - Bob can't, he's not staff.
        response = self.get(item.get_approve_url(), self.user_bob)
        self.assertEqual(404, response.status_code)
        item.refresh_from_db()
        self.assertFalse(item.is_live())

        # Try to approve the item - approver can and does.
        response = self.get(item.get_approve_url(), self.user_approver_zoe)
        self.assertEqual(302, response.status_code)
        item.refresh_from_db()
        self.assertTrue(item.is_live())

        # Verify what happens now that the item is approved.
        response = self.get(item.get_absolute_url())
        self.assertEqual(200, response.status_code)

        # Now that the item is approved, there should be no approve link.
        response = self.get(item.get_absolute_url(), self.user_approver_zoe)
        self.assertEqual(200, response.status_code)
