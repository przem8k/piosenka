from django.core.management.base import BaseCommand

from songs.models import Artist, ArtistNote


class Command(BaseCommand):
    help = 'Creates artist notes based on artist field data.'

    def handle(self, *args, **options):
        for artist in Artist.objects.all():
            if ArtistNote.objects.filter(artist=artist):
                print('No need to create note for: ' + str(artist))
                continue

            if not artist.description_trevor:
                print('No interesting info about: ' + str(artist))
                continue

            note = ArtistNote()
            note.artist = artist
            note.title = artist.name
            note.image = artist.image
            note.image_url = artist.image_url
            note.image_author = artist.image_author
            note.text_trevor = artist.description_trevor
            # content meta
            note.author = artist.author
            note.reviewed = artist.reviewed
            note.pub_date = artist.pub_date
            note.save()
            print('Created note: %s' % (note.title))
