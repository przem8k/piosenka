import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

from easy_thumbnails.signal_handlers import generate_aliases
from easy_thumbnails.signals import saved_file
from unidecode import unidecode

from frontpage.trevor import render_trevor

saved_file.connect(generate_aliases)


class PublishedArticleManager(models.Manager):
    def get_queryset(self):
        return super(PublishedArticleManager, self).get_queryset().filter(published=True)


class Article(models.Model):
    objects = models.Manager()
    po = PublishedArticleManager()

    title = models.CharField(max_length=100,
                             help_text="Tytuł artykułu, np. 'IX Festiwal Piosenki Poetyckiej im. "
                                       "Jacka Kaczmarskiego \"Nadzieja\"'.")
    lead_text_trevor = models.TextField()
    main_text_trevor = models.TextField()
    cover_image = models.ImageField(null=True, blank=True, upload_to='article_covers',
                                    help_text="Main illustration for the article.")
    cover_credits_trevor = models.TextField(null=True, blank=True)

    slug = models.SlugField(max_length=100, editable=False)
    author = models.ForeignKey(User, editable=False)
    date = models.DateTimeField(editable=False)
    published = models.BooleanField(default=True, editable=False)
    lead_text_html = models.TextField(editable=False)
    main_text_html = models.TextField(editable=False)
    cover_credits_html = models.TextField(null=True, blank=True, editable=False)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            assert self.title
            max_len = Article._meta.get_field('slug').max_length
            self.slug = slugify(unidecode(self.title))[:max_len]
        if not self.date:
            self.date = datetime.datetime.now()
        self.lead_text_html = render_trevor(self.lead_text_trevor)
        self.main_text_html = render_trevor(self.main_text_trevor)
        if self.cover_credits_trevor:
            self.cover_credits_html = render_trevor(self.cover_credits_trevor)
        super(Article, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return('article', (), {
            'slug': self.slug,
        })

    @models.permalink
    def get_edit_url(self):
        return('edit_article', (), {
            'slug': self.slug,
        })
