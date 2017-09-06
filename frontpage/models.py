from django.db import models

from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases
from markdown import markdown

saved_file.connect(generate_aliases)
