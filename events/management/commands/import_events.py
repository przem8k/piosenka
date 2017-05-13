import sys

from django.core.management.base import BaseCommand
from django.conf import settings

import facebook

from events.fb_import import update_events, import_events


class Command(BaseCommand):
    help = 'Imports events from FB'

    def handle(self, *args, **options):
        # Workaround running from cron encoding problems.
        sys.stdout = open(1, 'w', encoding='utf-8', closefd=False)

        token = facebook.GraphAPI().get_app_access_token(
            settings.FB_APP_ID, settings.FB_APP_SECRET)
        print('[get access token]')
        graph = facebook.GraphAPI(access_token=token)

        print('[update events]')
        update_events(graph)

        print('[import events from pages]')
        import_events(graph)
