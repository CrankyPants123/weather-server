#!/usr/bin/python
# -*- coding: utf-8 -*-
### BEGIN LICENSE
# Author: Kobe Lee
# Copyright (C) 2013 ~ 2014 National University of Defense Technology(NUDT) & Kylin Ltd
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

import json
#import pytz
import urllib

from datetime import (
    date,
    datetime,
    time,
    timedelta,
)

import os
import sys
from django.conf import settings
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

from server import AppServer#, CHN_CITY_LIST_FILE#weather.api.
#from base import PROJECT_ROOT_DIRECTORY
LOCATION_PATH = '/usr/share/locations.txt'

HttpResponse._is_string = True
HttpResponseBadRequest._is_string = True
HttpResponseNotFound._is_string = True
HttpResponseForbidden._is_string = True

#20170627
class Heweather_forecast_weather(BaseHandler):

    allowed_methods = ('GET',)

    def read(self, request, cityid):

        if request.GET:
            return HttpResponseBadRequest(
                "This api call does not take GET parameters.")

        server_object = AppServer()
        res = server_object.get_heweather_forecast_weather(cityid)
        return res



#20180827 heweather s6 version
class Heweather_observe_s6(BaseHandler):

    allowed_methods = ('GET',)

    def read(self, request, cityid):

        if request.GET:
            return HttpResponseBadRequest(
                "This api call does not take GET parameters.")

        server_object = AppServer()
        res = server_object.get_heweather_observe_s6(cityid)
        return HttpResponse(res, content_type="application/json")

class Heweather_forecast_s6(BaseHandler):

    allowed_methods = ('GET',)

    def read(self, request, cityid):

        if request.GET:
            return HttpResponseBadRequest(
                "This api call does not take GET parameters.")

        server_object = AppServer()
        res = server_object.get_heweather_forecast_s6(cityid)
        return HttpResponse(res, content_type="application/json")







class Forecast6d_weather(BaseHandler):

    allowed_methods = ('GET',)

    def read(self, request, cityid):

        if request.GET:
            return HttpResponseBadRequest(
                "This api call does not take GET parameters.")

        server_object = AppServer()
        res = server_object.get_cma_forecast6d_weather(cityid)
        return res

class Forecast3d_weather(BaseHandler):

    allowed_methods = ('GET',)

    def read(self, request, cityid):

        if request.GET:
            return HttpResponseBadRequest(
                "This api call does not take GET parameters.")

        server_object = AppServer()
        res = server_object.get_cma_forecast3d_weather(cityid)
        return res

class Observe_weather(BaseHandler):

    allowed_methods = ('GET',)

    def read(self, request, cityid):
#        cityname = self.get_cityname(cityid)
        if request.GET:
            return HttpResponseBadRequest(
                "This api call does not take GET parameters.")

        server_object = AppServer()
        res = server_object.get_heweather_observe_weather(cityid)
#        res = server_object.get_cma_observe_weather(cityid,cityname)
        return res



#20200308
class Heweather_data_s6(BaseHandler):

    allowed_methods = ('GET',)

    def read(self, request, cityid):

        if request.GET:
            return HttpResponseBadRequest(
                "This api call does not take GET parameters.")

        server_object = AppServer()
        res = server_object.heweather_s6_all_data_api(cityid)
        return HttpResponse(res, content_type="application/json")


class Heweather_simple_s6(BaseHandler):

    allowed_methods = ('GET',)

    def read(self, request):

        #if request.GET:
        #    return HttpResponseBadRequest(
        #        "This api call does not take GET parameters.")

        cityids = request.GET.get('cityids')
        server_object = AppServer()
        res = server_object.heweather_s6_simple_data_api(cityids)
        return HttpResponse(res, content_type="application/json")

#CHN_CITY_LIST_FILE = os.path.join(PROJECT_ROOT_DIRECTORY, 'src/locations.txt')

    def get_cityname(self, cityid):
        # print "sfasdfasf###",LOCATION_PATH
        with open(LOCATION_PATH) as f:
            for line in f:
                if line.strip():
                    city = line.rstrip('\n').split(':')
                    if city[1] == cityid:
                        return city[0]
