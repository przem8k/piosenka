"""
Converts the description field in Markdown to description_trevor.
"""

import json

from django.core.management.base import BaseCommand

from events.models import Event


class Command(BaseCommand):
    help = "Trevorise event descriptions."

    def handle(self, *args, **options):
        for event in Event.objects.all():
            if event.description:
                trevor = {
                    'data': [{
                        "type": "text",
                        "data": {
                            "text": event.description
                        }
                    }]
                }
                event.description_trevor = json.dumps(trevor)
                event.save()
                print("Processed %s." % (event, ))
