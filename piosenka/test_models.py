from django.test import TestCase

from piosenka.models import ContentItem


class ContentItemTest(TestCase):

    def test_is_live(self):
        item = ContentItem()

        item.reviewed = False
        self.assertFalse(item.is_live())

        item.reviewed = True
        self.assertTrue(item.is_live())
