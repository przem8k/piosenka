import uuid

from django.core.exceptions import ValidationError
from django.db import models

from content.slug import SlugFieldMixin


class Entity(SlugFieldMixin, models.Model):
    name = models.CharField(max_length=50,
                            help_text="Name for a band, lastname for a person.")
    first_name = models.CharField(max_length=50, null=True, blank=True,
                                  help_text="First (and possibly second) name if this is a person.")
    featured = models.BooleanField(default=False,
                                   help_text="Iff true, it will be included in the songbook menu.")
    still_plays = models.BooleanField(default=False,
                                      help_text="Iff true, the entity can be added on events.")
    website = models.URLField(null=True, blank=True)

    TYPE_TEXTER = 1
    TYPE_COMPOSER = 2
    TYPE_TRANSLATOR = 3
    TYPE_PERFORMER = 4
    TYPE_POET = 5
    TYPE_FOREIGN = 6
    TYPE_BAND = 7
    ENTITY_TYPES = (
        (TYPE_TEXTER, u'Wykonawca własnych tekstów'),
        (TYPE_COMPOSER, u'Kompozytor'),
        (TYPE_TRANSLATOR, u'Tłumacz'),
        (TYPE_PERFORMER, u'Wykonawca cudzych piosenek'),
        (TYPE_POET, u'Poeta nieśpiewający'),
        (TYPE_FOREIGN, u'Bard zagraniczny'),
        (TYPE_BAND, u'Zespół'),
    )
    kind = models.IntegerField(choices=ENTITY_TYPES, null=True, blank=True,
                               help_text="Select the best fit.")
    is_band = models.BooleanField(default=False, editable=False,
                                  help_text="Filled automaticely from type to facilitate sorting.")

    @staticmethod
    def create_for_testing():
        entity = Entity()
        entity.name = str(uuid.uuid4()).replace("-", "")
        entity.slug = entity.name
        entity.save()
        return entity

    class Meta:
        ordering = ["is_band", "name", "first_name"]

    def __str__(self):
        return self.name if not self.first_name else self.first_name + " " + self.name

    def save(self, *args, **kwargs):
        self.is_band = self.kind == Entity.TYPE_BAND
        super().save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('songbook_entity', (), {'slug': self.slug})

    @models.permalink
    def get_gigs_url(self):
        return ('view_performer', (), {'slug': self.slug})

    def clean(self):
        super().clean()
        if self.kind == Entity.TYPE_BAND and self.first_name:
            raise ValidationError("Bands don't have first names.")

    # SlugFieldMixin:
    def get_slug_elements(self):
        if self.first_name:
            return [self.first_name, self.name]
        else:
            return [self.name]
