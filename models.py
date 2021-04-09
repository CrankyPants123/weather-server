#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_syncdb
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import utc

import os.path
import random
import struct
import string

class Pingback_weather(models.Model):
    ip = models.CharField(max_length = 64)
    distro = models.CharField(max_length = 64)
    version_os = models.CharField(max_length = 64)
    version_weather = models.CharField(max_length = 64)
    city = models.CharField(max_length = 64)
    date = models.DateTimeField(default=datetime.now().replace(tzinfo=utc))
    enable = models.BooleanField()
