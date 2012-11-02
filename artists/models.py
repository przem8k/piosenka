# coding=utf-8

from django.db import models


class Artist(models.Model):
    firstname = models.CharField(max_length=25)
    lastname = models.CharField(max_length=25)
    slug = models.SlugField(max_length=100, unique=True, help_text="Used in urls, has to be unique", default="void")
    display = models.BooleanField()
    website = models.URLField(null=True, blank=True)

    KIND_TEXTER = 1
    KIND_COMPOSER = 2
    KIND_TRANSLATOR = 3
    KIND_PERFORMER = 4
    KIND_POET = 5
    KIND_FOREIGN = 6
    ARTIST_KINDS = (
        (KIND_TEXTER, u'Wykonawca własnych tekstów'),
        (KIND_COMPOSER, u'Kompozytor'),
        (KIND_TRANSLATOR, u'Tłumacz'),
        (KIND_PERFORMER, u'Wykonawca cudzych piosenek'),
        (KIND_POET, u'Poeta nieśpiewający'),
        (KIND_FOREIGN, u'Bard zagraniczny'),
    )
    kind = models.IntegerField(choices=ARTIST_KINDS, null=True, blank=True, help_text="Select the most prominent thing the person is famous for.")

    def get_absolute_url(self):
        return "/spiewnik/%s/" % self.slug

    def __unicode__(self):
        return self.firstname + " " + self.lastname

    class Meta:
        ordering = ["lastname", "firstname", ]


class Band(models.Model):
    name = models.CharField(max_length=50)
    members = models.ManyToManyField(Artist, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, help_text="Used in urls, has to be unique.")
    display = models.BooleanField()
    website = models.URLField(null=True, blank=True)

    def get_absolute_url(self):
        return "/spiewnik/%s/" % self.slug

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name", ]
