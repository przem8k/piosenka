import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

from markdown import markdown
from unidecode import unidecode


class PublishedPostManager(models.Manager):
    def get_queryset(self):
        return super(PublishedPostManager, self).get_queryset().filter(published=True)


class Post(models.Model):
    objects = models.Manager()
    po = PublishedPostManager()

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, null=True)
    author = models.ForeignKey(User, editable=False)
    date = models.DateTimeField(editable=False)
    post = models.TextField(help_text="Post or its introductory part, written in Markdown.")
    post_html = models.TextField(null=True, blank=True, editable=False)
    more = models.TextField(blank=True, null=True,
                            help_text="Optional rest of the post, written in Markdown.")
    more_html = models.TextField(null=True, blank=True, editable=False)
    published = models.BooleanField(default=True, help_text="Only admins see not-published posts")

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            assert self.title
            max_len = Post._meta.get_field('slug').max_length
            self.slug = slugify(unidecode(self.title))[:max_len]
        if not self.date:
            self.date = datetime.datetime.now()
        self.post_html = markdown(self.post, safe_mode='escape')
        self.more_html = markdown(self.more, safe_mode='escape')
        super(Post, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('post_detail', (), {
            'year': self.date.strftime("%Y"),
            'month': self.date.strftime("%m"),
            'day': self.date.strftime("%d"),
            'slug': self.slug
        })
