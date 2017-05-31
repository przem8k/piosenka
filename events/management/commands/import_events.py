import sys

from django.core.management.base import BaseCommand

from events.fb_import import update_events, import_events


class Command(BaseCommand):
    help = 'Imports events from FB'

    def handle(self, *args, **options):
        # Workaround running from cron encoding problems.
        sys.stdout = open(1, 'w', encoding='utf-8', closefd=False)

        print('[update events]')
        update_events()

        print('[import events from pages]')
        import_events()
