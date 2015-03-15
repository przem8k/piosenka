from django.db import models
from django.utils.text import slugify

from unidecode import unidecode


class SlugMixin(models.Model):
    """ A class that extends this has to have:
     - a slug field
     - get_slug_elements"""
    # TODO: define the slug field here.
    # TODO: add explicit - clean() ? - validation for unique contraint.
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
            slug_elements = (kwargs.pop('prepend_slug_elements', []) +
                             self.get_slug_elements())
            self.slug = SlugMixin.make_slug(slug_elements)
        return super().save(*args, **kwargs)
