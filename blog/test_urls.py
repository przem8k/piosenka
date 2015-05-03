from django.core.urlresolvers import reverse

from blog.models import Post
from content.scenarios import ContentTestScenarios
from piosenka.testing import PiosenkaTestCase


class PostUrlTest(ContentTestScenarios, PiosenkaTestCase):
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
        self.content_approve(Post)

    def test_review_post(self):
        self.content_review(Post)
