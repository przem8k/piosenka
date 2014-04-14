"""
Sets author and date on events using admin panel history.
"""

from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from events.models import Event


class Command(BaseCommand):
    help = "Sets autorship on events."

    def handle(self, *args, **options):
        event_type = ContentType.objects.get(app_label="events", model="event")
        for event in Event.objects.all():
            entries = LogEntry.objects.filter(content_type=event_type, action_flag=ADDITION,
                                              object_id=event.pk).order_by("-action_time")
            assert len(entries) == 1
            entry = entries[0]
            event.author = entry.user
            event.date = entry.action_time
            event.save()
            print("%s by %s on %s" % (event, entry.user, entry.action_time))
