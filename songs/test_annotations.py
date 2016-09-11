from django.test import TestCase

from base import testing
from base.overrides import overrides
from content.scenarios import TestScenariosMixin
from songs.models import Annotation, Artist, Song


class AnnotationTest(TestScenariosMixin, TestCase):
    item_cls = Annotation

    @overrides(TestScenariosMixin)
    def get_add_url(self):
        author = testing.create_user()
        artist = Artist.create_for_testing()
        artist.reviewed = True
        artist.save()
        song = Song.create_for_testing(author)
        song.reviewed = True
        return song.get_add_annotation_url()

    @overrides(TestScenariosMixin)
    def assertServedOk(self, item, response):
        self.assertContains(response, item.get_id(), html=False)

    @overrides(TestScenariosMixin)
    def assertNotServedOk(self, item, response):
        self.assertNotContains(response, item.get_id(), html=False)
