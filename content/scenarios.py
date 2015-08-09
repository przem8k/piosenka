""" Test-scenarios mixins to be shared among tests for concrete content types.
"""

from django.core.urlresolvers import reverse

from base import testing


class TestScenariosMixin(object):
    """This is intended to be used in a TestCase implementation, so that
    self.assertXyz() functions are available.
    """

    def content_review(self, cls):
        """ Tests the review helper view. """
        # Add a new item.
        author = testing.create_user()
        item = cls.create_for_testing(author)
        self.assertFalse(item.is_live())

        # Verify that anonymous user is redirected to login.
        response = testing.get_public_client().get(item.get_review_url())
        self.assertEqual(302, response.status_code)
        self.assertTrue(reverse('hello') in response.url)

        # The author should be redirected to the actual item with some
        # informative message.
        response = testing.get_client(author).get(
            item.get_review_url(), follow=True)
        self.assertRedirects(response, item.get_absolute_url())
        self.assertTrue('messages' in response.context)
        self.assertEqual(1, len(response.context['messages']))

        # Another regular user should be redirected too.
        response = testing.get_user_client().get(item.get_review_url(),
                                                 follow=True)
        self.assertRedirects(response, item.get_absolute_url())
        self.assertTrue('messages' in response.context)
        self.assertEqual(1, len(response.context['messages']))

        # And the valid approver too.
        reviewer = testing.create_user(perms=['content.review'])
        response = testing.get_client(reviewer).get(
            item.get_review_url(), follow=True)
        self.assertRedirects(response, item.get_absolute_url())
        self.assertTrue('messages' in response.context)
        self.assertEqual(1, len(response.context['messages']))

        # After the item is live too.
        item.reviewed = True
        item.save()
        response = testing.get_client(reviewer).get(item.get_review_url(),
                                                    follow=True)
        self.assertRedirects(response, item.get_absolute_url())
        self.assertTrue('messages' in response.context)
        self.assertEqual(1, len(response.context['messages']))

    def content_approve(self, cls):
        """ Tests the review helper view. """
        # Add a new item.
        author = testing.create_user()
        item = cls.create_for_testing(author)
        self.assertFalse(item.is_live())

        # Verify that the general public can't access the item.
        response = testing.get_public_client().get(item.get_absolute_url())
        self.assertEqual(404, response.status_code)

        # Try to approve the item - the author can't do that.
        response = testing.get_user_client(author).get(
            item.get_approve_url())
        self.assertEqual(404, response.status_code)
        item.refresh_from_db()
        self.assertFalse(item.is_live())

        # Try to approve the item - another regular user cannot.
        response = testing.get_user_client().get(item.get_approve_url())
        self.assertEqual(404, response.status_code)
        item.refresh_from_db()
        self.assertFalse(item.is_live())

        # Try to approve the item - reviewer can and does.
        reviewer = testing.create_user(perms=['content.review'])
        response = testing.get_user_client(reviewer).get(item.get_approve_url())
        self.assertEqual(302, response.status_code)
        item.refresh_from_db()
        self.assertTrue(item.is_live())

        # General public should now be able to access the item.
        response = testing.get_public_client().get(item.get_absolute_url())
        self.assertEqual(200, response.status_code)

        # The reviewer should still be able to access the item. Ideally we'd
        # verify that the 'approve' link is no longer displayed here anymore.
        response = testing.get_user_client(reviewer).get(
            item.get_absolute_url())
        self.assertEqual(200, response.status_code)
