"""Processes templates of the documentation pages."""

import os
import re
from os import path

from django.core.management.base import BaseCommand
from django.conf import settings
from django.template import Context, loader

from songs.lyrics import render_lyrics

_REWRITE_LYRICS_BEGIN_TAG = r"<!-- rewrite-song-lyrics-begin -->"
_REWRITE_LYRICS_END_TAG = r"<!-- rewrite-song-lyrics-end -->"


def _rewrite_lyrics(match):
    template_name = 'songs/lyrics_example.html'
    input_lyrics = '\n'.join(line.strip()
                             for line in str(match.group(1)).split('\n'))
    output_lyrics = render_lyrics(input_lyrics)
    return loader.get_template(template_name).render(
        Context({
            'input_lyrics': input_lyrics,
            'output_lyrics': output_lyrics
        }))


class Command(BaseCommand):
    help = 'Processes templates of the documentation pages.' ''

    def handle(self, *args, **options):
        for dirpath, dirnames, filenames in os.walk(settings.PROJECT_PATH):
            for filename in [f for f in filenames if f.endswith('.htmltmpl')]:
                source_path = path.realpath(path.join(dirpath, filename))
                dest_path = source_path.rsplit('.', 1)[0] + '.generated'

                with open(source_path, 'r') as source_file:
                    template = source_file.read()

                result = re.sub(_REWRITE_LYRICS_BEGIN_TAG + r"((?s).*?)" +
                                _REWRITE_LYRICS_END_TAG, _rewrite_lyrics,
                                template)

                with open(dest_path, 'w') as dest_file:
                    dest_file.write(result)
                print('Rewritten %s -> %s.' % (source_path, dest_path))
