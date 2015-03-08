import uuid

from django.contrib.auth.models import User
from django.test import Client, TestCase

from blog.models import Post
from articles.models import Article
from artists.models import Entity
from events.models import Event, Venue
from songs.models import EntityContribution, Song

PASS = "secret"
EMAIL = "example@example.com"
NAME_LEN = 20


class PiosenkaTestCase(TestCase):
    """ Creates two non-staff users:
     - user_alice
     - user_bob
     and two staff users:
     - user_approver_zoe
     - user_approver_jake
    """
    def get(self, url, user=None):
        return self.get_client(user).get(url)

    def get_client(self, user=None):
        c = Client()
        if user:
            c.login(username=user.username, password=PASS)
        return c

    def create_user_for_testing(self):
        name = str(uuid.uuid4()).replace("-", "")[:NAME_LEN]
        return User.objects.create_user(username=name,
                                        email=EMAIL,
                                        password=PASS)

    def setUp(self):
        super().setUp()
        self.user_alice = self.create_user_for_testing()
        self.user_bob = self.create_user_for_testing()
        self.user_approver_zoe = self.create_user_for_testing()
        self.user_approver_zoe.is_staff = True
        self.user_approver_zoe.save()
        self.user_approver_jake = self.create_user_for_testing()
        self.user_approver_jake.is_staff = True
        self.user_approver_jake.save()

    def new_article(self, author_user):
        article = Article.create_for_testing()
        article.author = author_user
        article.save()
        return article

    def new_event(self, venue, author_user):
        event = Event.create_for_testing()
        event.venue = venue
        event.author = author_user
        event.save()
        return event

    def new_venue(self):
        venue = Venue.create_for_testing()
        venue.save()
        return venue

    def new_post(self, author_user):
        post = Post.create_for_testing()
        post.author = author_user
        post.save()
        return post

    def new_song(self, author_user):
        song = Song.create_for_testing()
        song.author = author_user
        song.save()
        return song

    def new_entity(self):
        entity = Entity.create_for_testing()
        entity.save()
        return entity

    def add_contribution(self, song, entity, performed=False, texted=False,
                         translated=False, composed=False):
        contribution = EntityContribution()
        contribution.song = song
        contribution.entity = entity
        contribution.performed = performed
        contribution.texted = texted
        contribution.translated = translated
        contribution.composed = composed
        contribution.save()
