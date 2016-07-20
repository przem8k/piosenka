from django.contrib import admin
from django.contrib.auth.models import Permission

from piosenka.models import Invitation

admin.site.register(Invitation)
admin.site.register(Permission)
