from django.db import models
from django.utils.text import slugify

from unidecode import unidecode


class SlugLogicMixin(object):
    """Bring your-own slug field slug mixin.

    This assumes that a slug field is already defined on the object."""

    def get_slug_elements(self):
        raise NotImplementedError

    def make_slug(self, slug_elements):
        normalized_string = unidecode(' '.join(slug_elements))
        max_length = self._meta.get_field('slug').max_length
        return slugify(normalized_string)[:max_length]

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_elements = self.get_slug_elements()
            candidate = self.make_slug(slug_elements)
            counter = 0
            while self.__class__.objects.filter(slug=candidate):
                counter += 1
                candidate = self.make_slug(slug_elements + [str(counter)])
            self.slug = candidate
        return super().save(*args, **kwargs)


class SlugFieldMixin(SlugLogicMixin, models.Model):
    slug = models.SlugField(max_length=100, unique=True, editable=False)

    class Meta:
        abstract = True
