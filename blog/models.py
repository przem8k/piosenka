from django.db import models

from frontpage.trevor import render_trevor
from piosenka.models import ContentItem


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
    post_html = models.TextField(null=True, editable=False)
    more_html = models.TextField(null=True, editable=False)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.title

    # ContentItem override.
    def get_slug_elements(self):
        assert self.title
        return [self.title]

    def save(self, *args, **kwargs):
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
