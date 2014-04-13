"""
Sets the has_extra_chords value on existing songs.
"""

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Runs full_clean on all songs to properly set has_extra_chords."

    def handle(self, *args, **options):
        from songs.models import Song
        for song in Song.objects.all():
            if song.lyrics:
                before = song.has_extra_chords
                song.full_clean()
                song.save()
                after = song.has_extra_chords
                print("%s: %s -> %s" % (song, before, after,))
