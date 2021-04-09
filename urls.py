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
from django.conf.urls import (
    patterns,
    include,
    url,
)
from django.views.decorators.cache import never_cache
from piston.resource import Resource
from handlers import Pingbackmain, Pingnetwork

weather_pingbackmain = Resource(handler = Pingbackmain)

weather_pingnetwork = Resource(handler = Pingnetwork)
weather_pingnetwork.__name__ = "Resource"

urlpatterns = patterns('',
    url(r'^api/', include('weather.api.urls')),
    url(r'^pingbackmain/$', weather_pingbackmain),
    url(r'^pingnetwork/$', weather_pingnetwork),
)
