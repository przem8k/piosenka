"""
 Command creates missing user profiles (for users added via admin panel
    before the public registration was made available)
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from users.models import Profile
from users.registration import generate_activation_key


class Command(BaseCommand):
    help = "Create missing user profiles"

    def handle(self, *args, **options):
        for user in User.objects.all():
            if Profile.objects.filter(user=user).count() == 0:
                print "No profile for user: %s" % (user,)
                new_profile = Profile(user=user, activation_key=generate_activation_key(user.username))
                new_profile.save()
                print "Created new profile for username: %s" % (user.username,)
