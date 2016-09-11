import uuid

from django.db import models

from easy_thumbnails.signal_handlers import generate_aliases
from easy_thumbnails.signals import saved_file

from base.overrides import overrides
from content import url_scheme
from content.trevor import render_trevor, put_text_in_trevor
from content.models import ContentItem
from content.slug import SlugFieldMixin

saved_file.connect(generate_aliases)


class Article(SlugFieldMixin, url_scheme.ViewEditReviewApprove, ContentItem):
    HELP_TITLE = """\
Tytuł artykułu, np. 'IX Festiwal Piosenki Poetyckiej im. Jacka Kaczmarskiego \
"Nadzieja"'."""
    HELP_COVER_IMAGE = """\
Main illustration for the article."""

    title = models.CharField(max_length=100, help_text=HELP_TITLE)
    lead_text_trevor = models.TextField()
    main_text_trevor = models.TextField()
    cover_image = models.ImageField(null=True,
                                    blank=True,
                                    upload_to='article_covers',
                                    help_text=HELP_COVER_IMAGE)
    cover_credits_trevor = models.TextField(null=True, blank=True)

    lead_text_html = models.TextField(editable=False)
    main_text_html = models.TextField(editable=False)
    cover_credits_html = models.TextField(null=True, blank=True, editable=False)

    @staticmethod
    def create_for_testing(author):
        article = Article()
        article.author = author
        article.title = str(uuid.uuid4()).replace('-', '')
        article.lead_text_trevor = put_text_in_trevor('Abc')
        article.main_text_trevor = put_text_in_trevor('Abc')
        article.save()
        return article

    class Meta(ContentItem.Meta):
        ordering = ['-pub_date']

    def __str__(self):
        return self.title

    @overrides(SlugFieldMixin)
    def get_slug_elements(self):
        assert self.title
        return [self.title]

    @overrides(url_scheme.ViewEditReviewApprove)
    def get_url_name(self):
        return 'article'

    def save(self, *args, **kwargs):
        self.lead_text_html = render_trevor(self.lead_text_trevor)
        self.main_text_html = render_trevor(self.main_text_trevor)
        if self.cover_credits_trevor:
            self.cover_credits_html = render_trevor(self.cover_credits_trevor)
        else:
            self.cover_credits_html = ''
        super().save(*args, **kwargs)

    def get_url_params(self):
        return {'slug': self.slug}
