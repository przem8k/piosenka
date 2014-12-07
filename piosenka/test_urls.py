from django.test import Client, TestCase


class SiteUrlTest(TestCase):
    def test_top_level_urls(self):
        self.go("/")
        self.go("/blog/")
        self.go("/spiewnik/")
        self.go("/wydarzenia/")
        self.go("/artykuly/")
        self.go("/o-stronie/")

    def go(self, url):
        c = Client()
        response = c.get(url)
        self.assertEqual(200, response.status_code)
