from datetime import datetime

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.dateparse import parse_datetime
from django.utils import timezone

import facebook

from events.models import FbEvent, Performer


class Command(BaseCommand):
    help = 'Imports events from FB'

    def handle(self, *args, **options):
        token = facebook.GraphAPI().get_app_access_token(settings.FB_APP_ID,
                                                         settings.FB_APP_SECRET)
        graph = facebook.GraphAPI(access_token=token)
        print('Got access token.')

        for performer in Performer.objects.all():
            if not performer.fb_page_id:
                continue

            response = graph.request(performer.fb_page_id + '/events')
            events = response['data']

            print('Got %d events for %s' % (len(events), performer))

            for event_data in events:
                fb_id = event_data['id']
                start_time = parse_datetime(event_data['start_time'])

                # Don't add new event if it's already passed.
                exists = FbEvent.objects.filter(fb_id=fb_id).exists()
                if not exists and start_time < timezone.now():
                    continue

                name = event_data['name']
                if not exists:
                    fb_event = FbEvent(fb_id=fb_id, name=name,
                                       datetime=start_time)
                else:
                    fb_event = FbEvent.objects.get(fb_id=fb_id)
                    fb_event.name = name
                    fb_event.datetime = start_time

                if 'place' in event_data and 'location' in event_data['place']:
                    location_data = event_data['place']['location']
                    if ('latitude' in location_data and
                        'longitude' in location_data):
                        fb_event.lat = location_data['latitude']
                        fb_event.lon = location_data['longitude']
                    if 'city' in location_data:
                        fb_event.town = location_data['city']

                fb_event.save()
                print("created or updated %s at %s" % (fb_event.name,
                                                       str(start_time)))
