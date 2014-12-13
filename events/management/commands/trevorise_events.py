"""
Converts the description field in Markdown to description_trevor.
"""

import json

from django.core.management.base import BaseCommand

from events.models import Event
from piosenka.trevor import put_text_in_trevor


class Command(BaseCommand):
    help = "Trevorise event descriptions."

    def handle(self, *args, **options):
        for event in Event.objects.all():
            if event.description:
                event.description_trevor = put_text_in_trevor(event.description)
                event.save()
                print("Processed %s." % (event, ))
