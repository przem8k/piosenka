"""
 Command for generating markdown representation from legacy event entries.
"""

from markdown import markdown

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Null"
    def handle(self, *args, **options):
        from events.models import Event
        for event in Event.objects.all():
            event.description_html = markdown(event.description, safe_mode='escape')
            event.save()
            print "Processed event: %s." % (event.name,)
