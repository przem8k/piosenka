"""
Command that validates all songs in the database reporting any errors. This is useful after
parser or transposer changes.
"""

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Check all songs in the database.'

    def handle(self, *args, **options):
        from songs.models import Song, validate_lyrics
        count_all = 0
        count_incorrect = 0
        for song in Song.objects.all():
            if song.lyrics:
                try:
                    validate_lyrics(song.lyrics)
                except ValidationError as m:
                    print 'Song %d %s incorrect: %s' % (song.id,
                                                        song.title,
                                                        m,)
                    count_incorrect = count_incorrect + 1
                count_all = count_all + 1

        if count_incorrect == 0:
            print 'All good!'
        else:
            print 'Incorrect %d out of %d songs.' % (count_incorrect,
                                                     count_all,)
