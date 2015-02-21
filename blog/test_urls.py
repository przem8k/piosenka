from django.core.urlresolvers import reverse

from blog.models import Post
from piosenka.url_test_case import UrlTestCase


class PostUrlTest(UrlTestCase):
    def setUp(self):
        self.user_mark = self.create_user_for_testing()
        self.user_john = self.create_user_for_testing()

    def new_post(self, author_user):
        post = Post.create_for_testing()
        post.author = author_user
        post.save()
        return post

    def test_blog_index(self):
        response = self.get(reverse('post_index'))
        self.assertEqual(200, response.status_code)

        post_a = self.new_post(self.user_mark)
        post_a.reviewed = True
        post_a.save()

        post_b = self.new_post(self.user_mark)
        post_b.reviewed = False
        post_b.save()


        response = self.get(reverse('post_index'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.context['all_posts']))

        response = self.get(reverse('post_index'), self.user_mark)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context['all_posts']))

        response = self.get(reverse('post_index'), self.user_john)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context['all_posts']))
