#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from django import forms
from django.conf import settings
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
import json

class JSONErrorMixin(object):
    def errors_json(self):
        errs = dict((key, [unicode(v) for v in values])
                        for (key, values) in self.errors.items())
        return json.dumps({'errors': errs})

class PingbackmainForm(forms.Form, JSONErrorMixin):
    distro = forms.CharField(max_length = 64)
    version_os = forms.CharField(max_length = 64)
    version_weather = forms.CharField(max_length = 64)
    city = forms.CharField(max_length = 64)
