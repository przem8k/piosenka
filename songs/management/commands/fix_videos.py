"""
Command that validates all yt videos referenced by songs and removes the
obsoletes.
"""

from django.core.management.base import BaseCommand
from django.conf import settings

from apiclient.discovery import build

from songs.models import Song

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"



class Command(BaseCommand):
    help = 'Check and fix all video links.'

    def handle(self, *args, **options):
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                            developerKey=settings.GOOGLE_API_KEY)

        count_all = 0
        count_none = 0
        count_incorrect = 0
        for song in Song.objects.all():
            count_all += 1
            if not song.youtube_id():
                print('No video link: ' + str(song))
                count_none += 1
                continue
            id = song.youtube_id()
            response = youtube.videos().list(
                part='id,snippet',
                id=id
            ).execute()
            if not response['items']:
                print('Invalid video link: ' + str(song))
                count_incorrect += 1
                song.link_youtube = None
                song.save()

        print('all songs: ' + str(count_all))
        print('no link: ' + str(count_none))
        print('invalid link (fixed): ' + str(count_incorrect))
