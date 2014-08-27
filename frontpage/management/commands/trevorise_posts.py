"""
Converts the description field in Markdown to description_trevor.
"""

import json

from django.core.management.base import BaseCommand

from blog.models import Post
from frontpage.trevor import put_text_in_trevor


class Command(BaseCommand):
    help = "Trevorise post content"

    def handle(self, *args, **options):
        for post in Post.objects.all():
            if post.post:
                post.post_trevor = put_text_in_trevor(post.post)
            if post.more:
                post.more_trevor = put_text_in_trevor(post.more)
            post.save()
            print("Processed %s." % (post, ))
