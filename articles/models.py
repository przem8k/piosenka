import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

from easy_thumbnails.signal_handlers import generate_aliases
from easy_thumbnails.signals import saved_file
from markdown import markdown
from unidecode import unidecode

saved_file.connect(generate_aliases)


class ArticleCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "ArticleCategories"

    def __str__(self):
        return self.name


class PublishedArticleManager(models.Manager):
    def get_queryset(self):
        return super(PublishedArticleManager, self).get_queryset().filter(published=True)


class Article(models.Model):
    objects = models.Manager()
    po = PublishedArticleManager()

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    category = models.ForeignKey(ArticleCategory, null=True, blank=True)
    date = models.DateTimeField(editable=False, help_text="Publication date.")
    lead_text = models.TextField(help_text="Introductory paragraph, written in Markdown.")
    lead_text_html = models.TextField(null=True, blank=True, editable=False)
    main_text = models.TextField(help_text="Rest of the article, written in Markdown.")
    main_text_html = models.TextField(null=True, blank=True, editable=False)
    published = models.BooleanField(default=True)
    author = models.ForeignKey(User, editable=False)
    cover_image = models.ImageField(null=True, blank=True, upload_to='article_covers',
                                    help_text="Main illustration for the article.")
    cover_credits = models.TextField(null=True, blank=True,
                                     help_text="Thank you / credit notes about the author of "
                                               "the cover picture, written in Markdown.")
    cover_credits_html = models.TextField(null=True, blank=True, editable=False)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.lead_text_html = markdown(self.lead_text, safe_mode='escape')
        self.main_text_html = markdown(self.main_text)
        self.cover_credits_html = markdown(self.cover_credits, safe_mode='escape')
        if not self.slug:
            assert self.title
            max_len = Article._meta.get_field('slug').max_length
            self.slug = slugify(unidecode(self.title))[:max_len]
        if not self.date:
            self.date = datetime.datetime.now()
        super(Article, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return('article', (), {
            'slug': self.slug,
        })
