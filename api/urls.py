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

from django.conf import settings
from django.conf.urls import url, patterns
from django.views.decorators.cache import (
    cache_control,
    never_cache,
)

from piston.resource import Resource

from handlers import Forecast6d_weather,Forecast3d_weather,Observe_weather,Heweather_forecast_weather,Heweather_observe_s6,Heweather_forecast_s6,Heweather_data_s6,Heweather_simple_s6

weather_cma_forecast6d = Resource(handler = Forecast6d_weather)
weather_cma_forecast3d = Resource(handler = Forecast3d_weather)
weather_observe_weather = Resource(handler = Observe_weather)

#20170627
heweather_forecast_weather = Resource(handler = Heweather_forecast_weather)


#20180827 heweather s6 version
heweather_observe_s6 = Resource(handler = Heweather_observe_s6)
heweather_forecast_s6 = Resource(handler = Heweather_forecast_s6)

#20200307 heweather s6 version
heweather_data_s6 = Resource(handler = Heweather_data_s6)
heweather_simple_s6 = Resource(handler = Heweather_simple_s6)


#service.ubuntukylin.com:8001/weather/api/3.0/heweather_data_s6/101250101/
urlpatterns = patterns(
    '',
    url(r'^1.0/forecast6d/(?P<cityid>\d+)/$', weather_cma_forecast6d),
    url(r'^1.0/forecast3d/(?P<cityid>\d+)/$', weather_cma_forecast3d),
    url(r'^1.0/observe/(?P<cityid>\d+)/$', weather_observe_weather),
    url(r'^1.0/heweather_forecast/(?P<cityid>\d+)/$', heweather_forecast_weather),
    url(r'^2.0/heweather_observe_s6/(?P<cityid>\d+)/$', heweather_observe_s6),
    url(r'^2.0/heweather_forecast_s6/(?P<cityid>\d+)/$', heweather_forecast_s6),
    url(r'^3.0/heweather_data_s6/(?P<cityid>\d+)/$', heweather_data_s6),
    url(r'^3.0/heweather_simple_s6/$', heweather_simple_s6),
)

