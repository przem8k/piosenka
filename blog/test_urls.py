from django.core.urlresolvers import reverse

from blog.models import Post
from piosenka.testing import PiosenkaTestCase


class PostUrlTest(PiosenkaTestCase):
    def test_blog_index(self):
        response = self.get(reverse('post_index'))
        self.assertEqual(200, response.status_code)

        post_a = self.new_post(self.user_alice)
        post_a.reviewed = True
        post_a.save()

        post_b = self.new_post(self.user_alice)
        post_b.reviewed = False
        post_b.save()

        response = self.get(reverse('post_index'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.context['all_posts']))

        response = self.get(reverse('post_index'), self.user_alice)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context['all_posts']))

        response = self.get(reverse('post_index'), self.user_bob)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context['all_posts']))

    def test_approve_post(self):
        post = self.new_post(self.user_alice)
        self.assertFalse(post.is_live())

        # Verify that the general public can't access the post.
        response = self.get(post.get_absolute_url())
        self.assertEqual(404, response.status_code)

        # Try to approve the post - Alice can't, she's the author.
        response = self.get(post.get_approve_url(), self.user_alice)
        self.assertEqual(404, response.status_code)
        post = Post.objects.get(id=post.id)  # Refresh from db.
        self.assertFalse(post.is_live())

        # Try to approve the post - Bob can't, he's not staff.
        response = self.get(post.get_approve_url(), self.user_bob)
        self.assertEqual(404, response.status_code)
        post = Post.objects.get(id=post.id)  # Refresh from db.
        self.assertFalse(post.is_live())

        # Try to approve the post - approver can and does.
        response = self.get(post.get_approve_url(), self.user_approver_zoe)
        self.assertEqual(301, response.status_code)
        post = Post.objects.get(id=post.id)  # Refresh from db.
        self.assertTrue(post.is_live())

        # Verify what happens now that the post is approved.
        response = self.get(post.get_absolute_url())
        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context['can_edit'])
        self.assertFalse(response.context['can_approve'])

    def test_review_post(self):
        """ Tests the review helper view. """
        # Add a new post.
        post = self.new_post(self.user_alice)
        self.assertFalse(post.is_live())

        # Verify that anonymous user is redirected to login.
        response = self.get(post.get_review_url())
        self.assertEqual(302, response.status_code)
        self.assertTrue(reverse('hello') in response.url)

        # Alice should be redirected to the actual post with some informative
        # message.
        response = self.get_client(self.user_alice).get(post.get_review_url(),
                                                        follow=True)
        self.assertRedirects(response, post.get_absolute_url(), status_code=301)
        self.assertTrue('messages' in response.context)
        self.assertEqual(1, len(response.context['messages']))

        # Bob should be redirected too.
        response = self.get_client(self.user_bob).get(post.get_review_url(),
                                                      follow=True)
        self.assertRedirects(response, post.get_absolute_url(), status_code=301)
        self.assertTrue('messages' in response.context)
        self.assertEqual(1, len(response.context['messages']))

        # And the valid approver too.
        response = self.get_client(self.user_approver_zoe).get(
                post.get_review_url(), follow=True)
        self.assertRedirects(response, post.get_absolute_url(), status_code=301)
        self.assertTrue('messages' in response.context)
        self.assertEqual(1, len(response.context['messages']))

        # And the valid approver after the post is live too.
        post.reviewed = True
        post.save()
        response = self.get_client(self.user_approver_zoe).get(
                post.get_review_url(), follow=True)
        self.assertRedirects(response, post.get_absolute_url(), status_code=301)
        self.assertTrue('messages' in response.context)
        self.assertEqual(1, len(response.context['messages']))
