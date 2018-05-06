"""
Command that always fails.

This can be used in a cron job to verify that the error reporting works.
"""

import sys

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Returns a non-zero exit status.'

    def handle(self, *args, **options):
        sys.exit(-1)
