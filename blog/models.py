from markdown import markdown
import datetime
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length="100", null=True)
    author = models.ForeignKey(User)
    date = models.DateTimeField(editable=False)
    post = models.TextField(help_text="Post or its introductory part, written in Markdown.")
    post_html = models.TextField(null=True, blank=True, editable=False)
    more = models.TextField(blank=True, null=True, help_text="Optional rest of the post, written in Markdown.")
    more_html = models.TextField(null=True, blank=True, editable=False)
    published = models.BooleanField(default=True, help_text="Only admins see not-published posts")

    @models.permalink
    def get_absolute_url(self):
        return ('post_detail', (), {
            'year': self.date.strftime("%Y"),
            'month': self.date.strftime("%m"),
            'day': self.date.strftime("%d"),
            'slug': self.slug
        })

    def save(self, *args, **kwargs):
        self.post_html = markdown(self.post, safe_mode='escape')
        self.more_html = markdown(self.more, safe_mode='escape')
        if not self.date and self.published:
            self.date = datetime.datetime.now()
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-date"]

    def __unicode__(self):
        return self.title
