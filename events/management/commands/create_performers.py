from django.core.management.base import BaseCommand

from events.models import Performer, EntityPerformance


class Command(BaseCommand):
    help = 'Creates event performers based on existing entities.'

    def handle(self, *args, **options):
        for performance in EntityPerformance.objects.all():
            entity = performance.entity
            if Performer.objects.filter(entity=entity):
                print('No need to create performer for: ' + str(entity))
                performer = Performer.objects.get(entity=entity)
            else:
                performer = Performer()
                performer.name = str(entity)
                performer.slug = entity.slug
                performer.website = entity.website
                performer.entity = entity
                performer.save()
                print('Created performer: %s, slug: %s' % (performer.name,
                                                           performer.slug))

            if performance.performer:
                assert performance.performer == performer
                print('No need to set performer on: ' + str(performance))
            else:
                performance.performer = performer
                performance.save()
                print('Set performer on %s' % str(performance))
