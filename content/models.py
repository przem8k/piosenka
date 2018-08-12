from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from base.overrides import overrides
from content.slug import SlugFieldMixin
import content.trevor as trevor


def get_default_author():
    """ Not used anymore. TODO: delete when migrations are squashed. """
    pass


def get_default_pub_date():
    pass


class ContentItem(models.Model):
    author = models.ForeignKey(User, editable=False, on_delete=models.CASCADE)
    reviewed = models.BooleanField(default=False, editable=False)
    pub_date = models.DateTimeField(editable=False)

    class Meta:
        abstract = True
        default_permissions = []

    def save(self, *args, **kwargs):
        if not self.pub_date:
            self.pub_date = timezone.now()
        return super().save(*args, **kwargs)

    @classmethod
    def items_live(cls):
        return cls.objects.filter(reviewed=True)

    @classmethod
    def items_visible_to(cls, user):
        if user and user.is_authenticated:
            return cls.objects.all()
        return cls.items_live()

    @classmethod
    def items_reviewable_by(cls, user):
        if user and user.is_authenticated and user.has_perm('content.review'):
            return cls.objects.filter(reviewed=False).exclude(author=user)
        else:
            return []

    def can_be_seen_by(self, user):
        return self.is_live() or (user.is_active and user.is_authenticated)

    def can_be_edited_by(self, user):
        return (user.is_active and user.is_authenticated and
                (user == self.author or user.has_perm('content.review')))

    def can_be_approved_by(self, user):
        return (not self.is_live() and user.is_active and
                user.is_authenticated and user.has_perm('content.review') and
                user != self.author)

    def is_live(self):
        return self.reviewed


class Note(SlugFieldMixin, ContentItem):
    """Represents a note complementing the information from a main item."""
    HELP_TITLE = 'Tytuł adnotacji.'
    HELP_IMAGE = 'Ilustracja.'
    HELP_IMAGE_URL = 'Źródło zdjęcia (adres www).'
    HELP_IMAGE_AUTHOR = 'Źródło zdjęcia (autor).'
    HELP_IMAGE_LICENSE = 'Źródło zdjęcia (licencja).'
    HELP_TEXT = 'Treść adnotacji.'
    HELP_SOURCE_URL = 'Źródło (adres www).'
    HELP_SOURCE_REF = 'Źródło (nazwa i autor publikacji).'

    title = models.CharField(max_length=100, help_text=HELP_TITLE)
    image = models.ImageField(
        null=True, blank=True, upload_to='notes', help_text=HELP_IMAGE)
    image_url = models.URLField(null=True, blank=True, help_text=HELP_IMAGE_URL)
    image_author = models.CharField(
        null=True, blank=True, max_length=50, help_text=HELP_IMAGE_AUTHOR)
    image_license = models.CharField(
        null=True, blank=True, max_length=50, help_text=HELP_IMAGE_LICENSE)
    text_trevor = models.TextField(help_text=HELP_TEXT)
    text_html = models.TextField(editable=False)
    url1 = models.URLField(null=True, blank=True, help_text=HELP_SOURCE_URL)
    url2 = models.URLField(null=True, blank=True, help_text=HELP_SOURCE_URL)
    ref1 = models.TextField(null=True, blank=True, help_text=HELP_SOURCE_REF)
    ref2 = models.TextField(null=True, blank=True, help_text=HELP_SOURCE_REF)

    class Meta:
        abstract = True

    def get_parent(self):
        raise NotImplementedError

    def __str__(self):
        return self.title

    def get_id(self):
        return self.slug

    def get_absolute_url(self):
        return self.get_parent().get_absolute_url() + '#' + self.get_id()

    def save(self, *args, **kwargs):
        self.text_html = trevor.render_trevor(self.text_trevor)
        super().save(*args, **kwargs)

    @overrides(SlugFieldMixin)
    def get_slug_elements(self):
        return [self.title, self.get_parent().slug]


class Permissions(models.Model):
    """Dummy model used to define additional permissions not tied to a
    particular model.
    """

    class Meta:
        permissions = [('review', 'Can review content items.')]
