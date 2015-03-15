from django.db import models

from easy_thumbnails.signal_handlers import generate_aliases
from easy_thumbnails.signals import saved_file

from piosenka.trevor import render_trevor, put_text_in_trevor
from piosenka.models import ContentItem, LiveContentManager

saved_file.connect(generate_aliases)


class Article(ContentItem):
    HELP_TITLE = """\
Tytuł artykułu, np. 'IX Festiwal Piosenki Poetyckiej im. Jacka Kaczmarskiego \
"Nadzieja"'."""
    HELP_COVER_IMAGE = """\
Main illustration for the article."""

    objects = models.Manager()
    live = LiveContentManager()

    title = models.CharField(max_length=100, help_text=HELP_TITLE)
    lead_text_trevor = models.TextField()
    main_text_trevor = models.TextField()
    cover_image = models.ImageField(null=True, blank=True,
                                    upload_to='article_covers',
                                    help_text=HELP_COVER_IMAGE)
    cover_credits_trevor = models.TextField(null=True, blank=True)

    slug = models.SlugField(max_length=100, unique=True, editable=False)
    lead_text_html = models.TextField(editable=False)
    main_text_html = models.TextField(editable=False)
    cover_credits_html = models.TextField(null=True, blank=True, editable=False)

    @staticmethod
    def create_for_testing():
        import uuid
        article = Article()
        article.title = str(uuid.uuid4()).replace("-", "")
        article.lead_text_trevor = put_text_in_trevor("Abc")
        article.main_text_trevor = put_text_in_trevor("Abc")
        return article

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
        super().save(*args, **kwargs)

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

    @models.permalink
    def get_approve_url(self):
        return ('approve_article', (), {
            'slug': self.slug
        })
