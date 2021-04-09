#!/usr/bin/env python
# -*- coding: utf-8 -*-

### BEGIN LICENSE
# Copyright (C) 2013 ~ 2014 National University of Defense Technology(NUDT) & Kylin Ltd
# Author: Kobe Lee
#
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

import os, sys
import time, httplib
# from gi.repository import GObject


# def get_parent_path(folderpath, level=1):
#     parent_path = os.path.realpath(folderpath)
#     while(level > 0):
#         parent_path = os.path.dirname(parent_path)
#         level -= 1
#     return parent_path

# def get_http_time():
#     try:
#         conn = httplib.HTTPConnection("www.beijing-time.org")
#         conn.request("GET", "/time.asp")
#         response = conn.getresponse()
#         if response.status == 200:
#             result = response.read()
#             data = result.split("\r\n")
#             print data#['t0=new Date().getTime();', 'nyear=2014;', 'nmonth=5;', 'nday=7;', 'nwday=3;', 'nhrs=13;', 'nmin=32;', 'nsec=2;']
#             year = data[1][len("nyear")+1 : len(data[1])-1]
#             month = data[2][len("nmonth")+1 : len(data[2])-1]
#             day = data[3][len("nday")+1 : len(data[3])-1]
#             hrs = data[5][len("nhrs")+1 : len(data[5])-1]
#             bjtime = "%s-%s-%s %s hour" % (year, month, day, hrs)
#             print bjtime
#     except:
#         print "00-00-00 00"

def get_local_format_time():
    '''
    year-month-day hour:minute:second
    2014-05-07 13:51:30
    '''
    local_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return local_date

# def get_local_normal_time():
#     '''
#     year month day hour minute
#     201405071351
#     '''
#     local_date = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
#     return local_date

# WEATHER_URL = 'http://m.weather.com.cn/data/%s.html'
WEATHER_URL = 'http://m.weather.com.cn/atad/%s.html'
WEATHER_URL1 = 'http://www.weather.com.cn/data/sk/%s.html'
WEATHER_URL2 = 'http://www.weather.com.cn/data/cityinfo/%s.html'
PM25_URL = 'http://pm25.in/api/querys/pm2_5.json?city='
WEATHER_URL_bak = 'http://api.k780.com:88/?app=weather.today&weaid=%s&appkey=13342&sign=94e85c3e0c85d051cca43fcada6881b9&format=json'
# attention: PM2.5 APPKey From Email:kobe24_lixiang@126.com
TOKEN = '&token=yqpL46DpUeYqcqsox7bM'
# attention: PM2.5 APPKey From Email:xiangli@ubuntukylin.com
#TOKEN = '&token=wYpDvD83HMDy553JqFNx'

# PROJECT_ROOT_DIRECTORY = os.path.abspath(
    # os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0]))))
# DATA_PATH = os.path.join(PROJECT_ROOT_DIRECTORY, "data")
# ICON_PATH = os.path.join(PROJECT_ROOT_DIRECTORY, "icons")
# SERVER_IP = '192.168.30.156'#'192.168.1.105'#'192.168.30.156'#'192.168.30.231'#
# SERVER_URL = 'http://' + SERVER_IP + ':8888/RPC2'
# QSETTING_PATH = 'ubuntukylin/weaher-app'
# QSETTING_FILE = 'ubuntukylin-weaher-app'
