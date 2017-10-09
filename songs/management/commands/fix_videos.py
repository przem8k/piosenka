"""
Command that validates all yt videos referenced by songs and removes the
obsoletes.
"""

from django.core.management.base import BaseCommand
from django.conf import settings

from apiclient.discovery import build

from songs.models import Song, EntityContribution

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


"""Fixes outdated or missing YT links.

This uses the YT data API: https://developers.google.com/youtube/v3/docs/.
"""
class Command(BaseCommand):
    help = 'Check and fix all video links.'

    def handle(self, *args, **options):
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                            developerKey=settings.GOOGLE_API_KEY)

        count_all = 0
        count_none = 0
        count_incorrect = 0
        for song in Song.objects.all():
            print(str(song))
            count_all += 1
            if not song.youtube_id():
                print(' - no link')
                count_none += 1
            else:
                id = song.youtube_id()
                response = youtube.videos().list(
                    part='id,snippet',
                    id=id
                ).execute()
                if not response['items']:
                    print(' - incorrect link, deleting')
                    count_incorrect += 1
                    song.link_youtube = None
                    song.save()

            if song.youtube_id():
                print(' - OK')
                continue

            # The link is missing - try to find a new one.
            head_contribution = EntityContribution.head_contribution(EntityContribution.objects.filter(song=song.id))
            query = song.title + ' ' + str(head_contribution.artist)
            print(' - would look for: ' + query)
            candidates = youtube.search().list(maxResults=1, part='id,snippet',
                                               q=query).execute()
            if not candidates['items']:
                print(' - no results :(')
            else:
                candidate = candidates['items'][0]
                title = candidate['snippet']['title']
                channelTitle = candidate['snippet']['channelTitle']
                print(' - top: ' + title + ' (' + channelTitle + ')')
                print('   does it look good? (y/n)')
                answer = input()
                if answer == 'y' or answer == 'yes':
                    song.set_youtube_id(candidate['id']['videoId'])
                    song.save()
                    print(' - set!')

        print('all songs: ' + str(count_all))
        print('no link: ' + str(count_none))
        print('invalid link (fixed): ' + str(count_incorrect))
