from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from songs.views import AddSong


class AddSongViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="songeditor", email="example@example.com", password="secret")

    def test_form_display_logged_in(self):
        request = self.factory.get("/opracowanie/dodaj/")
        request.user = self.user

        view = AddSong.as_view()
        response = view(request)
        self.assertEqual(200, response.status_code)

    def test_form_display_no_login(self):
        request = self.factory.get("/opracowanie/dodaj/")
        request.user = AnonymousUser()

        view = AddSong.as_view()
        response = view(request)
        self.assertEqual(302, response.status_code)
