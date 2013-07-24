from markdown import markdown
from sorl.thumbnail import ImageField

from django.db import models

class CarouselItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(help_text="Description, written in Markdown.")
    description_html = models.TextField(null=True, blank=True, editable=False)
    position = models.IntegerField()
    image = ImageField(upload_to='carousel_items', help_text="Picture to display in carousel.")
    archived = models.BooleanField(default=False)

    class Meta:
        ordering = ["position"]

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.description_html = markdown(self.description, safe_mode='escape')
        super(CarouselItem, self).save(*args, **kwargs)
