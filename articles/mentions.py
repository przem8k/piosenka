import re

from songs.models import Song


def find_songs_mentioned_in_article(article):
    """Returns the set of songs mentioned in the given article."""
    regex = re.compile(r"opracowanie/([^/\"\']+)")
    matches = regex.findall(article.main_text_html)

    songs = set()
    for slug in matches:
        song = Song.objects.filter(slug=slug).first()
        if not song:
            continue
        songs.add(song)
    return songs
