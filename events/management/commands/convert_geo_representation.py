"""
Command for moving from Location text field to a pair of FloatFields for geo coordinates.
"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Null"

    def handle(self, *args, **options):
        from events.models import Venue
        for venue in Venue.objects.all():
            venue.lat = venue.location_lat()
            venue.lon = venue.location_lng()
            venue.save()
            print("Processed venue: %s, setting the coords to: %f %f." % (venue.name, venue.lat,
                                                                          venue.lon))
