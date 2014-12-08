from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

from unidecode import unidecode


class ContentItem(models.Model):
    MAX_SLUG_LENGTH = 200

    author = models.ForeignKey(User, editable=False)
    published = models.BooleanField(default=True, editable=False)
    pub_date = models.DateTimeField(editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_elements = kwargs.pop('prepend_slug_elements', []) + self.get_slug_elements()
            self.slug = ContentItem.make_slug(slug_elements)

        return super(ContentItem, self).save(*args, **kwargs)

    @staticmethod
    def make_slug(slug_elements):
        return slugify(unidecode(" ".join(slug_elements)))[:ContentItem.MAX_SLUG_LENGTH]
