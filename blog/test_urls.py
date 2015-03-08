from django.core.urlresolvers import reverse

from blog.models import Post
from piosenka.url_test_case import UrlTestCase


class PostUrlTest(UrlTestCase):
    def new_post(self, author_user):
        post = Post.create_for_testing()
        post.author = author_user
        post.save()
        return post

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

        # Verify that the general public can't access the post.
        self.assertFalse(post.is_live())
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
