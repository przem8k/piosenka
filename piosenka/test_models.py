from django.test import TestCase

from piosenka.models import ContentItem


class ContentItemTest(TestCase):

    def test_is_live(self):
        item = ContentItem()

        item.ready = False
        item.reviewed = False
        self.assertFalse(item.is_live())

        item.ready = True
        item.reviewed = False
        self.assertFalse(item.is_live())

        # Should never happen, but let's allow that for now.
        item.ready = False
        item.reviewed = True
        self.assertFalse(item.is_live())

        item.ready = True
        item.reviewed = True
        self.assertTrue(item.is_live())
