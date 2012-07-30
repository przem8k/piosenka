from django.db import models
from django.contrib.auth.models import User

from songs.models import Song
from events.models import Event


class Profile(models.Model):
    user = models.OneToOneField(User, blank=False)
    activation_key = models.CharField(max_length=50)

    hide_real_name = models.BooleanField(default=False)

    def email(self):
        return self.user.email

    def login(self):
        return self.user.username

    def name(self):
        return "%s %s" % (self.user.first_name, self.user.last_name,)

    def __unicode__(self):
        return self.name()


class SongAddedAction(models.Model):
    author_profile = models.ForeignKey(Profile)
    song = models.ForeignKey(Song)
    creation_date = models.DateTimeField(blank=True)


class EventAddedAction(models.Model):
    author_profile = models.ForeignKey(Profile)
    event = models.ForeignKey(Event)
    creation_date = models.DateTimeField(blank=True)
