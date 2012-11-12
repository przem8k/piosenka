from django.db import models

class ArticleCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "ArticleCategories"

    def __unicode__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    category = models.ForeignKey(ArticleCategory, null=True, empty=True)
    date = models.DateTimeField()
    lead_text = models.TextField(help_text="Introductory paragraph, written in Markdown")
    main_text = models.TextField(help_text="Rest of the article, written in Markdown")
    published = models.BooleanField(default=True)
    author = models.ForeignKey(User)
    cover = models.ImageField(null=True, blank=True, upload_to='articles', help_text="Main illustration for the article.")

