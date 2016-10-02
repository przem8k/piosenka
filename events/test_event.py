from django.core.urlresolvers import reverse
from django.test import TestCase

from base.overrides import overrides
from content.generic_tests import GenericTestsMixin
from events.models import Event


class EventTest(GenericTestsMixin, TestCase):
    item_cls = Event

    @overrides(GenericTestsMixin)
    def get_add_url(self):
        return reverse('add_event')
