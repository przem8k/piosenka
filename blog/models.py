from django.db import models

from content.trevor import render_trevor, put_text_in_trevor
from content.models import ContentItem, LiveContentManager
from content.slug import SlugMixin


class Post(SlugMixin, ContentItem):
    HELP_TITLE = "Tytuł posta, np. 'Nowa wyszukiwarka piosenek.'."

    objects = models.Manager()
    live = LiveContentManager()

    title = models.CharField(max_length=100,
                             help_text=HELP_TITLE)
    post_trevor = models.TextField()
    more_trevor = models.TextField(null=True, blank=True)

    slug = models.SlugField(max_length=100, unique=True, editable=False)
    post_html = models.TextField(null=True, editable=False)
    more_html = models.TextField(null=True, editable=False)

    @staticmethod
    def create_for_testing():
        import uuid
        post = Post()
        post.title = str(uuid.uuid4()).replace("-", "")
        post.post_trevor = put_text_in_trevor("Abc")
        post.more_trevor = put_text_in_trevor("Abc")
        return post

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.title

    # SlugMixin:
    def get_slug_elements(self):
        assert self.title
        return [self.title]

    def save(self, *args, **kwargs):
        self.post_html = render_trevor(self.post_trevor)
        if self.more_trevor:
            self.more_html = render_trevor(self.more_trevor)
        else:
            self.more_html = ""
        super().save(*args, **kwargs)

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

    @models.permalink
    def get_approve_url(self):
        return ('approve_post', (), {
            'year': self.pub_date.strftime("%Y"),
            'month': self.pub_date.strftime("%m"),
            'day': self.pub_date.strftime("%d"),
            'slug': self.slug
        })
