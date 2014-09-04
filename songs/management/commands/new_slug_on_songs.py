"""
Sets new_slug simply by calling save on each song.
"""

from django.core.management.base import BaseCommand

from songs.models import Song


class Command(BaseCommand):
    help = "Sets new_slug on songs."

    def handle(self, *args, **options):
        for song in Song.objects.all():
            song.save()
            print("Slugs: %s %s" % (song.slug, song.new_slug))
