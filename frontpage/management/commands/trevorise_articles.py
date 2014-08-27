"""
Converts the description field in Markdown to description_trevor.
"""

import json

from django.core.management.base import BaseCommand

from articles.models import Article
from frontpage.trevor import put_text_in_trevor


class Command(BaseCommand):
    help = "Trevorise article content"

    def handle(self, *args, **options):
        for article in Article.objects.all():
            if article.main_text:
                article.main_text_trevor = put_text_in_trevor(article.main_text)
            if article.lead_text:
                article.lead_text_trevor = put_text_in_trevor(article.lead_text)
            if article.cover_credits:
                article.cover_credits_trevor = put_text_in_trevor(article.cover_credits)
            article.save()
            print("Processed %s." % (article, ))
