from django.core.management.base import BaseCommand

from songs import models


class Command(BaseCommand):
    help = 'Converts existing Annotations into SongNotes.'

    def handle(self, *args, **options):
        for annotation in models.Annotation.objects.all():
            note = models.SongNote()
            note.song = annotation.song
            note.slug = annotation.slug
            note.title = annotation.title
            note.image = annotation.image
            note.url1 = annotation.source_url1
            note.url2 = annotation.source_url2
            note.ref1 = annotation.source_ref1
            note.ref2 = annotation.source_ref2
            note.text_trevor = annotation.text_trevor
            # content meta
            note.author = annotation.author
            note.reviewed = annotation.reviewed
            note.pub_date = annotation.pub_date
            note.save()
            print('Created note: %s' % (note.title))
