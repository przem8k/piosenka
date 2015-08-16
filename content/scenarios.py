""" Test-scenarios mixins to be shared among tests for concrete content types.
"""

from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse

from base import testing


class TestScenariosMixin(object):
    """This is intended to be used in a TestCase implementation, so that
    self.assertXyz() functions are available.

    Requires self.item_cls to be set on the object.
    """

    def assertServedOk(self, item, response):
        if self.item_cls.is_card:
            self.assertContains(response, item.get_id(), html=False)
        else:
            self.assertEqual(200, response.status_code)

    def assertNotServedOk(self, item, response):
        if self.item_cls.is_card:
            self.assertNotContains(response, item.get_id(), html=False)
        else:
            self.assertEqual(404, response.status_code)

    def test_get_permstring(self):
        """Verifies that the permission string returned from get_permstring
        exists in the db.
        """
        permstring = self.item_cls.permstring()
        parts = permstring.split('.')
        self.assertEquals(2, len(parts))
        self.assertTrue(Permission.objects.get(content_type__app_label=parts[0],
                                               codename=parts[1]))

    def test_view_new_item(self):
        author = testing.create_user()
        item = self.item_cls.create_for_testing(author)
        item.save()

        # Verify that the general public can't access the item.
        self.assertFalse(item.is_live())
        response = testing.get_public_client().get(item.get_absolute_url())
        self.assertNotServedOk(item, response)

        # Verify that the author can.
        response = testing.get_user_client(author).get(item.get_absolute_url())
        self.assertServedOk(item, response)

        # Verify that another signed-in user can, too.
        response = testing.get_user_client().get(item.get_absolute_url())
        self.assertServedOk(item, response)

    def test_edit_item(self):
        author = testing.create_user()
        item = self.item_cls.create_for_testing(author)

        response = testing.get_public_client().get(item.get_edit_url())
        self.assertEqual(302, response.status_code)

        response = testing.get_user_client(author).get(item.get_edit_url())
        self.assertEqual(200, response.status_code)

    def test_review_item(self):
        """Tests the review helper view."""
        # Add a new item.
        author = testing.create_user()
        item = self.item_cls.create_for_testing(author)
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

    def test_approve_item(self):
        """Tests the approve view."""
        # Add a new item.
        author = testing.create_user()
        item = self.item_cls.create_for_testing(author)
        self.assertFalse(item.is_live())

        # Verify that the general public can't access the item.
        response = testing.get_public_client().get(item.get_absolute_url())
        self.assertNotServedOk(item, response)

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
        self.assertServedOk(item, response)

        # The reviewer should still be able to access the item. Ideally we'd
        # verify that the 'approve' link is no longer displayed here anymore.
        response = testing.get_user_client(reviewer).get(
            item.get_absolute_url())
        self.assertServedOk(item, response)
