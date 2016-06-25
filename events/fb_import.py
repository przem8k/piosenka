from django.utils.dateparse import parse_datetime
from django.utils import timezone

from events.models import FbEvent, Performer


def _get_event_from_data(event_data):
    fb_id = event_data['id']
    start_time = parse_datetime(event_data['start_time'])
    name = event_data['name']
    fb_event = FbEvent(fb_id=fb_id, name=name, datetime=start_time)

    if 'place' in event_data and 'location' in event_data['place']:
        location_data = event_data['place']['location']
        if ('latitude' in location_data and 'longitude' in location_data):
            fb_event.lat = location_data['latitude']
            fb_event.lon = location_data['longitude']
            if 'city' in location_data:
                fb_event.town = location_data['city']

    return fb_event


def update_events(graph):
    for fb_event in FbEvent.objects.all():
        fresh_fb_event = _get_event_from_data(graph.request(str(
            fb_event.fb_id)))
        fb_event.name = fresh_fb_event.name
        fb_event.datetime = fresh_fb_event.datetime
        fb_event.town = fresh_fb_event.town
        fb_event.lat = fresh_fb_event.lat
        fb_event.lon = fresh_fb_event.lon

        if fb_event.datetime > timezone.now():
            fb_event.save()
            print(' refreshed ' + fb_event.name)
        else:
            fb_event.delete()
            print(' deleted ' + fb_event.name)


def import_events(graph):
    for performer in Performer.objects.all():
        if not performer.fb_page_id:
            continue

        response = graph.request(performer.fb_page_id + '/events')
        events = response['data']

        print(' got %d events for %s' % (len(events), performer))

        for event_data in events:
            fb_id = event_data['id']
            start_time = parse_datetime(event_data['start_time'])

            # Don't add new event if it's already passed.
            exists = FbEvent.objects.filter(fb_id=fb_id).exists()
            if exists or start_time < timezone.now():
                continue
            fb_event = _get_event_from_data(event_data)
            fb_event.save()
            print(' added %s from %s' % (fb_event.name, performer))
