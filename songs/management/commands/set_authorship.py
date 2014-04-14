"""
Sets author and date on Songs using admin panel history.
"""

from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from songs.models import Song


class Command(BaseCommand):
    help = "Sets autorship on songs."

    def handle(self, *args, **options):
        song_type = ContentType.objects.get(app_label="songs", model="song")
        for song in Song.objects.all():
            entries = LogEntry.objects.filter(content_type=song_type, action_flag=ADDITION,
                                              object_id=song.pk).order_by("-action_time")
            assert len(entries) == 1
            entry = entries[0]
            song.author = entry.user
            song.date = entry.action_time
            song.save()
            print("%s by %s on %s" % (song, entry.user, entry.action_time))
