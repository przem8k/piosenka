import datetime

from django.db import models
from django.utils.text import slugify

from unidecode import unidecode

from frontpage.models import ContentItem
from frontpage.trevor import render_trevor


class PublishedPostManager(models.Manager):
    def get_queryset(self):
        return super(PublishedPostManager, self).get_queryset().filter(published=True)


class Post(ContentItem):
    objects = models.Manager()
    po = PublishedPostManager()

    title = models.CharField(max_length=100,
                             help_text="Tytuł posta, np. 'Nowa wyszukiwarka piosenek.'.")
    post_trevor = models.TextField()
    more_trevor = models.TextField(null=True, blank=True)

    slug = models.SlugField(max_length=100, unique=True, editable=False)
    pub_date = models.DateTimeField(editable=False)
    post_html = models.TextField(null=True, editable=False)
    more_html = models.TextField(null=True, editable=False)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            assert self.title
            max_len = Post._meta.get_field('slug').max_length
            self.slug = slugify(unidecode(self.title))[:max_len]
        if not self.pub_date:
            self.pub_date = datetime.datetime.now()
        self.post_html = render_trevor(self.post_trevor)
        if self.more_trevor:
            self.more_html = render_trevor(self.more_trevor)
        else:
            self.more_html = ""
        super(Post, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('post_detail', (), {
            'year': self.pub_date.strftime("%Y"),
            'month': self.pub_date.strftime("%m"),
            'day': self.pub_date.strftime("%d"),
            'slug': self.slug
        })

    @models.permalink
    def get_edit_url(self):
        return ('edit_post', (), {
            'year': self.pub_date.strftime("%Y"),
            'month': self.pub_date.strftime("%m"),
            'day': self.pub_date.strftime("%d"),
            'slug': self.slug
        })
