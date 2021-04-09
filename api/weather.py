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

import base64
import os, sys
from urllib import quote, urlencode
import urllib2
import time
import uuid
import hmac, hashlib
import urllib2, urllib
import json
from datetime import *
import pycwapi
import time
#from hashlib import sha1
#my_sign = hmac.new('123457', '123456', hashlib.sha1).digest()
#my_sign = base64.b64encode(my_sign)
#print my_sign
#print "-------------------"

def get_smartweather_forecast(cityId, typeName):
    forecast_data = {}
    try:
        dt = datetime.now()
        cur_time = dt.strftime('%Y%m%d%H%M')
        #print cur_time#201404171030
        private_key = "220804_SmartWeatherAPI_4503f1c"
        public_key = "http://webapi.weather.com.cn/data/?areaid=%s&type=%s&date=%s&appid=6f2bbad491f3b77e" % (cityId, typeName, cur_time)
        print 'public_key->  ' + public_key
        #bb = hmac.new(public_key, private_key, hashlib.sha1).hexdigest()
        bb = hmac.new(private_key, public_key, hashlib.sha1).digest()
        signature = base64.b64encode(bb)
        url = "http://webapi.weather.com.cn/data/?areaid=%s&type=%s&date=%s&appid=6f2bba&key=%s" % (cityId, typeName, cur_time, signature)
        print 'url->  ' + url
        request = urllib2.Request(url, headers={'User-Agent ' : 'Magic Browser'})
        f = urllib2.urlopen(request)
        json_data = f.read()
        f.close()
        python_data = json.loads(json_data)
        if isinstance(python_data, dict):
            forecast_data = python_data
        else:
            forecast_data = python_data[-1]
    except Exception as e:
        print 'error-----'
        print e
    return forecast_data

# 2018 和风天气api s6版本：client的主界面切换城市时从server端获取数据
def get_open_weather(cityId):
    weather_data = {}
    try:
        weather_data = pycwapi.get_weather_from_nmc(cityId, 0)
        # print weather_data
    except Exception as e:
        # print 'open error-----'
        print e
    return weather_data

def get_open_forecast6d_weather(cityId):
    forecast_data = {}
    try:
        forecast_data = pycwapi.get_weather_from_nmc(cityId, 1)
        # print forecast_data
    except Exception as e:
        # print 'open error-----'
        print e
    return forecast_data

#testCity = "101010100"
#testType = "index"#实况：observe，指数：index，常规预报：forecast3d
#info = get_weather(testCity, testType)
#print "weather info-> "
#print info
# get_open_weather("101010100")


# {u'weather4': u'99', u'weather5': u'1', u'weather6': u'2', u'weather1': u'1', u'weather2': u'99', u'weather3': u'1', u'temp4': u'27\u2103~22\u2103', u'img12': u'\u5317\u98ce\u5c0f\u4e8e3\u7ea7', u'tempF6': u'\u9635\u96e8\u8f6c\u4e2d\u96e8', u'temp2': u'30\u2103~22\u2103', u'tempF4': u'\u4e2d\u96e8', u'tempF5': u'\u4e2d\u96e8', u'tempF2': u'\u591a\u4e91', u'temp6': u'27\u2103~22\u2103', u'temp5': u'25\u2103~22\u2103', u'tempF1': u'\u591a\u4e91', u'img3': u'8', u'img2': u'99', u'img1': u'8', u'img_title3': u'\u5c0f\u4e8e3\u7ea7', u'img7': u'\u5317\u98ce\u5c0f\u4e8e3\u7ea7', u'img6': u'8', u'img5': u'3', u'img4': u'99', u'city': u'\u957f\u6c99',
#  u'city_en': u'2014\u5e745\u670826\u65e5', u'fchh': u'2014-05-26 16:22:46', u'week': u'11',
# u'img_title_single': u'\u5c0f\u4e8e3\u7ea7', u'img_title12': u'\u9002\u5b9c', u'img_title10': u'\u8f83\u8212\u9002',
# u'img_title11': u'\u9002\u5b9c', u'img11': u'\u5317\u98ce\u5c0f\u4e8e3\u7ea7', u'date': u'\u661f\u671f\u4e00',
# u'wind1': u'\u6781\u4e0d\u6613\u53d1', u'date_y': u'\u56db\u6708\u5eff\u516b', u'temp3': u'31\u2103~24\u2103',
# u'img_title8': u'\u8f83\u4e0d\u5b9c', u'img_title9': u'\u9002\u5b9c', u'img_title4': u'\u5c0f\u4e8e3\u7ea7',
# u'img_title5': u'\u8212\u9002',
#  u'img_title6': u'\u5efa\u8bae\u7740\u957f\u8896T\u6064\u3001\u886c\u886b\u52a0\u5355\u88e4\u7b49\u670d\u88c5\u3002\u5e74\u8001\u4f53\u5f31\u8005\u5b9c\u7740\u9488\u7ec7\u957f\u8896\u886c\u886b\u3001\u9a6c\u7532\u548c\u957f\u88e4\u3002', u'img_title7': u'\u5f31',
# u'img_title1': u'\u5c0f\u4e8e3\u7ea7', u'img9': u'\u5357\u98ce\u5c0f\u4e8e3\u7ea7',
# u'img10': u'\u5357\u98ce\u8f6c\u5317\u98ce\u5c0f\u4e8e3\u7ea7', u'img8': u'\u5317\u98ce\u5c0f\u4e8e3\u7ea7',
#  u'temp1': u'27\u2103~20\u2103', u'img_title2': u'\u5c0f\u4e8e3\u7ea7', u'img_single': u'\u5c0f\u4e8e3\u7ea7',
#  u'tempF3': u'\u591a\u4e91\u8f6c\u9634'}
