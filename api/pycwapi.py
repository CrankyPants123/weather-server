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

"""
Fetches weather reports from Chinese Weather
"""

import os, sys
import urllib2, urllib
import json

from base import WEATHER_URL,WEATHER_URL1, WEATHER_URL2, WEATHER_URL_bak

CHN_CITY_LIST_FILE = '/usr/share/locations.txt'

def read_from_url(url):
    # returns weather info by json_string
    request = urllib2.Request(url, headers={'User-Agent' : 'Magic Browser'})
    f = urllib2.urlopen(request)
    json_string = f.read()
    f.close()
    return json_string

# 2018 和风天气api s6版本：client的主界面切换城市时从server端获取数据
def get_weather_from_nmc(location_id, method = 0):
    """
    Fetches weather report from NMC
    
    Parameters:
      location_id: City ID for request weather
      method: 'simple' 0 or 'complex' 1
    
    Returns:
      weather_data: a dictionary of weather data that exists in Json feed.
    """
    weather_data = {}
    if method == 0:
#        fi = open('/home/ccnadmin/ukylin/ubuntukylin_server/weather/api/wb.txt','a+')
#        print >> fi,'method == 0'
#        fi.close()

	flag = 1
        try:  #过滤因气象局接口失效而程序出错
            url1 = WEATHER_URL1 % (location_id)
            url2 = WEATHER_URL2 % (location_id)
            json_string1 = read_from_url(url1)
            json_string2 = read_from_url(url2)
            parsed_json1 = json.loads(json_string1)
            parsed_json2 = json.loads(json_string2)

            for key in ('city', 'temp', 'SD', 'WD', 'WS', 'time'):
                weather_data[key] = parsed_json1['weatherinfo'][key]
            for key in ('weather', 'temp1', 'temp2', 'img1', 'img2', 'ptime'):
                weather_data[key] = parsed_json2['weatherinfo'][key]

        except:
            flag = 0

#***wenbo add***
        url3 = WEATHER_URL_bak % (location_id)
        json_string3 = read_from_url(url3)
        parsed_json3 = json.loads(json_string3)
#        fi = open('/home/ccnadmin/ukylin/ubuntukylin_server/weather/api/wb.txt','a+')
#        print >> fi,'-2'
#        print >> fi, url3
#        print >> fi,parsed_json3
#        fi.close()
        if flag: # 如果气象局接口有效，再检查是否是最新天气
#            fi = open('/home/ccnadmin/ukylin/ubuntukylin_server/weather/api/wb.txt','a+')
#            print >> fi,'-1'
            #print >> fi,parsed_json3['result']
            #print >> fi,parsed_json2['weatherinfo']['temp1']
            #print >> fi,parsed_json3['result']['temp_high']
            #print >> fi,parsed_json2['weatherinfo']['temp2']
            #print >> fi,parsed_json3['result']['temp_low']
#            fi.close()
            if not (parsed_json2['weatherinfo']['temp1']==(parsed_json3['result']['temp_high']+'℃') and parsed_json2['weatherinfo']['temp2']==(parsed_json3['result']['temp_low']+'℃')):

#                fi = open('/home/ccnadmin/ukylin/ubuntukylin_server/weather/api/wb.txt','a+')
#                print >> fi,'0'
                weather_data['city'] =  parsed_json3['result']['citynm']
                weather_data['temp'] =  parsed_json3['result']['temp_curr']
                weather_data['SD'] =  '未知' #湿度没有
                weather_data['WD'] =  parsed_json3['result']['wind']
                weather_data['WS'] =  parsed_json3['result']['winp']
                weather_data['time'] =  '08:00'
                weather_data['weather'] =  parsed_json3['result']['weather']
                weather_data['temp1'] =  parsed_json3['result']['temp_high']+'℃'
                weather_data['temp2'] =  parsed_json3['result']['temp_low']+'℃'
                if weather_data['time'] == '0':
                    if not(int(weather_data['time']) >= int(parsed_json3['result']['temp_low']) and int(weather_data['time']) <= int(parsed_json3['result']['temp_high'])):
                        weather_data['time'] = '未知'
                #imag1 = parsed_json3['result']['weather_icon']
#                print >> fi,'1'
                try :
                    image2 = parsed_json3['result']['weather_icon']
                    weather_data['img1'] = 'd'+ image2[-image2.index('/'):]
                    weather_data['img2'] = 'd'+ image2[-image2.index('/'):]
                except:
                    pass
                weather_data['ptime'] = '08:00'
#                print >> fi,'2'
#                fi.close()
        else:
#            fi = open('/home/ccnadmin/ukylin/ubuntukylin_server/weather/api/wb.txt','a+')
#            print >> fi,'3'
#            fi.close()
            weather_data['city'] =  parsed_json3['result']['citynm']
            weather_data['temp'] =  parsed_json3['result']['temp_curr']
            weather_data['SD'] =  '未知' #湿度没有
            weather_data['WD'] =  parsed_json3['result']['wind']
            weather_data['WS'] =  parsed_json3['result']['winp']
            weather_data['time'] =  '08:00'
            weather_data['weather'] =  parsed_json3['result']['weather']
            weather_data['temp1'] =  parsed_json3['result']['temp_high']+'℃'
            weather_data['temp2'] =  parsed_json3['result']['temp_low']+'℃'
            if weather_data['time'] == '0':
                if not(int(weather_data['time']) >= int(parsed_json3['result']['temp_low']) and int(weather_data['time']) <= int(parsed_json3['result']['temp_high'])):
                    weather_data['time'] = '未知'
            #imag1 = parsed_json3['result']['weather_icon']
            try:
                image2 = parsed_json3['result']['weather_icon']
                weather_data['img1'] = 'd'+ image2[-image2.index('/'):]
                weather_data['img2'] = 'd'+ image2[-image2.index('/'):]
            except:
                    pass
            weather_data['ptime'] = '08:00'
#        f = open('/home/ccnadmin/ukylin/ubuntukylin_server/weather/api/wb.txt','a+')
#        st = weather_data['city']+'   '+weather_data['temp1']+'     '+weather_data['SD']
#        print >> f,st
#        f.close()

#***end***

    elif method == 1:
#        fi = open('/home/ccnadmin/ukylin/ubuntukylin_server/weather/api/wb.txt','a+')
#        print >> fi,'method == 1'
#        fi.close()
        url = WEATHER_URL % (location_id)
        json_string = read_from_url(url)
        parsed_json = json.loads(json_string)
        tp_forecast = ('city', 'city_en', 'date_y', 'date', 'week', 'fchh', 'temp1', 'temp2', 'temp3', 'temp4', 'temp5', 'temp6', \
        'tempF1', 'tempF2', 'tempF3', 'tempF4', 'tempF5', 'tempF6', 'weather1', 'weather2', 'weather3', 'weather4', 'weather5', 'weather6', \
        'img1', 'img2', 'img3', 'img4', 'img5', 'img6', 'img7', 'img8', 'img9', 'img10', 'img11', 'img12', 'img_single', 'img_title_single',\
        'img_title1', 'img_title2', 'img_title3', 'img_title4', 'img_title5', 'img_title6', \
        'img_title7', 'img_title8', 'img_title9', 'img_title10', 'img_title11', 'img_title12', \
        'wind1', 'wind2', 'wind3', 'wind4', 'wind5', 'wind6', \
        'fx1', 'fx2', 'fl1', 'fl2', 'fl3', 'fl4', 'fl5', 'fl6', \
        'index', 'index_d', 'index_uv', 'index_xc', 'index_tr', 'index_co', 'index_cl', 'index_ls', 'index_ag')
        for key in tp_forecast:
            if key == "index":#because 'index' cannot insert into mysql db, so change it to 'index_clothes'
                weather_data['index_clothes'] = parsed_json['weatherinfo'][key]
            else:
                weather_data[key] = parsed_json['weatherinfo'][key]
    else:
        print "Error,choose method for 0 or 1"
        exit(1)
    return weather_data

def get_location_from_cityid(cityid):
    """
    returns city location by search cityid, added by kobe
    """
    location = ''
    f = open(CHN_CITY_LIST_FILE, 'r')
    for line in f.readlines():
        if cityid in line:
            location = line.split(':')[0]
            break
    f.close()
    return location

if __name__ == "__main__":
    weatherinfo = get_weather_from_nmc('101281601', 1)
    print weatherinfo
    # cities = get_cities_from_localfile('长沙')
    # download_icon_from_nmc('d0.gif', 'd')
