from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases
from markdown import markdown
from unidecode import unidecode

saved_file.connect(generate_aliases)


class CarouselItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(help_text="Description, written in Markdown.")
    description_html = models.TextField(null=True, blank=True, editable=False)
    position = models.IntegerField()
    image = models.ImageField(upload_to='carousel_items',
                              help_text="Picture to display in carousel.")
    archived = models.BooleanField(default=False)

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.description_html = markdown(self.description, safe_mode='escape')
        super(CarouselItem, self).save(*args, **kwargs)


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
