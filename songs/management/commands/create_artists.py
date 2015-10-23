from django.core.management.base import BaseCommand

from songs.models import Artist, EntityContribution
from artists.models import Entity


class Command(BaseCommand):
    help = 'Creates artists based on existing contributions.'

    def handle(self, *args, **options):
        for entity in Entity.objects.all():
            if Artist.objects.filter(entity=entity):
                print('No need to create artist for: ' + str(entity))
                continue

            artist = Artist()
            artist.name = str(entity)
            artist.slug = entity.slug
            artist.website = entity.website
            artist.entity = entity

            if entity.kind == entity.KIND_TEXTER:
                artist.category = artist.CAT_TEXTER
            elif entity.kind == entity.KIND_COMPOSER:
                artist.category = artist.CAT_COMPOSER
            elif entity.kind == entity.KIND_FOREIGN:
                artist.category = artist.CAT_FOREIGN
            elif entity.kind == entity.KIND_BAND:
                artist.category = artist.CAT_BAND

            artist.save()
            print('Created artist: %s, slug: %s' % (artist.name,
                                                    artist.slug))

        for contribution in EntityContribution.objects.all():
            if contribution.artist:
                print('No need to set artist on contribution.')
                continue

            contribution.artist = Artist.objects.get(entity=contribution.entity)
            contribution.save()
            print('%s set on %s' % (str(contribution.artist),
                                    str(contribution)))
