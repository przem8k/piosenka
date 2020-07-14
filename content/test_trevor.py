from django.test import TestCase

from content import trevor


class ContentItemTest(TestCase):
    def test_markdown_rendering(self):
        trevor_data = '{"data":[{"type":"text","data":{"text":"bazinga\\n"}}]}'
        rendered = trevor.render_trevor(trevor_data)

        self.assertEqual(rendered, "<p>bazinga</p>")
