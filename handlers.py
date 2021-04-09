#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import urllib

from datetime import (
    date,
    datetime,
    time,
    timedelta,
)

import os,sys,tempfile,zipfile
from django.conf import settings
from django.core.servers.basehttp import FileWrapper
from django.core.serializers.json import DjangoJSONEncoder
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    HttpResponseForbidden,
)
from django.shortcuts import get_object_or_404
from django.utils import datetime_safe
from piston.emitters import (
    Emitter,
    JSONEmitter,
)
from piston.handler import BaseHandler
from piston.utils import Mimer
from models import (
    Pingback_weather,
)
from forms import PingbackmainForm

HttpResponse._is_string = True
HttpResponseBadRequest._is_string = True
HttpResponseNotFound._is_string = True
HttpResponseForbidden._is_string = True

from django.utils.timezone import utc

class Pingbackmain(BaseHandler):
    allowed_methods = ('POST',)

    def create(self,request):
        form = PingbackmainForm(request.data)
        if not form.is_valid():
            return False
        po_distro = form.cleaned_data['distro']
        po_version_os = form.cleaned_data['version_os']
        po_version_weather = form.cleaned_data['version_weather']
        po_city = form.cleaned_data['city']
        po_date = datetime.now().replace(tzinfo=utc)
        po_enable = True
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            po_ip =  request.META['HTTP_X_FORWARDED_FOR']
        else:
            po_ip = request.META['REMOTE_ADDR']
        pingweather = Pingback_weather(ip = po_ip, distro = po_distro, version_os = po_version_os, version_weather = po_version_weather, city = po_city, date = po_date, enable = po_enable)
        pingweather.save()
        return True

class Pingnetwork(BaseHandler):
    allowed_methods = ('GET',)

    def read(self,request):
        return True
