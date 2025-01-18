"""Marks all items of all content types as reviewed."""

from articles.models import Article
from django.core.management.base import BaseCommand

from blog.models import Post
from songs.models import Artist, ArtistNote, Song, SongNote


class Command(BaseCommand):
    help = "Marks all items of all content types as reviewed."

    def handle(self, *args, **options):
        for artist in Artist.objects.all():
            artist.reviewed = True
            artist.save()
            print("Reviewed: %s" % (artist))

        for note in ArtistNote.objects.all():
            note.reviewed = True
            note.save()
            print("Reviewed: %s" % (note))

        for article in Article.objects.all():
            article.reviewed = True
            article.save()
            print("Reviewed: %s" % (article))

        for post in Post.objects.all():
            post.reviewed = True
            post.save()
            print("Reviewed: %s" % (post))

        for song in Song.objects.all():
            song.reviewed = True
            song.save()
            print("Reviewed: %s" % (song))

        for note in SongNote.objects.all():
            note.reviewed = True
            note.save()
            print("Reviewed: %s" % (note))
