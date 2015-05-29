"""Marks all items of all content types as reviewed."""

from django.core.management.base import BaseCommand

from articles.models import Article
from blog.models import Post
from events.models import Event
from songs.models import Annotation, Song


class Command(BaseCommand):
    help = "Marks all items of all content types as reviewed."

    def handle(self, *args, **options):
        for article in Article.objects.all():
            article.reviewed = True
            article.save()
            print("Reviewed: %s" % (article))

        for post in Post.objects.all():
            post.reviewed = True
            post.save()
            print("Reviewed: %s" % (post))

        for event in Event.objects.all():
            event.reviewed = True
            event.save()
            print("Reviewed: %s" % (event))

        for song in Song.objects.all():
            song.reviewed = True
            song.save()
            print("Reviewed: %s" % (song))

        for annotation in Annotation.objects.all():
            annotation.reviewed = True
            annotation.save()
            print("Reviewed: %s" % (annotation))
