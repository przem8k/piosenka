from django.core.management.base import BaseCommand

from songs.models import Artist


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        for artist in Artist.objects.all():
            if not artist.entity:
                print('No entity on ' + str(artist) + ', continue')
                continue

            if artist.entity.featured:
                artist.featured = True
                print('FEATURED ' + str(artist))
                artist.save()
