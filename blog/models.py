from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length="100", null=True)
    category = models.ForeignKey(Category)
    author = models.ForeignKey(User)
    date = models.DateTimeField()
    post = models.TextField()
    more = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=True, help_text="Only admins see not-published posts")

    @models.permalink
    def get_absolute_url(self):
        return ('post', (), {
            'year': self.date.strftime("%Y"),
            'month': self.date.strftime("%m"),
            'day': self.date.strftime("%d"),
            'slug': self.slug
        })

    def __unicode__(self):
        return self.title
