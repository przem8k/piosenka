"""
Converts the description field in Markdown to description_trevor.
"""

from django.core.management.base import BaseCommand

from artists.models import Artist, Band, Entity
from songs.models import ArtistContribution, BandContribution, EntityContribution
from events.models import Event, EntityPerformance


class Command(BaseCommand):
    help = "Unify Artists and Bands into Entities."

    def handle(self, *args, **options):
        print("Creating entities for Artists.")
        for artist in Artist.objects.all():
            if not artist.entity:
                entity = Entity()
                entity.name = artist.lastname
                entity.first_name = artist.firstname
                entity.slug = artist.slug
                entity.featured = artist.display
                entity.kind = artist.kind
                entity.website = artist.website
                entity.is_band = False
                entity.save()

                artist.entity = entity
                artist.save()
                print("Created entity: " + str(entity))
            else:
                print(str(artist) + " already has an Entity.")

        print("Creating entities for Bands.")
        for band in Band.objects.all():
            if not band.entity:
                entity = Entity()
                entity.name = band.name
                entity.slug = band.slug
                entity.featured = band.display
                entity.website = band.website
                entity.is_band = True
                entity.kind = Entity.TYPE_BAND
                entity.save()

                band.entity = entity
                band.save()
                print("Created entity: " + str(entity))
            else:
                print(str(band) + " already has an Entity.")

        print("Converting ArtistContributions.")
        for artist_contribution in ArtistContribution.objects.all():
            if not artist_contribution.entity_contribution:
                entity_contribution = EntityContribution()
                entity_contribution.song = artist_contribution.song
                entity_contribution.entity = artist_contribution.artist.entity
                entity_contribution.performed = artist_contribution.performed
                entity_contribution.texted = artist_contribution.texted
                entity_contribution.translated = artist_contribution.translated
                entity_contribution.composed = artist_contribution.composed
                entity_contribution.save()

                artist_contribution.entity_contribution = entity_contribution
                artist_contribution.save()
                print("Created entity cont.: " + str(entity_contribution))
            else:
                print(str(artist_contribution) + " already has an Entity.")

        print("Converting BandContributions.")
        for band_contribution in BandContribution.objects.all():
            if not band_contribution.entity_contribution:
                entity_contribution = EntityContribution()
                entity_contribution.song = band_contribution.song
                entity_contribution.entity = band_contribution.band.entity
                entity_contribution.performed = band_contribution.performed
                entity_contribution.texted = False
                entity_contribution.translated = False
                entity_contribution.composed = False
                entity_contribution.save()

                band_contribution.entity_contribution = entity_contribution
                band_contribution.save()
                print("Created entity cont.: " + str(entity_contribution))
            else:
                print(str(band_contribution) + " already has an Entity.")

        print("Converting artist performances.")
        for event in Event.objects.all():
            for artist in event.artists.all():
                entity_performance = EntityPerformance()
                entity_performance.event = event
                entity_performance.entity = artist.entity
                entity_performance.save()

                artist.entity.still_plays = True
                artist.entity.save()
                print("Added entity " + str(entity_performance.entity) + " on event " + str(event))

            for band in event.bands.all():
                entity_performance = EntityPerformance()
                entity_performance.event = event
                entity_performance.entity = band.entity
                entity_performance.save()

                band.entity.still_plays = True
                band.entity.save()
                print("Added entity " + str(entity_performance.entity) + " on event " + str(event))
