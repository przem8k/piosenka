from django.test import TestCase

from songs.models import Annotation
from content.scenarios import TestScenariosMixin


class AnnotationTest(TestScenariosMixin, TestCase):
    item_cls = Annotation
