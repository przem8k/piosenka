from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from unidecode import unidecode


class SlugLogicMixin(object):
    """Bring your-own slug field slug mixin.

    This assumes that a slug field is already defined on the object."""

    def get_slug_elements(self):
        raise NotImplementedError

    # TODO: make private?
    def make_slug(self, slug_elements):
        normalized_string = unidecode(" ".join(slug_elements))
        max_length = self._meta.get_field("slug").max_length
        return slugify(normalized_string)[:max_length]

    def get_slug(self):
        return self.make_slug(self.get_slug_elements())

    def clean(self):
        if not self.slug:
            self.slug = self.get_slug()

        if not self.pk and self.__class__.objects.filter(slug=self.slug):
            raise ValidationError(
                "Materiał o takich parametrach już jest bazie. "
                "Upewnij się, że nie dodajesz przypadkiem duplikatu. "
                "Jeśli chodzi o piosenkę, możesz użyć wyróżnika "
                "aby wskazać, że to inna piosenka."
            )
        return super().clean()


class SlugFieldMixin(SlugLogicMixin, models.Model):
    slug = models.SlugField(max_length=100, unique=True, editable=False)

    class Meta:
        abstract = True
