from markdown import markdown

from django.db import models
from django.contrib.auth.models import User


class ArticleCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "ArticleCategories"

    def __unicode__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    category = models.ForeignKey(ArticleCategory, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True, help_text="Publication date.") # TODO: automate
    lead_text = models.TextField(help_text="Introductory paragraph, written in Markdown")
    lead_text_html = models.TextField(null=True, blank=True, editable=False)
    main_text = models.TextField(help_text="Rest of the article, written in Markdown")
    main_text_html = models.TextField(null=True, blank=True, editable=False)
    published = models.BooleanField(default=True)
    author = models.ForeignKey(User, null=True, blank=True)
    cover = models.ImageField(null=True, blank=True, upload_to='articles', help_text="Main illustration for the article.")

    @models.permalink
    def get_absolute_url(self):
        return('article', (), {
            'slug': self.slug,
        })

    def save(self, *args, **kwargs):
        self.lead_text_html = markdown(self.lead_text, safe_mode='escape')
        self.main_text_html = markdown(self.main_text, safe_mode='escape')

        super(Article, self).save(*args, **kwargs)

    class Meta:
        ordering = ["title"]

    def __unicode__(self):
        return self.title
