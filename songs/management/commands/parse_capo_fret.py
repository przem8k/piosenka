"""
 Command for parsing the capo_fret from key
"""

import os, time
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Parse capo fret of the songs from key"
    ROMAN_TO_DECIMAL = {
        "I" : 1,
        "II" : 2,
        "III" : 3,
        "IV" : 4,
        "V" : 5,
        "VI" : 6
    }
    def handle(self, *args, **options):
        from songs.models import Song
        for song in Song.objects.all():
            if song.key:
                begin = song.key.find("kap.")
                end = song.key.find(")")
                if begin != -1 and end != -1 and begin < end:
                    raw = song.key[begin+4:end].strip()
                    if raw in Command.ROMAN_TO_DECIMAL:
                        converted = Command.ROMAN_TO_DECIMAL[raw]
                        song.capo_fret = converted;
                        song.save()
                        print "%s : %s -> %d" % (song.title, raw, converted)
            