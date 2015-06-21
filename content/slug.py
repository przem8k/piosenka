from django.db import models
from django.utils.text import slugify

from unidecode import unidecode


class SlugMixin(models.Model):
    """ A class that extends this has to have:
     - a slug field
     - get_slug_elements"""
    # TODO: define the slug field here.
    # TODO: add tests
    MAX_SLUG_LENGTH = 200

    class Meta:
        abstract = True

    def get_slug_elements(self):
        raise NotImplementedError

    @staticmethod
    def make_slug(slug_elements):
        normalized_string = unidecode(" ".join(slug_elements))
        return slugify(normalized_string)[:SlugMixin.MAX_SLUG_LENGTH]

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_elements = self.get_slug_elements()
            candidate = SlugMixin.make_slug(slug_elements)
            counter = 0
            while self.__class__.objects.filter(slug=candidate):
                counter += 1
                candidate = SlugMixin.make_slug(slug_elements + [str(counter)])
            self.slug = candidate
        return super().save(*args, **kwargs)
