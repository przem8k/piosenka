from django.test import TestCase

from blog.models import Post


class ContentItemTest(TestCase):
    def test_is_live(self):
        item = Post()

        item.reviewed = False
        self.assertFalse(item.is_live())

        item.reviewed = True
        self.assertTrue(item.is_live())
