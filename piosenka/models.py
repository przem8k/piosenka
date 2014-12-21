import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

from unidecode import unidecode


class ContentItem(models.Model):
    MAX_SLUG_LENGTH = 200

    author = models.ForeignKey(User, editable=False)
    reviewed = models.BooleanField(default=False, editable=False)
    # published is deprecated - need to use reviewed instead.
    published = models.BooleanField(default=True, editable=False)
    pub_date = models.DateTimeField(editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pub_date:
            self.pub_date = datetime.datetime.now()
        if not self.slug:
            slug_elements = kwargs.pop('prepend_slug_elements', []) + self.get_slug_elements()
            self.slug = ContentItem.make_slug(slug_elements)

        return super(ContentItem, self).save(*args, **kwargs)

    @staticmethod
    def make_slug(slug_elements):
        return slugify(unidecode(" ".join(slug_elements)))[:ContentItem.MAX_SLUG_LENGTH]

    def is_live(self):
        return self.reviewed

    def status_str(self):
        return "opublikowany" if self.reviewed else "w moderacji"

    def status_long_str(self):
        return "Widoczny publicznie." if self.reviewed else "Czeka na akceptację moderatora."
