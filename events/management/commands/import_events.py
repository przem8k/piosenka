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
                name = event_data['name']

                datetime = parse_datetime(event_data['start_time'])
                if datetime < timezone.now():
                    continue

                fb_id = event_data['id']
                if FbEvent.objects.filter(fb_id=fb_id).exists():
                    print('Skipping %s - exists' % (name))
                    continue

                extra_args = dict()
                if 'place' in event_data and 'location' in event_data['place']:
                    location_data = event_data['place']['location']
                    if ('latitude' in location_data and
                        'longitude' in location_data):
                        extra_args['lat'] = location_data['latitude']
                        extra_args['lon'] = location_data['longitude']
                    if 'city' in location_data:
                        extra_args['town'] = location_data['city']

                fb_event = FbEvent(fb_id=fb_id, name=name, datetime=datetime,
                                   **extra_args)
                fb_event.save()

                print("created %s at %s" % (name, str(datetime)))
