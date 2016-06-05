from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone


class ContentItem(models.Model):
    # Cards are item types that are displayed alongside the parent item. They
    # don't have an absolute url of their own, but defer to the parent instead.
    is_card = False

    author = models.ForeignKey(User, editable=False)
    reviewed = models.BooleanField(default=False, editable=False)
    pub_date = models.DateTimeField(editable=False)

    class Meta:
        abstract = True
        default_permissions = ['contribute']

    def save(self, *args, **kwargs):
        if not self.pub_date:
            self.pub_date = timezone.now()
        return super().save(*args, **kwargs)

    @classmethod
    def items_live(cls):
        return cls.objects.filter(reviewed=True)

    @classmethod
    def items_visible_to(cls, user):
        if user and user.is_authenticated():
            return cls.objects.all()
        return cls.items_live()

    @classmethod
    def items_reviewable_by(cls, user):
        if user and user.is_authenticated() and user.has_perm('content.review'):
            return cls.objects.filter(reviewed=False).exclude(author=user)
        else:
            return []

    @classmethod
    def permstring(cls):
        content_type = ContentType.objects.get_for_model(cls)
        return "%s.contribute_%s" % (content_type.app_label, content_type.model)

    @classmethod
    def can_be_contributed_by(cls, user):
        return user.has_perm(cls.permstring())

    def can_be_seen_by(self, user):
        return self.is_live() or (user.is_active and user.is_authenticated())

    def can_be_edited_by(self, user):
        return (user.is_active and
                user.is_authenticated() and
                (user == self.author or user.has_perm('content.review')))

    def can_be_approved_by(self, user):
        return (not self.is_live() and
                user.is_active and
                user.is_authenticated() and
                user.has_perm('content.review') and
                user != self.author)

    def is_live(self):
        return self.reviewed


class Permissions(models.Model):
    """Dummy model used to define additional permissions not tied to a
    particular model.
    """

    class Meta:
        permissions = [('review', 'Can review content items.')]
