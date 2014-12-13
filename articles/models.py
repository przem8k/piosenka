from django.db import models

from easy_thumbnails.signal_handlers import generate_aliases
from easy_thumbnails.signals import saved_file

from piosenka.trevor import render_trevor
from piosenka.models import ContentItem

saved_file.connect(generate_aliases)


class PublishedArticleManager(models.Manager):
    def get_queryset(self):
        return super(PublishedArticleManager, self).get_queryset().filter(published=True)


class Article(ContentItem):
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

    slug = models.SlugField(max_length=100, unique=True, editable=False)
    lead_text_html = models.TextField(editable=False)
    main_text_html = models.TextField(editable=False)
    cover_credits_html = models.TextField(null=True, blank=True, editable=False)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.title

    # ContentItem override.
    def get_slug_elements(self):
        assert self.title
        return [self.title]

    def save(self, *args, **kwargs):
        self.lead_text_html = render_trevor(self.lead_text_trevor)
        self.main_text_html = render_trevor(self.main_text_trevor)
        if self.cover_credits_trevor:
            self.cover_credits_html = render_trevor(self.cover_credits_trevor)
        else:
            self.cover_credits_html = ""
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
