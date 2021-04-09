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

__author__ = 'lixiang'

import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from weather import get_smartweather_forecast, get_open_weather, get_open_forecast6d_weather
import urllib2, urllib
import json
from pm25 import get_pm
from base import get_local_format_time
from database import DataBase
CHN_CITY_LIST_FILE = '/usr/share/locations.txt'
import logging, logging.handlers

global roundVal#在使用前初次声明
roundVal = False#给全局变量赋值
#
#WEATHER_UK_URL = 'https://free-api.heweather.com/v5/weather?city=CN%s&key=a3c0a9ef33b44257a6c8f2643a42e5b3'
#WEATHER_HB_URL = 'https://free-api.heweather.com/v5/weather?city=CN%s&key=40cc3ec6bbbf4de6a04029e207c986fd'

#example:   https://free-api.heweather.com/s6/weather?location=CN101250101&key=a3c0a9ef33b44257a6c8f2643a42e5b3

WEATHER_UK_AQI_URL = 'https://free-api.heweather.com/s6/air/now?location=CN%s&key=a3c0a9ef33b44257a6c8f2643a42e5b3'
WEATHER_UK_URL = 'https://free-api.heweather.com/s6/weather?location=CN%s&key=a3c0a9ef33b44257a6c8f2643a42e5b3'
WEATHER_HB_AQI_URL = 'https://free-api.heweather.com/s6/air/now?location=CN%s&key=40cc3ec6bbbf4de6a04029e207c986fd'
WEATHER_HB_URL = 'https://free-api.heweather.com/s6/weather?location=CN%s&key=40cc3ec6bbbf4de6a04029e207c986fd'


#HEWEATHER_AIR_NOW_URL = 'https://free-api.heweather.net/s6/air/now?location=CN%s&key=a3c0a9ef33b44257a6c8f2643a42e5b3'
#HEWEATHER_WEATHER_URL = 'https://free-api.heweather.net/s6/weather?location=CN%s&key=40cc3ec6bbbf4de6a04029e207c986fd'

#email: lixiang@kylinos.cn      phone: 15116165128
HEWEATHER_AIR_NOW_URL = 'https://free-api.heweather.net/s6/air/now?location=CN%s&key=9d230098dd0546c5bfd8e55ae4499f18'
HEWEATHER_WEATHER_URL = 'https://free-api.heweather.net/s6/weather?location=CN%s&key=9d230098dd0546c5bfd8e55ae4499f18'

#email: wenbo@kylinos.cn
HEWEATHER_AIR_NOW_URL = 'https://free-api.heweather.net/s6/air/now?location=CN%s&key=7aa7ca44344c40aa8aa5d6b8568e827d'
HEWEATHER_WEATHER_URL = 'https://free-api.heweather.net/s6/weather?location=CN%s&key=7aa7ca44344c40aa8aa5d6b8568e827d'


#http://127.0.0.1:8000/weather/api/1.0/forecast3d/cityid
#http://127.0.0.1:8000/weather/api/1.0/observe/cityid/cityname
weather_icons={
            '100': 'd0.gif',
            '101': 'd1.gif',
            '102': 'd2.gif',
            '103': 'd1.gif',
            '104': 'd2.gif',
            '200': 'd20.gif',
            '201': 'd18.gif',
            '202': 'd18.gif',
            '203': 'd18.gif',
            '204': 'd18.gif',
            '205': 'd18.gif',
            '206': 'd18.gif',
            '207': 'd18.gif',
            '208': 'd18.gif',
            '209': 'd18.gif',
            '210': 'd18.gif',
            '211': 'd18.gif',
            '212': 'd18.gif',
            '213': 'd18.gif',
            '300': 'd4.gif',
            '301': 'd4.gif',
            '302': 'd4.gif',
            '303': 'd4.gif',
            '304': 'd4.gif',
            '305': 'd7.gif',
            '306': 'd9.gif',
            '307': 'd7.gif',
            '308': 'd4.gif',
            '309': 'd4.gif',
            '310': 'd4.gif',
            '311': 'd4.gif',
            '312': 'd4.gif',
            '313': 'd4.gif',
            '400': 'd6.gif',
            '401': 'd6.gif',
            '402': 'd6.gif',
            '403': 'd6.gif',
            '404': 'd6.gif',
            '405': 'd6.gif',
            '406': 'd6.gif',
            '407': 'd6.gif',
            '500': 'd18.gif',
            '501': 'd18.gif',
            '502': 'd18.gif',
            '503': 'd18.gif',
            '504': 'd18.gif',
            '507': 'd18.gif',
            '508': 'd18.gif',
            '900': 'd18.gif',
            '901': 'd18.gif'
        }

def read_json_from_url(url):
    # returns weather info by json_string
    request = urllib2.Request(url, headers={'User-Agent' : 'Magic Browser'})
    f = urllib2.urlopen(request)
    json_string = f.read()
    f.close()
    return json_string

class AppServer:
    def __init__(self):
        # self.observeStat = ObserveStat("kobe")
        self.db = DataBase()
        # global log
        # cachedir = os.environ.get('XDG_CACHE_HOME','').strip()
        # if not cachedir:
        #     cachedir = os.path.expanduser("~/.cache")
        # log_filename = os.path.join(cachedir, "weather.log")
        # log = logging.getLogger('KobeLee')
        # log.propagate = False
        # log.setLevel(logging.DEBUG)
        # log_handler = logging.handlers.RotatingFileHandler(log_filename, maxBytes=1024*1024, backupCount=5)
        # log_formatter = logging.Formatter("[%(asctime)s - %(levelname)s - %(message)s")
        # log_handler.setFormatter(log_formatter)
        # log.addHandler(log_handler)
        # log.info("--Started UbuntuKylin Weather App from %s --" % os.path.abspath(os.path.curdir))

    def init_and_update_observe_table(self):
        """
        init or update observe all items
        """
        # print CHN_CITY_LIST_FILE
        location = ''
        id = ''
        f = open(CHN_CITY_LIST_FILE, 'r')
        for line in f.readlines():
            line_list = line.strip('\n').split(':')
            location = line_list[0]
            id = line_list[1]
            pm = get_pm(location)
            # get current weather
            weather_dict = get_open_weather(id)
            if weather_dict not in ('', None, [], {}):
                if 'error' in pm or pm == False:
                    weather_dict['aqi'] = '无数据'#'N/A'
                else:
                    weather_dict['aqi'] = pm['quality'] + '(' + str(pm['aqi']) + ')'
                db_record = self.db.search_observe_record(str(id))
                # db_record = []
                now_date = get_local_format_time()
                if db_record != []:#update
                    self.db.update_observe_data(weather_dict['ptime'],weather_dict['time'],now_date,weather_dict['WD'],weather_dict['WS'],weather_dict['SD'],weather_dict['weather'],weather_dict['img1'],weather_dict['img2'],weather_dict['temp'],weather_dict['temp1'],weather_dict['temp2'],weather_dict['aqi'],id)
                else:#insert
                    self.db.insert_observe_data(id,weather_dict['city'],weather_dict['ptime'],weather_dict['time'],now_date,weather_dict['WD'],weather_dict['WS'],weather_dict['SD'],weather_dict['weather'],weather_dict['img1'],weather_dict['img2'],weather_dict['temp'],weather_dict['temp1'],weather_dict['temp2'],weather_dict['aqi'])
        f.close()
        return True



#-------------------------------------------20170627 start------------------------------------------------
    # 2018 和风天气api s6版本： 天气预报界面显示时从server端获取数据, called by get_heweather_observe_weather
    def access_heweather_forecast_and_observe(self, cityid, selected):
        weather_data = {}
        forecast3d_dict = {}
        observe_key_list = ['city', 'ptime', 'time', 'WD', 'WS', 'SD', 'weather', 'img1', 'img2', 'temp', 'temp1', 'temp2', 'aqi']
        forecast_key_list = ['date0','astro_mr0','astro_ms0','astro_sr0','astro_ss0','code_d0','code_n0','txt_d0','txt_n0','hum0','pcpn0','pop0','pres0','tmp_max0','tmp_min0','uv0','vis0','wind_deg0','wind_dir_sc0','wind_spd0','date1','astro_mr1','astro_ms1','astro_sr1','astro_ss1','code_d1','code_n1','txt_d1','txt_n1','hum1','pcpn1','pop1','pres1','tmp_max1','tmp_min1','uv1','vis1','wind_deg1','wind_dir_sc1','wind_spd1','date2','astro_mr2','astro_ms2','astro_sr2','astro_ss2','code_d2','code_n2','txt_d2','txt_n2','hum2','pcpn2','pop2','pres2','tmp_max2','tmp_min2','uv2','vis2','wind_deg2','wind_dir_sc2','wind_spd2']
        
        #init
        for i in range(0, len(observe_key_list)):
            weather_data[observe_key_list[i]] = "未知"
        for i in range(0, len(forecast_key_list)):
            forecast3d_dict[forecast_key_list[i]] = "未知"

        try:
            if selected:
                url = WEATHER_HB_URL % (cityid)
                url_aqi = WEATHER_HB_AQI_URL % (cityid)
            else:
                url = WEATHER_UK_URL % (cityid)
                url_aqi = WEATHER_UK_AQI_URL % (cityid)

            json_string = read_json_from_url(url)
            parsed_json = json.loads(json_string)

            json_aqi_string = read_json_from_url(url_aqi)
            parsed_aqi_json = json.loads(json_aqi_string)

            # 2018 和风天气api s6版本
            tmp_list = parsed_json['HeWeather6'][0]
            if tmp_list:
                if tmp_list['status'] == "ok":
                    forecast3d_dict['cityid'] = cityid#城市ID

                    if tmp_list.has_key('basic'):
                        basic_dict = tmp_list['basic']
                        if (isinstance(basic_dict, dict)):
                            forecast3d_dict['city'] = basic_dict.get('location', "未知")#城市名称
                            weather_data['city'] = forecast3d_dict['city']#城市名称
                            forecast3d_dict['prov'] = basic_dict.get('admin_area', "未知")#forecast3d_dict['prov'] = tmp_list['prov'] if 'prov' in tmp_list else "未知"
                            forecast3d_dict['cnty'] = basic_dict.get('cnty', "未知")#国家

                    if tmp_list.has_key('update'):
                        time_dict = tmp_list['update']
                        if (isinstance(time_dict, dict)):
                            forecast3d_dict['update_time'] = time_dict.get('loc', "未知")#更新时间
                            weather_data['time'] = forecast3d_dict['update_time']#实况更新时间
                            weather_data['ptime'] = forecast3d_dict['update_time']#更新时间

                    if tmp_list.has_key('daily_forecast'):
                        forecast_len = len(tmp_list['daily_forecast'])#3 days forecast
                        if forecast_len > 0:
                            i = 0;
                            daily_forecast = tmp_list.get('daily_forecast', "")
                            if daily_forecast not in (False, None, {}, '', "", '[]', "['']"):
                                for data in daily_forecast:#//3天天气预报
                                    if (i == 0):#第一天
                                        if (isinstance(data, dict)):
                                            forecast3d_dict['date0'] = data.get('date', "未知")#预报日期
                                            forecast3d_dict['astro_mr0'] = data.get('mr', "未知")#月升时间
                                            forecast3d_dict['astro_ms0'] = data.get('ms', "未知")#月落时间
                                            forecast3d_dict['astro_sr0'] = data.get('sr', "未知")#日出时间
                                            forecast3d_dict['astro_ss0'] = data.get('ss', "未知")#日落时间

                                            forecast3d_dict['code_d0'] = data.get('cond_code_d', "未知")#白天天气状况代码
                                            forecast3d_dict['code_n0'] = data.get('cond_code_n', "未知")#夜间天气状况代码
                                            forecast3d_dict['txt_d0'] = data.get('cond_txt_d', "未知")#白天天气状况描述
                                            forecast3d_dict['txt_n0'] = data.get('cond_txt_n', "未知")#夜间天气状况描述

                                            forecast3d_dict['hum0'] = data.get('hum', "未知")#相对湿度（%）
                                            forecast3d_dict['pcpn0'] = data.get('pcpn', "未知")#降水量（mm）
                                            forecast3d_dict['pop0'] = data.get('pop', "未知")#降水概率
                                            forecast3d_dict['pres0'] = data.get('pres', "未知")#气压
                                            forecast3d_dict['uv0'] = data.get('uv_index', "未知")#紫外线指数
                                            forecast3d_dict['vis0'] = data.get('vis', "未知")#能见度（km）

                                            forecast3d_dict['tmp_max0'] = data.get('tmp_max', "未知")#最高温度
                                            forecast3d_dict['tmp_min0'] = data.get('tmp_min', "未知")#最低温度
                                            if forecast3d_dict['tmp_min0'] != "未知":
                                                weather_data['temp1'] = forecast3d_dict['tmp_min0']+'℃'#实时天气里的最低温度
                                            else:
                                                weather_data['temp1'] = forecast3d_dict['tmp_min0']#实时天气里的最低温度
                                            if forecast3d_dict['tmp_max0'] != "未知":
                                                weather_data['temp2'] = forecast3d_dict['tmp_max0']+'℃'#实时天气里的最高温度
                                            else:
                                                weather_data['temp2'] = forecast3d_dict['tmp_max0']#实时天气里的最高温度

                                            forecast3d_dict['wind_deg0'] = data.get('wind_deg', "未知")#风向（360度）
                                            forecast3d_dict['wind_spd0'] = data.get('wind_spd', "未知")#风速（kmph）
                                            dir = data.get('wind_dir', "")
                                            sc = data.get('wind_sc', "")
                                            if dir not in (False, None, '', "") and sc not in (False, None, '', ""):
                                                forecast3d_dict['wind_dir_sc0'] = dir + " " + sc#风向风力等级
                                            elif dir not in (False, None, '', "") and sc in (False, None, '', ""):
                                                forecast3d_dict['wind_dir_sc0'] = dir#风向风力等级
                                            elif dir in (False, None, '', "") and sc not in (False, None, '', ""):
                                                forecast3d_dict['wind_dir_sc0'] = sc#风向风力等级
                                    elif (i == 1):
                                        if (isinstance(data, dict)):
                                            forecast3d_dict['date1'] = data.get('date', "未知")#预报日期

                                            forecast3d_dict['astro_mr1'] = data.get('mr', "未知")#月升时间
                                            forecast3d_dict['astro_ms1'] = data.get('ms', "未知")#月落时间
                                            forecast3d_dict['astro_sr1'] = data.get('sr', "未知")#日出时间
                                            forecast3d_dict['astro_ss1'] = data.get('ss', "未知")#日落时间

                                            forecast3d_dict['code_d1'] = data.get('cond_code_d', "未知")#白天天气状况代码
                                            forecast3d_dict['code_n1'] = data.get('cond_code_n', "未知")#夜间天气状况代码
                                            forecast3d_dict['txt_d1'] = data.get('cond_txt_d', "未知")#白天天气状况描述
                                            forecast3d_dict['txt_n1'] = data.get('cond_txt_n', "未知")#夜间天气状况描述

                                            forecast3d_dict['hum1'] = data.get('hum', "未知")#相对湿度（%）
                                            forecast3d_dict['pcpn1'] = data.get('pcpn', "未知")#降水量（mm）
                                            forecast3d_dict['pop1'] = data.get('pop', "未知")#降水概率
                                            forecast3d_dict['pres1'] = data.get('pres', "未知")#气压
                                            forecast3d_dict['uv1'] = data.get('uv_index', "未知")#紫外线指数
                                            forecast3d_dict['vis1'] = data.get('vis', "未知")#能见度（km）

                                            forecast3d_dict['tmp_max1'] = data.get('tmp_max', "未知")#最高温度
                                            forecast3d_dict['tmp_min1'] = data.get('tmp_min', "未知")#最低温度

                                            forecast3d_dict['wind_deg1'] = data.get('wind_deg', "未知")#风向（360度）
                                            forecast3d_dict['wind_spd1'] = data.get('wind_spd', "未知")#风速（kmph）
                                            dir = data.get('wind_dir', "")
                                            sc = data.get('wind_sc', "")
                                            if dir not in (False, None, '', "") and sc not in (False, None, '', ""):
                                                forecast3d_dict['wind_dir_sc1'] = dir + " " + sc#风向风力等级
                                            elif dir not in (False, None, '', "") and sc in (False, None, '', ""):
                                                forecast3d_dict['wind_dir_sc1'] = dir#风向风力等级
                                            elif dir in (False, None, '', "") and sc not in (False, None, '', ""):
                                                forecast3d_dict['wind_dir_sc1'] = sc#风向风力等级
                                    elif (i == 2):
                                        if (isinstance(data, dict)):
                                            forecast3d_dict['date2'] = data.get('date', "未知")#预报日期

                                            forecast3d_dict['astro_mr2'] = data.get('mr', "未知")#月升时间
                                            forecast3d_dict['astro_ms2'] = data.get('ms', "未知")#月落时间
                                            forecast3d_dict['astro_sr2'] = data.get('sr', "未知")#日出时间
                                            forecast3d_dict['astro_ss2'] = data.get('ss', "未知")#日落时间

                                            forecast3d_dict['code_d2'] = data.get('cond_code_d', "未知")#白天天气状况代码
                                            forecast3d_dict['code_n2'] = data.get('cond_code_n', "未知")#夜间天气状况代码
                                            forecast3d_dict['txt_d2'] = data.get('cond_txt_d', "未知")#白天天气状况描述
                                            forecast3d_dict['txt_n2'] = data.get('cond_txt_n', "未知")#夜间天气状况描述

                                            forecast3d_dict['hum2'] = data.get('hum', "未知")#相对湿度（%）
                                            forecast3d_dict['pcpn2'] = data.get('pcpn', "未知")#降水量（mm）
                                            forecast3d_dict['pop2'] = data.get('pop', "未知")#降水概率
                                            forecast3d_dict['pres2'] = data.get('pres', "未知")#气压
                                            forecast3d_dict['uv2'] = data.get('uv_index', "未知")#紫外线指数
                                            forecast3d_dict['vis2'] = data.get('vis', "未知")#能见度（km）

                                            forecast3d_dict['tmp_max2'] = data.get('tmp_max', "未知")#最高温度
                                            forecast3d_dict['tmp_min2'] = data.get('tmp_min', "未知")#最低温度

                                            forecast3d_dict['wind_deg2'] = data.get('wind_deg', "未知")#风向（360度）
                                            forecast3d_dict['wind_spd2'] = data.get('wind_spd', "未知")#风速（kmph）
                                            dir = data.get('wind_dir', "")
                                            sc = data.get('wind_sc', "")
                                            if dir not in (False, None, '', "") and sc not in (False, None, '', ""):
                                                forecast3d_dict['wind_dir_sc2'] = dir + " " + sc#风向风力等级
                                            elif dir not in (False, None, '', "") and sc in (False, None, '', ""):
                                                forecast3d_dict['wind_dir_sc2'] = dir#风向风力等级
                                            elif dir in (False, None, '', "") and sc not in (False, None, '', ""):
                                                forecast3d_dict['wind_dir_sc2'] = sc#风向风力等级
                                    i = i+1

                    if tmp_list.has_key('lifestyle'):
                        suggestion_dict = tmp_list['lifestyle']
                        for i in range(len(suggestion_dict)):
                            sub_dict = suggestion_dict[i]
                            if (isinstance(sub_dict, dict)):
                                if sub_dict.get('type', "") == "comf":
                                    forecast3d_dict['comf_brf'] = sub_dict.get('brf', "未知")#舒适度指数  简介
                                    forecast3d_dict['comf_txt'] = sub_dict.get('txt', "未知")#舒适度指数  详细描述
                                elif sub_dict.get('type', "") == "cw":
                                    forecast3d_dict['cw_brf'] = sub_dict.get('brf', "未知")#洗车指数  简介
                                    forecast3d_dict['cw_txt'] = sub_dict.get('txt', "未知")#洗车指数  详细描述
                                elif sub_dict.get('type', "") == "drsg":
                                    forecast3d_dict['drsg_brf'] = sub_dict.get('brf', "未知")#穿衣指数  简介
                                    forecast3d_dict['drsg_txt'] = sub_dict.get('txt', "未知")#穿衣指数  详细描述
                                elif sub_dict.get('type', "") == "flu":
                                    forecast3d_dict['flu_brf'] = sub_dict.get('brf', "未知")#感冒指数  简介
                                    forecast3d_dict['flu_txt'] = sub_dict.get('txt', "未知")#感冒指数  详细描述
                                elif sub_dict.get('type', "") == "sport":
                                    forecast3d_dict['sport_brf'] = sub_dict.get('brf', "未知")#运动指数  简介
                                    forecast3d_dict['sport_txt'] = sub_dict.get('txt', "未知")#运动指数  详细描述
                                elif sub_dict.get('type', "") == "trav":
                                    forecast3d_dict['trav_brf'] = sub_dict.get('brf', "未知")#旅游指数  简介
                                    forecast3d_dict['trav_txt'] = sub_dict.get('txt', "未知")#旅游指数  详细描述
                                elif sub_dict.get('type', "") == "uv":
                                    forecast3d_dict['uv_brf'] = sub_dict.get('brf', "未知")#紫外线指数  简介
                                    forecast3d_dict['uv_txt'] = sub_dict.get('txt', "未知")#紫外线指数  详细描述

                    if tmp_list.has_key('now'):
                        now_dict = tmp_list['now']
                        if (isinstance(now_dict, dict)):
                            weather_data['temp'] = now_dict.get('tmp', "未知")#温度
                            weather_data['SD'] = now_dict.get('hum', "未知")#相对湿度（%）
                            weather_data['WD'] = now_dict.get('wind_dir', "未知")#风向
                            weather_data['WS'] = now_dict.get('wind_sc', "未知")#风力等级
                            weather_data['weather'] = now_dict.get('cond_txt', "未知")#天气
                            weather_data['img1'] = weather_icons[now_dict.get('cond_code', "100")]#天气状况代码
                            weather_data['img2'] = weather_data['img1']

            weather_data['aqi'] = '未知'
            tmp_aqi_list = parsed_aqi_json['HeWeather6'][0]
            if tmp_aqi_list:
                if tmp_aqi_list['status'] == "ok":
                    if tmp_aqi_list.has_key('air_now_city'):
                        aqi_dict = tmp_aqi_list['air_now_city']
                        if (isinstance(aqi_dict, dict)):
                                qlty = aqi_dict.get('qlty', "")
                                aqi = aqi_dict.get('aqi', "")
                                if qlty not in (False, None, '', "") and aqi not in (False, None, '', ""):
                                    weather_data['aqi'] = qlty + '(' + aqi + ')'
                                elif qlty not in (False, None, '', "") and aqi in (False, None, '', ""):
                                    weather_data['aqi'] = qlty
                                elif qlty in (False, None, '', "") and aqi not in (False, None, '', ""):
                                    weather_data['aqi'] = aqi

#            print "weather_data="
#            print weather_data#{'city': u'\u957f\u6c99', 'WD': u'\u897f\u5317\u98ce', 'ptime': u'2017-05-04 13:54', 'temp': u'23', 'temp2': u'26\u2103', 'temp1': u'16\u2103', 'weather': u'\u591a\u4e91', 'WS': u'4-5', 'time': u'2017-05-04 13:54', 'img2': 'd1.gif', 'img1': 'd1.gif', 'aqi': u'\u4f18(39)', 'SD': u'53'}
#            print "forecast3d_dict="
#            print forecast3d_dict#{'f0': u'2017-05-04 15:53', 'fc0': u'16', 'fc2': u'18', 'weather1': u'\u663c:\u591a\u4e91  \u591c:\u591a\u4e91', 'weather2': u'\u663c:\u591a\u4e91  \u591c:\u591a\u4e91', 'fc1': u'18', 'fa2': u'101', 'fa0': u'101', 'fa1': u'101', 'fg0': u'3-4', 'fg1': u'\u5fae\u98ce', 'fg2': u'\u5fae\u98ce', 'weather3': u'\u663c:\u591a\u4e91  \u591c:\u591a\u4e91', 'fd1': u'27', 'fd0': u'26', 'fd2': u'22', 'c13': u'28.19409', 'fh1': u'\u5fae\u98ce', 'fh0': u'3-4', 'c14': u'112.982279', 'fb2': u'101', 'fb1': u'101', 'fb0': u'101', 'ff2': u'\u5317\u98ce', 'ff1': u'\u5317\u98ce', 'ff0': u'\u897f\u5317\u98ce', 'c3': u'\u957f\u6c99', 'fe2': u'\u5317\u98ce', 'fe0': u'\u897f\u5317\u98ce', 'fe1': u'\u5317\u98ce', 'fh2': u'\u5fae\u98ce'}
            return (True, weather_data, forecast3d_dict)

# 2018 和风天气api v5版本
#            tmp_list = parsed_json['HeWeather5'][0]
#            if tmp_list:
#                if tmp_list['status'] == "ok":
#                    forecast3d_dict['cityid'] = cityid#城市ID

#                    if tmp_list.has_key('basic'):
#                        basic_dict = tmp_list['basic']
#                        if (isinstance(basic_dict, dict)):
#                            forecast3d_dict['city'] = basic_dict.get('city', "未知")#城市名称
#                            weather_data['city'] = forecast3d_dict['city']#城市名称
#                            forecast3d_dict['prov'] = basic_dict.get('prov', "未知")#forecast3d_dict['prov'] = tmp_list['prov'] if 'prov' in tmp_list else "未知"
#                            forecast3d_dict['cnty'] = basic_dict.get('cnty', "未知")#国家
#                            if basic_dict.has_key('update'):
#                                time_dict = basic_dict['update']
#                                if (isinstance(time_dict, dict)):
#                                    forecast3d_dict['update_time'] = time_dict.get('loc', "未知")#更新时间
#                                    weather_data['time'] = forecast3d_dict['update_time']#实况更新时间
#                                    weather_data['ptime'] = forecast3d_dict['update_time']#更新时间

#                    if tmp_list.has_key('daily_forecast'):
#                        forecast_len = len(tmp_list['daily_forecast'])#3 days forecast
#                        if forecast_len > 0:
#                            i = 0;
#                            daily_forecast = tmp_list.get('daily_forecast', "")
#                            if daily_forecast not in (False, None, {}, '', "", '[]', "['']"):
#                                for data in daily_forecast:#//3天天气预报
#                                    if (i == 0):#第一天
#                                        if (isinstance(data, dict)):
#                                            forecast3d_dict['date0'] = data.get('date', "未知")#预报日期
#                                            if data.has_key('astro'):
#                                                astro_dict = data['astro']
#                                                forecast3d_dict['astro_mr0'] = astro_dict.get('mr', "未知")#月升时间
#                                                forecast3d_dict['astro_ms0'] = astro_dict.get('ms', "未知")#月落时间
#                                                forecast3d_dict['astro_sr0'] = astro_dict.get('sr', "未知")#日出时间
#                                                forecast3d_dict['astro_ss0'] = astro_dict.get('ss', "未知")#日落时间
#                                            if data.has_key('cond'):
#                                                cond_dict = data['cond']
#                                                forecast3d_dict['code_d0'] = cond_dict.get('code_d', "未知")#白天天气状况代码
#                                                forecast3d_dict['code_n0'] = cond_dict.get('code_n', "未知")#夜间天气状况代码
#                                                forecast3d_dict['txt_d0'] = cond_dict.get('txt_d', "未知")#白天天气状况描述
#                                                forecast3d_dict['txt_n0'] = cond_dict.get('txt_n', "未知")#夜间天气状况描述
#                                            forecast3d_dict['hum0'] = data.get('hum', "未知")#相对湿度（%）
#                                            forecast3d_dict['pcpn0'] = data.get('pcpn', "未知")#降水量（mm）
#                                            forecast3d_dict['pop0'] = data.get('pop', "未知")#降水概率
#                                            forecast3d_dict['pres0'] = data.get('pres', "未知")#气压
#                                            forecast3d_dict['uv0'] = data.get('uv', "未知")#紫外线指数
#                                            forecast3d_dict['vis0'] = data.get('vis', "未知")#能见度（km）
#                                            if data.has_key('tmp'):
#                                                tmp_dict = data['tmp']
#                                                forecast3d_dict['tmp_max0'] = tmp_dict.get('max', "未知")#最高温度
#                                                forecast3d_dict['tmp_min0'] = tmp_dict.get('min', "未知")#最低温度
#                                                if forecast3d_dict['tmp_min0'] != "未知":
#                                                    weather_data['temp1'] = forecast3d_dict['tmp_min0']+'℃'#实时天气里的最低温度
#                                                else:
#                                                    weather_data['temp1'] = forecast3d_dict['tmp_min0']#实时天气里的最低温度
#                                                if forecast3d_dict['tmp_max0'] != "未知":
#                                                    weather_data['temp2'] = forecast3d_dict['tmp_max0']+'℃'#实时天气里的最高温度
#                                                else:
#                                                    weather_data['temp2'] = forecast3d_dict['tmp_max0']#实时天气里的最高温度
#                                            if data.has_key('wind'):
#                                                wind_dict = data['wind']
#                                                forecast3d_dict['wind_deg0'] = wind_dict.get('deg', "未知")#风向（360度）
#                                                forecast3d_dict['wind_spd0'] = wind_dict.get('spd', "未知")#风速（kmph）
#                                                dir = wind_dict.get('dir', "")
#                                                sc = wind_dict.get('sc', "")
#                                                if dir not in (False, None, '', "") and sc not in (False, None, '', ""):
#                                                    forecast3d_dict['wind_dir_sc0'] = dir + " " + sc#风向风力等级
#                                                elif dir not in (False, None, '', "") and sc in (False, None, '', ""):
#                                                    forecast3d_dict['wind_dir_sc0'] = dir#风向风力等级
#                                                elif dir in (False, None, '', "") and sc not in (False, None, '', ""):
#                                                    forecast3d_dict['wind_dir_sc0'] = sc#风向风力等级
#        #                                forecast3d_dict['weather1'] = "昼:" + data['cond']['txt_d'] + "  夜:" + data['cond']['txt_n']#天气描述：如多云
#                                    elif (i == 1):
#                                        if (isinstance(data, dict)):
#                                            forecast3d_dict['date1'] = data.get('date', "未知")#预报日期
#                                            if data.has_key('astro'):
#                                                astro_dict = data['astro']
#                                                forecast3d_dict['astro_mr1'] = astro_dict.get('mr', "未知")#月升时间
#                                                forecast3d_dict['astro_ms1'] = astro_dict.get('ms', "未知")#月落时间
#                                                forecast3d_dict['astro_sr1'] = astro_dict.get('sr', "未知")#日出时间
#                                                forecast3d_dict['astro_ss1'] = astro_dict.get('ss', "未知")#日落时间
#                                            if data.has_key('cond'):
#                                                cond_dict = data['cond']
#                                                forecast3d_dict['code_d1'] = cond_dict.get('code_d', "未知")#白天天气状况代码
#                                                forecast3d_dict['code_n1'] = cond_dict.get('code_n', "未知")#夜间天气状况代码
#                                                forecast3d_dict['txt_d1'] = cond_dict.get('txt_d', "未知")#白天天气状况描述
#                                                forecast3d_dict['txt_n1'] = cond_dict.get('txt_n', "未知")#夜间天气状况描述
#                                            forecast3d_dict['hum1'] = data.get('hum', "未知")#相对湿度（%）
#                                            forecast3d_dict['pcpn1'] = data.get('pcpn', "未知")#降水量（mm）
#                                            forecast3d_dict['pop1'] = data.get('pop', "未知")#降水概率
#                                            forecast3d_dict['pres1'] = data.get('pres', "未知")#气压
#                                            forecast3d_dict['uv1'] = data.get('uv', "未知")#紫外线指数
#                                            forecast3d_dict['vis1'] = data.get('vis', "未知")#能见度（km）
#                                            if data.has_key('tmp'):
#                                                tmp_dict = data['tmp']
#                                                forecast3d_dict['tmp_max1'] = tmp_dict.get('max', "未知")#最高温度
#                                                forecast3d_dict['tmp_min1'] = tmp_dict.get('min', "未知")#最低温度
#                                            if data.has_key('wind'):
#                                                wind_dict = data['wind']
#                                                forecast3d_dict['wind_deg1'] = wind_dict.get('deg', "未知")#风向（360度）
#                                                forecast3d_dict['wind_spd1'] = wind_dict.get('spd', "未知")#风速（kmph）
#                                                dir = wind_dict.get('dir', "")
#                                                sc = wind_dict.get('sc', "")
#                                                if dir not in (False, None, '', "") and sc not in (False, None, '', ""):
#                                                    forecast3d_dict['wind_dir_sc1'] = dir + " " + sc#风向风力等级
#                                                elif dir not in (False, None, '', "") and sc in (False, None, '', ""):
#                                                    forecast3d_dict['wind_dir_sc1'] = dir#风向风力等级
#                                                elif dir in (False, None, '', "") and sc not in (False, None, '', ""):
#                                                    forecast3d_dict['wind_dir_sc1'] = sc#风向风力等级
#                                    elif (i == 2):
#                                        if (isinstance(data, dict)):
#                                            forecast3d_dict['date2'] = data.get('date', "未知")#预报日期
#                                            if data.has_key('astro'):
#                                                astro_dict = data['astro']
#                                                forecast3d_dict['astro_mr2'] = astro_dict.get('mr', "未知")#月升时间
#                                                forecast3d_dict['astro_ms2'] = astro_dict.get('ms', "未知")#月落时间
#                                                forecast3d_dict['astro_sr2'] = astro_dict.get('sr', "未知")#日出时间
#                                                forecast3d_dict['astro_ss2'] = astro_dict.get('ss', "未知")#日落时间
#                                            if data.has_key('cond'):
#                                                cond_dict = data['cond']
#                                                forecast3d_dict['code_d2'] = cond_dict.get('code_d', "未知")#白天天气状况代码
#                                                forecast3d_dict['code_n2'] = cond_dict.get('code_n', "未知")#夜间天气状况代码
#                                                forecast3d_dict['txt_d2'] = cond_dict.get('txt_d', "未知")#白天天气状况描述
#                                                forecast3d_dict['txt_n2'] = cond_dict.get('txt_n', "未知")#夜间天气状况描述
#                                            forecast3d_dict['hum2'] = data.get('hum', "未知")#相对湿度（%）
#                                            forecast3d_dict['pcpn2'] = data.get('pcpn', "未知")#降水量（mm）
#                                            forecast3d_dict['pop2'] = data.get('pop', "未知")#降水概率
#                                            forecast3d_dict['pres2'] = data.get('pres', "未知")#气压
#                                            forecast3d_dict['uv2'] = data.get('uv', "未知")#紫外线指数
#                                            forecast3d_dict['vis2'] = data.get('vis', "未知")#能见度（km）
#                                            if data.has_key('tmp'):
#                                                tmp_dict = data['tmp']
#                                                forecast3d_dict['tmp_max2'] = tmp_dict.get('max', "未知")#最高温度
#                                                forecast3d_dict['tmp_min2'] = tmp_dict.get('min', "未知")#最低温度
#                                            if data.has_key('wind'):
#                                                wind_dict = data['wind']
#                                                forecast3d_dict['wind_deg2'] = wind_dict.get('deg', "未知")#风向（360度）
#                                                forecast3d_dict['wind_spd2'] = wind_dict.get('spd', "未知")#风速（kmph）
#                                                dir = wind_dict.get('dir', "")
#                                                sc = wind_dict.get('sc', "")
#                                                if dir not in (False, None, '', "") and sc not in (False, None, '', ""):
#                                                    forecast3d_dict['wind_dir_sc2'] = dir + " " + sc#风向风力等级
#                                                elif dir not in (False, None, '', "") and sc in (False, None, '', ""):
#                                                    forecast3d_dict['wind_dir_sc2'] = dir#风向风力等级
#                                                elif dir in (False, None, '', "") and sc not in (False, None, '', ""):
#                                                    forecast3d_dict['wind_dir_sc2'] = sc#风向风力等级
#                                    i = i+1

#                    if tmp_list.has_key('suggestion'):
#                        suggestion_dict = tmp_list['suggestion']
#                        if (isinstance(suggestion_dict, dict)):
#                            if suggestion_dict.has_key('comf'):
#                                comf_dict = suggestion_dict['comf']
#                                if (isinstance(comf_dict, dict)):
#                                    forecast3d_dict['comf_brf'] = comf_dict.get('brf', "未知")#舒适度指数  简介
#                                    forecast3d_dict['comf_txt'] = comf_dict.get('txt', "未知")#舒适度指数  详细描述
#                            if suggestion_dict.has_key('cw'):
#                                cw_dict = suggestion_dict['cw']
#                                if (isinstance(cw_dict, dict)):
#                                    forecast3d_dict['cw_brf'] = cw_dict.get('brf', "未知")#洗车指数  简介
#                                    forecast3d_dict['cw_txt'] = cw_dict.get('txt', "未知")#洗车指数  详细描述
#                            if suggestion_dict.has_key('drsg'):
#                                drsg_dict = suggestion_dict['drsg']
#                                if (isinstance(drsg_dict, dict)):
#                                    forecast3d_dict['drsg_brf'] = drsg_dict.get('brf', "未知")#穿衣指数  简介
#                                    forecast3d_dict['drsg_txt'] = drsg_dict.get('txt', "未知")#穿衣指数  详细描述
#                            if suggestion_dict.has_key('flu'):
#                                flu_dict = suggestion_dict['flu']
#                                if (isinstance(flu_dict, dict)):
#                                    forecast3d_dict['flu_brf'] = flu_dict.get('brf', "未知")#感冒指数  简介
#                                    forecast3d_dict['flu_txt'] = flu_dict.get('txt', "未知")#感冒指数  详细描述
#                            if suggestion_dict.has_key('sport'):
#                                sport_dict = suggestion_dict['sport']
#                                if (isinstance(sport_dict, dict)):
#                                    forecast3d_dict['sport_brf'] = sport_dict.get('brf', "未知")#运动指数  简介
#                                    forecast3d_dict['sport_txt'] = sport_dict.get('txt', "未知")#运动指数  详细描述
#                            if suggestion_dict.has_key('trav'):
#                                trav_dict = suggestion_dict['trav']
#                                if (isinstance(trav_dict, dict)):
#                                    forecast3d_dict['trav_brf'] = trav_dict.get('brf', "未知")#旅游指数  简介
#                                    forecast3d_dict['trav_txt'] = trav_dict.get('txt', "未知")#旅游指数  详细描述
#                            if suggestion_dict.has_key('uv'):
#                                uv_dict = suggestion_dict['uv']
#                                if (isinstance(uv_dict, dict)):
#                                    forecast3d_dict['uv_brf'] = uv_dict.get('brf', "未知")#紫外线指数  简介
#                                    forecast3d_dict['uv_txt'] = uv_dict.get('txt', "未知")#紫外线指数  详细描述

#                    if tmp_list.has_key('now'):
#                        now_dict = tmp_list['now']
#                        if (isinstance(now_dict, dict)):
#                            weather_data['temp'] = now_dict.get('tmp', "未知")#温度
#                            weather_data['SD'] = now_dict.get('hum', "未知")#相对湿度（%）
#                            if now_dict.has_key('wind'):
#                                wind_dict = now_dict['wind']
#                                if (isinstance(wind_dict, dict)):
#                                    weather_data['WD'] = wind_dict.get('dir', "未知")#风向
#                                    weather_data['WS'] = wind_dict.get('sc', "未知")#风力等级
#                            if now_dict.has_key('cond'):
#                                cond_dict = now_dict['cond']
#                                if (isinstance(cond_dict, dict)):
#                                    weather_data['weather'] = cond_dict.get('txt', "未知")#天气
#                                    weather_data['img1'] = weather_icons[cond_dict.get('code', "100")]#天气状况代码
#                                    weather_data['img2'] = weather_data['img1']

#                    if tmp_list.has_key('aqi'):
#                        aqi_dict = tmp_list['aqi']
#                        if (isinstance(aqi_dict, dict)):
#                            if aqi_dict.has_key('city'):
#                                city_dict = aqi_dict['city']
#                                if (isinstance(city_dict, dict)):
#                                    qlty = city_dict.get('qlty', "")
#                                    aqi = city_dict.get('aqi', "")
#                                    if qlty not in (False, None, '', "") and aqi not in (False, None, '', ""):
#                                        weather_data['aqi'] = qlty + '(' + aqi + ')'
#                                    elif qlty not in (False, None, '', "") and aqi in (False, None, '', ""):
#                                        weather_data['aqi'] = qlty
#                                    elif qlty in (False, None, '', "") and aqi not in (False, None, '', ""):
#                                        weather_data['aqi'] = aqi
#                    else:
#                        weather_data['aqi'] = '未知'
#                    #print "weather_data="
#                    #print weather_data#{'city': u'\u957f\u6c99', 'WD': u'\u897f\u5317\u98ce', 'ptime': u'2017-05-04 13:54', 'temp': u'23', 'temp2': u'26\u2103', 'temp1': u'16\u2103', 'weather': u'\u591a\u4e91', 'WS': u'4-5', 'time': u'2017-05-04 13:54', 'img2': 'd1.gif', 'img1': 'd1.gif', 'aqi': u'\u4f18(39)', 'SD': u'53'}
#                    #print "forecast3d_dict="
#                    #print forecast3d_dict#{'f0': u'2017-05-04 15:53', 'fc0': u'16', 'fc2': u'18', 'weather1': u'\u663c:\u591a\u4e91  \u591c:\u591a\u4e91', 'weather2': u'\u663c:\u591a\u4e91  \u591c:\u591a\u4e91', 'fc1': u'18', 'fa2': u'101', 'fa0': u'101', 'fa1': u'101', 'fg0': u'3-4', 'fg1': u'\u5fae\u98ce', 'fg2': u'\u5fae\u98ce', 'weather3': u'\u663c:\u591a\u4e91  \u591c:\u591a\u4e91', 'fd1': u'27', 'fd0': u'26', 'fd2': u'22', 'c13': u'28.19409', 'fh1': u'\u5fae\u98ce', 'fh0': u'3-4', 'c14': u'112.982279', 'fb2': u'101', 'fb1': u'101', 'fb0': u'101', 'ff2': u'\u5317\u98ce', 'ff1': u'\u5317\u98ce', 'ff0': u'\u897f\u5317\u98ce', 'c3': u'\u957f\u6c99', 'fe2': u'\u5317\u98ce', 'fe0': u'\u897f\u5317\u98ce', 'fe1': u'\u5317\u98ce', 'fh2': u'\u5fae\u98ce'}
#                    return (True, weather_data, forecast3d_dict)
        except Exception as e:
#            print e
            return (False, weather_data, forecast3d_dict)
        return (False, weather_data, forecast3d_dict)

    def insert_or_update_heweather_forecast(self, dict_data, now_date, insertflag):
        if insertflag:
            self.db.insert_heweather_forecast_data(dict_data, now_date)
        else:
            self.db.update_heweather_forecast_data(dict_data, now_date)
    #        if 'c16' not in dict_data.keys():
    #            dict_data['c16'] = '未知'

    def insert_or_update_observe(self, cityid, dict_data, now_date, insertflag):
        if insertflag:
            self.db.insert_observe_data(cityid,dict_data['city'],dict_data['ptime'],dict_data['time'],now_date,dict_data['WD'],dict_data['WS'],dict_data['SD'],dict_data['weather'],dict_data['img1'],dict_data['img2'],dict_data['temp'],dict_data['temp1'],dict_data['temp2'],dict_data['aqi'])
        else:
            self.db.update_observe_data(dict_data['ptime'],dict_data['time'],now_date,dict_data['WD'],dict_data['WS'],dict_data['SD'],dict_data['weather'],dict_data['img1'],dict_data['img2'],dict_data['temp'],dict_data['temp1'],dict_data['temp2'],dict_data['aqi'],cityid)

    def get_heweather_observe_weather(self, cityid):
        '''
        如果没有数据，则直接获取后插入数据库中
        如果有数据，则比较时间，如果日期不同，则重新获取后更新数据库；如果日期相同，小时不同，则重写获取后更新数据库；否则使用数据库中数据
        '''
#        selected = 0
        again = False
        observe_dict = {}
        forecast3d_dict = {}
        observe_key_list = ['city', 'ptime', 'time', 'WD', 'WS', 'SD', 'weather', 'img1', 'img2', 'temp', 'temp1', 'temp2', 'aqi']
        now_date = get_local_format_time()
        observe_db_record = self.db.search_observe_record(cityid)
        forecast_db_record = self.db.search_heweather_forecast_record(cityid)
        if observe_db_record != []:
            db_time_list = self.db.search_observe_record_update_time(cityid)
            db_time = None
            db_time = db_time_list[0][0]
            if db_time is not None and db_time != "未知":# db_time = '2014-05-07 13:51:30'
                db_time_list = db_time.split(" ")
                now_date_list = now_date.split(" ")
                # compare now_time with db_time ,when they are different, then access weather data again
                if db_time_list[0] != now_date_list[0]:#different day
                    again = True
#                    selected = 0
                else:# same day
                    again = False#20170626
                    dbTime = int(db_time_list[1].split(":")[0])#16
                    nowTime = int(now_date_list[1].split(":")[0])#19
                    time_space = nowTime - dbTime
                    if dbTime < 8:
                        if nowTime >=8 and nowTime < 16:
                            again = True
#                            selected = 1
                        elif nowTime >=16:
                            again = True
#                            selected = 2
                    if dbTime >=8 and dbTime < 16:
                        if nowTime >=16:
                            again = True
#                            selected = 2
    #                    print time_space
    #                if db_time_list[1].split(":")[0] == now_date_list[1].split(":")[0]:#same day and same hour
    #                    again = False
    #                else:#same day and different hour
    #                    again = True
                if again:
                    again = False
                    global roundVal#再次声明，表示在这里使用的是全局变量，而不是局部变量
                    #(ret, observe_dict, forecast3d_dict) = self.access_heweather_forecast_and_observe(cityid, selected)#update
                    (ret, observe_dict, forecast3d_dict) = self.access_heweather_forecast_and_observe(cityid, roundVal)#update
                    if roundVal:
                        roundVal = False
                    else:
                        roundVal = True
                    if ret:
                        if observe_dict not in (False, None, {}, '', '[]', "['']"):
                            self.insert_or_update_observe(cityid, observe_dict, now_date, False)#update
                        else:
                            if len(observe_db_record) >= 1:
                                for i in range(0, len(observe_db_record[0])):
                                    observe_dict[observe_key_list[i]] = observe_db_record[0][i]
                        if forecast_db_record != []:#update forecast
                            if forecast3d_dict not in (False, None, {}, '', '[]', "['']"):
                                self.insert_or_update_heweather_forecast(forecast3d_dict, now_date, False)
                        else:#insert forecast
                            if forecast3d_dict not in (False, None, {}, '', '[]', "['']"):
                                self.insert_or_update_heweather_forecast(forecast3d_dict, now_date, True)
                    else:
                        if len(observe_db_record) >= 1:
                            for i in range(0, len(observe_db_record[0])):
                                observe_dict[observe_key_list[i]] = observe_db_record[0][i]
                else:
                    if len(observe_db_record) >= 1:
                        for i in range(0, len(observe_db_record[0])):
                            observe_dict[observe_key_list[i]] = observe_db_record[0][i]
            else:#get new data, then update db
#                selected = 0
                global roundVal#再次声明，表示在这里使用的是全局变量，而不是局部变量
                #(ret, observe_dict, forecast3d_dict) = self.access_heweather_forecast_and_observe(cityid, selected)#update
                (ret, observe_dict, forecast3d_dict) = self.access_heweather_forecast_and_observe(cityid, roundVal)#update
                if roundVal:
                    roundVal = False
                else:
                    roundVal = True
                if ret:
                    if observe_dict not in (False, None, {}, '', '[]', "['']"):
                        self.insert_or_update_observe(cityid, observe_dict, now_date, False)#update
                    else:
                        if len(observe_db_record) >= 1:
                            for i in range(0, len(observe_db_record[0])):
                                observe_dict[observe_key_list[i]] = observe_db_record[0][i]
                    if forecast_db_record != []:#update forecast
                        if forecast3d_dict not in (False, None, {}, '', '[]', "['']"):
                            self.insert_or_update_heweather_forecast(forecast3d_dict, now_date, False)
                    else:#insert forecast
                        if forecast3d_dict not in (False, None, {}, '', '[]', "['']"):
                            self.insert_or_update_heweather_forecast(forecast3d_dict, now_date, True)
                else:
                    if len(observe_db_record) >= 1:
                        for i in range(0, len(observe_db_record[0])):
                            observe_dict[observe_key_list[i]] = observe_db_record[0][i]
        else:#observe_db_record == []
#            selected = 0
            global roundVal#再次声明，表示在这里使用的是全局变量，而不是局部变量
            #(ret, observe_dict, forecast3d_dict) = self.access_heweather_forecast_and_observe(cityid, selected)
            (ret, observe_dict, forecast3d_dict) = self.access_heweather_forecast_and_observe(cityid, roundVal)
            if roundVal:
                roundVal = False
            else:
                roundVal = True
            if ret:
                if observe_dict not in (False, None, {}, '', '[]', "['']"):
                    self.insert_or_update_observe(cityid, observe_dict, now_date, True)#insert
                if forecast_db_record != []:#update forecast
                    if forecast3d_dict not in (False, None, {}, '', '[]', "['']"):
                        self.insert_or_update_heweather_forecast(forecast3d_dict, now_date, False)
                else:#insert forecast
                    if forecast3d_dict not in (False, None, {}, '', '[]', "['']"):
                        self.insert_or_update_heweather_forecast(forecast3d_dict, now_date, True)
        return observe_dict

    # 2018 和风天气api s6版本： 天气预报界面显示时从server端获取数据
    def get_heweather_forecast_weather(self, cityid):
#        selected = 0
        again = False#20170626
        observe_dict = {}
        forecast3d_dict = {}
        forecast_key_list = ['city','prov','cnty','update_time','insert_time','date0','astro_mr0','astro_ms0','astro_sr0','astro_ss0','code_d0','code_n0','txt_d0','txt_n0','hum0','pcpn0','pop0','pres0','tmp_max0','tmp_min0','uv0','vis0','wind_deg0','wind_dir_sc0','wind_spd0','date1','astro_mr1','astro_ms1','astro_sr1','astro_ss1','code_d1','code_n1','txt_d1','txt_n1','hum1','pcpn1','pop1','pres1','tmp_max1','tmp_min1','uv1','vis1','wind_deg1','wind_dir_sc1','wind_spd1','date2','astro_mr2','astro_ms2','astro_sr2','astro_ss2','code_d2','code_n2','txt_d2','txt_n2','hum2','pcpn2','pop2','pres2','tmp_max2','tmp_min2','uv2','vis2','wind_deg2','wind_dir_sc2','wind_spd2','comf_brf','comf_txt','cw_brf','cw_txt','drsg_brf','drsg_txt','flu_brf','flu_txt','sport_brf','sport_txt','trav_brf','trav_txt','uv_brf','uv_txt']
        now_date = get_local_format_time()
        observe_db_record = self.db.search_observe_record(cityid)
        forecast_db_record = self.db.search_heweather_forecast_record(cityid)
        if forecast_db_record != []:
            db_time_list = self.db.search_heweather_forecast_record_update_time(cityid)
            db_time = None
            db_time = db_time_list[0][0]
            if db_time is not None and db_time != "未知":# db_time = '2014-05-07 13:51:30'
                db_time_list = db_time.split(" ")
                now_date_list = now_date.split(" ")
                # compare now_time with db_time ,when they are different, then access weather data again
                if db_time_list[0] != now_date_list[0]:#different day
                    again = True
#                    selected = 0
                else:# same day
                    again = False#20170626
                    dbTime = int(db_time_list[1].split(":")[0])#16
                    nowTime = int(now_date_list[1].split(":")[0])#19
    #                    time_space = nowTime - dbTime
    #            if db_time is not None:# db_time = '2014-05-07 13:51:30'
    #                dbTime = int(db_time.split()[1].split(":")[0])#16
    #                nowTime = int(now_date.split()[1].split(":")[0])#19
    #                time_space = nowTime - dbTime
                    if dbTime < 8:
                        if nowTime >=8 and nowTime < 16:
                            again = True
#                            selected = 1
                        elif nowTime >=16:
                            again = True
#                            selected = 2
                    if dbTime >=8 and dbTime < 16:
                        if nowTime >=16:
                            again = True
#                            selected = 2
        #                if db_time_list[1].split(":")[0] == now_date_list[1].split(":")[0]:#same day and same hour
        #                    again = False
        #                else:#same day and different hour
        #                    again = True
                if again:
                    again = False
                    global roundVal#再次声明，表示在这里使用的是全局变量，而不是局部变量
                    #(ret, observe_dict, forecast3d_dict) = self.access_heweather_forecast_and_observe(cityid, selected)#update
                    (ret, observe_dict, forecast3d_dict) = self.access_heweather_forecast_and_observe(cityid, roundVal)#update
                    if roundVal:
                        roundVal = False
                    else:
                        roundVal = True
                    if ret:
                        if forecast3d_dict not in (False, None, {}, '', '[]', "['']"):
                            self.insert_or_update_heweather_forecast(forecast3d_dict, now_date, False)#update
                        else:
                            if len(forecast_db_record) >= 1:
                                for i in range(0, len(forecast_db_record[0])):
                                    forecast3d_dict[forecast_key_list[i]] = forecast_db_record[0][i]
                        if observe_db_record != []:#update observe
                            if observe_dict not in (False, None, {}, '', '[]', "['']"):
                                self.insert_or_update_observe(cityid, observe_dict, now_date, False)#20170810
                        else:#insert observe
                            if observe_dict not in (False, None, {}, '', '[]', "['']"):
                                self.insert_or_update_observe(cityid, observe_dict, now_date, True)
                    else:
                        if len(forecast_db_record) >= 1:
                            for i in range(0, len(forecast_db_record[0])):
                                forecast3d_dict[forecast_key_list[i]] = forecast_db_record[0][i]
                else:
                    if len(forecast_db_record) >= 1:
                        for i in range(0, len(forecast_db_record[0])):
                            forecast3d_dict[forecast_key_list[i]] = forecast_db_record[0][i]
            else:#get new data, then update db
#                selected = 0
                global roundVal#再次声明，表示在这里使用的是全局变量，而不是局部变量
                #(ret, observe_dict, forecast3d_dict) = self.access_heweather_forecast_and_observe(cityid, selected)#update
                (ret, observe_dict, forecast3d_dict) = self.access_heweather_forecast_and_observe(cityid, roundVal)#update
                if roundVal:
                    roundVal = False
                else:
                    roundVal = True
                if ret:
                    if forecast3d_dict not in (False, None, {}, '', '[]', "['']"):
                        self.insert_or_update_heweather_forecast(forecast3d_dict, now_date, False)#update
                    else:
                        if len(forecast_db_record) >= 1:
                            for i in range(0, len(forecast_db_record[0])):
                                forecast3d_dict[forecast_key_list[i]] = forecast_db_record[0][i]
                    if observe_db_record != []:#update observe
                        if observe_dict not in (False, None, {}, '', '[]', "['']"):
                            self.insert_or_update_observe(cityid, observe_dict, now_date, False)#20170810
                    else:#insert observe
                        if observe_dict not in (False, None, {}, '', '[]', "['']"):
                            self.insert_or_update_observe(cityid, observe_dict, now_date, True)
                else:
                    if len(forecast_db_record) >= 1:
                        for i in range(0, len(forecast_db_record[0])):
                            forecast3d_dict[forecast_key_list[i]] = forecast_db_record[0][i]
        else:#forecast_db_record == []
#            selected = 0
            global roundVal#再次声明，表示在这里使用的是全局变量，而不是局部变量
            #(ret, observe_dict, forecast3d_dict) = self.access_heweather_forecast_and_observe(cityid, selected)
            (ret, observe_dict, forecast3d_dict) = self.access_heweather_forecast_and_observe(cityid, roundVal)
            if roundVal:
                roundVal = False
            else:
                roundVal = True
            if ret:
                if forecast3d_dict not in (False, None, {}, '', '[]', "['']"):
                    self.insert_or_update_heweather_forecast(forecast3d_dict, now_date, True)
                if observe_db_record != []:#update observe
                    if observe_dict not in (False, None, {}, '', '[]', "['']"):
                        self.insert_or_update_observe(cityid, observe_dict, now_date, False)#20170810
                else:#insert observe
                    if observe_dict not in (False, None, {}, '', '[]', "['']"):
                        self.insert_or_update_observe(cityid, observe_dict, now_date, True)
            else:
                if len(forecast_db_record) >= 1:
                    for i in range(0, len(forecast_db_record[0])):
                        forecast3d_dict[forecast_key_list[i]] = forecast_db_record[0][i]
        return forecast3d_dict
#-------------------------------------------20170627 end------------------------------------------------






#-------------------------------------------------------------------------------------------
    # 20180827 heweather s6 version
    def insert_or_update_heweather_air_to_db(self, dict_data, isInsert):
        if isInsert:
            self.db.insert_heweather_air_s6_data(str(dict_data['id']),str(dict_data['location']),str(dict_data['pub_time']),str(dict_data['aqi']),str(dict_data['qlty']),str(dict_data['main']),str(dict_data['pm25']),str(dict_data['pm10']),str(dict_data['no2']),str(dict_data['so2']),str(dict_data['co']),str(dict_data['o3']))
        else:
            self.db.update_heweather_air_s6_data(str(dict_data['pub_time']),str(dict_data['aqi']),str(dict_data['qlty']),str(dict_data['main']),str(dict_data['pm25']),str(dict_data['pm10']),str(dict_data['no2']),str(dict_data['so2']),str(dict_data['co']),str(dict_data['o3']),str(dict_data['id']))

    def insert_or_update_heweather_observe_to_db(self, dict_data, isInsert):
        if isInsert:
            self.db.insert_heweather_observe_s6_data(str(dict_data['id']),str(dict_data['location']),str(dict_data['parent_city']),str(dict_data['admin_area']),str(dict_data['cnty']),str(dict_data['lat']),str(dict_data['lon']),str(dict_data['tz']),str(dict_data['update_loc']),str(dict_data['update_utc']),str(dict_data['cloud']),str(dict_data['cond_code']),str(dict_data['cond_txt']),str(dict_data['fl']),str(dict_data['hum']),str(dict_data['pcpn']),str(dict_data['pres']),str(dict_data['tmp']),str(dict_data['vis']),str(dict_data['wind_deg']),str(dict_data['wind_dir']),str(dict_data['wind_sc']),str(dict_data['wind_spd']))
        else:
            self.db.update_heweather_observe_s6_data(str(dict_data['location']),str(dict_data['parent_city']),str(dict_data['admin_area']),str(dict_data['cnty']),str(dict_data['lat']),str(dict_data['lon']),str(dict_data['tz']),str(dict_data['update_loc']),str(dict_data['update_utc']),str(dict_data['cloud']),str(dict_data['cond_code']),str(dict_data['cond_txt']),str(dict_data['fl']),str(dict_data['hum']),str(dict_data['pcpn']),str(dict_data['pres']),str(dict_data['tmp']),str(dict_data['vis']),str(dict_data['wind_deg']),str(dict_data['wind_dir']),str(dict_data['wind_sc']),str(dict_data['wind_spd']),str(dict_data['id']))

    def insert_or_update_heweather_forecast_to_db(self, dict_data, isInsert):
        if isInsert:
            #self.db.insert_heweather_forecast_s6_data(dict_data)
            self.db.insert_heweather_forecast_s6_data(str(dict_data['id']),str(dict_data['location']),str(dict_data['update_loc']),str(dict_data['cond_code_d0']),str(dict_data['cond_code_n0']),str(dict_data['cond_txt_d0']),str(dict_data['cond_txt_n0']),str(dict_data['forcast_date0']),str(dict_data['hum0']),str(dict_data['mr_ms0']),str(dict_data['pcpn0']),str(dict_data['pop0']),str(dict_data['pres0']),str(dict_data['sr_ss0']),str(dict_data['tmp_max0']),str(dict_data['tmp_min0']),str(dict_data['uv_index0']),str(dict_data['vis0']),str(dict_data['wind_deg0']),str(dict_data['wind_dir0']),str(dict_data['wind_sc0']),str(dict_data['wind_spd0']),str(dict_data['cond_code_d1']),str(dict_data['cond_code_n1']),str(dict_data['cond_txt_d1']),str(dict_data['cond_txt_n1']),str(dict_data['forcast_date1']),str(dict_data['hum1']),str(dict_data['mr_ms1']),str(dict_data['pcpn1']),str(dict_data['pop1']),str(dict_data['pres1']),str(dict_data['sr_ss1']),str(dict_data['tmp_max1']),str(dict_data['tmp_min1']),str(dict_data['uv_index1']),str(dict_data['vis1']),str(dict_data['wind_deg1']),str(dict_data['wind_dir1']),str(dict_data['wind_sc1']),str(dict_data['wind_spd1']),str(dict_data['cond_code_d2']),str(dict_data['cond_code_n2']),str(dict_data['cond_txt_d2']),str(dict_data['cond_txt_n2']),str(dict_data['forcast_date2']),str(dict_data['hum2']),str(dict_data['mr_ms2']),str(dict_data['pcpn2']),str(dict_data['pop2']),str(dict_data['pres2']),str(dict_data['sr_ss2']),str(dict_data['tmp_max2']),str(dict_data['tmp_min2']),str(dict_data['uv_index2']),str(dict_data['vis2']),str(dict_data['wind_deg2']),str(dict_data['wind_dir2']),str(dict_data['wind_sc2']),str(dict_data['wind_spd2']))
        else:
            #self.db.update_heweather_forecast_s6_data(dict_data)
            self.db.update_heweather_forecast_s6_data(str(dict_data['location']),str(dict_data['update_loc']),str(dict_data['cond_code_d0']),str(dict_data['cond_code_n0']),str(dict_data['cond_txt_d0']),str(dict_data['cond_txt_n0']),str(dict_data['forcast_date0']),str(dict_data['hum0']),str(dict_data['mr_ms0']),str(dict_data['pcpn0']),str(dict_data['pop0']),str(dict_data['pres0']),str(dict_data['sr_ss0']),str(dict_data['tmp_max0']),str(dict_data['tmp_min0']),str(dict_data['uv_index0']),str(dict_data['vis0']),str(dict_data['wind_deg0']),str(dict_data['wind_dir0']),str(dict_data['wind_sc0']),str(dict_data['wind_spd0']),str(dict_data['cond_code_d1']),str(dict_data['cond_code_n1']),str(dict_data['cond_txt_d1']),str(dict_data['cond_txt_n1']),str(dict_data['forcast_date1']),str(dict_data['hum1']),str(dict_data['mr_ms1']),str(dict_data['pcpn1']),str(dict_data['pop1']),str(dict_data['pres1']),str(dict_data['sr_ss1']),str(dict_data['tmp_max1']),str(dict_data['tmp_min1']),str(dict_data['uv_index1']),str(dict_data['vis1']),str(dict_data['wind_deg1']),str(dict_data['wind_dir1']),str(dict_data['wind_sc1']),str(dict_data['wind_spd1']),str(dict_data['cond_code_d2']),str(dict_data['cond_code_n2']),str(dict_data['cond_txt_d2']),str(dict_data['cond_txt_n2']),str(dict_data['forcast_date2']),str(dict_data['hum2']),str(dict_data['mr_ms2']),str(dict_data['pcpn2']),str(dict_data['pop2']),str(dict_data['pres2']),str(dict_data['sr_ss2']),str(dict_data['tmp_max2']),str(dict_data['tmp_min2']),str(dict_data['uv_index2']),str(dict_data['vis2']),str(dict_data['wind_deg2']),str(dict_data['wind_dir2']),str(dict_data['wind_sc2']),str(dict_data['wind_spd2']),str(dict_data['id']))

    def insert_or_update_heweather_lifestyle_to_db(self, dict_data, isInsert):
        if isInsert:
            self.db.insert_heweather_lifestyle_s6_data(str(dict_data['id']),str(dict_data['comf_brf']),str(dict_data['comf_txt']),str(dict_data['drsg_brf']),str(dict_data['drsg_txt']),str(dict_data['flu_brf']),str(dict_data['flu_txt']),str(dict_data['sport_brf']),str(dict_data['sport_txt']),str(dict_data['trav_brf']),str(dict_data['trav_txt']),str(dict_data['uv_brf']),str(dict_data['uv_txt']),str(dict_data['cw_brf']),str(dict_data['cw_txt']),str(dict_data['air_brf']),str(dict_data['air_txt']))
        else:
            self.db.update_heweather_lifestyle_s6_data(str(dict_data['comf_brf']),str(dict_data['comf_txt']),str(dict_data['drsg_brf']),str(dict_data['drsg_txt']),str(dict_data['flu_brf']),str(dict_data['flu_txt']),str(dict_data['sport_brf']),str(dict_data['sport_txt']),str(dict_data['trav_brf']),str(dict_data['trav_txt']),str(dict_data['uv_brf']),str(dict_data['uv_txt']),str(dict_data['cw_brf']),str(dict_data['cw_txt']),str(dict_data['air_brf']),str(dict_data['air_txt']),str(dict_data['id']))

    # https://free-api.heweather.com/s6/weather?location=CN101250101&key=xxxxxxxxxxxxxxxx
    def access_heweather_api_air_now_interface(self, cityid, isInsert):
        air_url = HEWEATHER_AIR_NOW_URL % (cityid)
        air_key_list = ['id' ,'location', 'pub_time', 'aqi', 'qlty', 'main', 'pm25', 'pm10', 'no2', 'so2', 'co', 'o3']
        air_data_dict = {}

        # init value
        for i in range(0, len(air_key_list)):
            air_data_dict[air_key_list[i]] = "Unknown"
        air_data_dict['id'] = cityid
        air_data_dict['pub_time'] = "2018-08-28 22:00"

        try:
            json_string = read_json_from_url(air_url)
            parsed_json = json.loads(json_string)
        except Exception as e:
            print "read json error:", str(e)
            return air_data_dict

        tmp_list = parsed_json['HeWeather6'][0]
        if tmp_list:
            if tmp_list['status'] == "ok":
                if tmp_list.has_key('basic'):
                    basic_dict = tmp_list['basic']
                    if (isinstance(basic_dict, dict)):
                        air_data_dict['location'] = basic_dict.get('location', "Unknown")

                if tmp_list.has_key('air_now_city'):
                    air_dict = tmp_list['air_now_city']
                    if (isinstance(air_dict, dict)):
                        air_data_dict['aqi'] = air_dict.get('aqi', "Unknown")
                        air_data_dict['qlty'] = air_dict.get('qlty', "Unknown")
                        air_data_dict['main'] = air_dict.get('main', "Unknown")
                        air_data_dict['pm25'] = air_dict.get('pm25', "Unknown")
                        air_data_dict['pm10'] = air_dict.get('pm10', "Unknown")
                        air_data_dict['no2'] = air_dict.get('no2', "Unknown")
                        air_data_dict['so2'] = air_dict.get('so2', "Unknown")
                        air_data_dict['co'] = air_dict.get('co', "Unknown")
                        air_data_dict['o3'] = air_dict.get('o3', "Unknown")
                        air_data_dict['pub_time'] = air_dict.get('pub_time', "2018-08-28 22:00")

        self.insert_or_update_heweather_air_to_db(air_data_dict, isInsert)

        return air_data_dict

    # https://free-api.heweather.com/s6/air/now?location=CN101250101&key=xxxxxxxxxxxxxxxx
    def access_heweather_api_weather_interface(self, cityid, isInsert, isObserve):
        '''
        isInsert: insert or update db
        isObserve: weather observe or weather forecast
        '''
        url = HEWEATHER_WEATHER_URL % (cityid)
        observe_key_list = ['id','location','parent_city','admin_area','cnty','lat','lon','tz','update_loc','update_utc','cloud','cond_code','cond_txt','fl','hum','pcpn','pres','tmp','vis','wind_deg','wind_dir','wind_sc','wind_spd']
        observe_data_dict = {}
        forecast_key_list = ['id','location','update_loc','cond_code_d0','cond_code_n0','cond_txt_d0','cond_txt_n0','forcast_date0','hum0','mr_ms0','pcpn0','pop0','pres0','sr_ss0','tmp_max0','tmp_min0','uv_index0','vis0','wind_deg0','wind_dir0','wind_sc0','wind_spd0','cond_code_d1','cond_code_n1','cond_txt_d1','cond_txt_n1','forcast_date1','hum1','mr_ms1','pcpn1','pop1','pres1','sr_ss1','tmp_max1','tmp_min1','uv_index1','vis1','wind_deg1','wind_dir1','wind_sc1','wind_spd1','cond_code_d2','cond_code_n2','cond_txt_d2','cond_txt_n2','forcast_date2','hum2','mr_ms2','pcpn2','pop2','pres2','sr_ss2','tmp_max2','tmp_min2','uv_index2','vis2','wind_deg2','wind_dir2','wind_sc2','wind_spd2']
        forecast_data_dict = {}
        lifestyle_key_list = ['id','comf_brf','comf_txt','drsg_brf','drsg_txt','flu_brf','flu_txt','sport_brf','sport_txt','trav_brf','trav_txt','uv_brf','uv_txt','cw_brf','cw_txt','air_brf','air_txt']
        lifestyle_data_dict = {}

        # init value
        for i in range(0, len(observe_key_list)):
            observe_data_dict[observe_key_list[i]] = "Unknown"
        observe_data_dict['id'] = cityid
        observe_data_dict['update_loc'] = "2018-08-28 22:00"
        observe_data_dict['update_utc'] = "2018-08-28 22:00"
        for i in range(0, len(forecast_key_list)):
            forecast_data_dict[forecast_key_list[i]] = "Unknown"
        forecast_data_dict['id'] = cityid
        forecast_data_dict['update_loc'] = "2018-08-28 22:00"
        for i in range(0, len(lifestyle_key_list)):
            lifestyle_data_dict[lifestyle_key_list[i]] = "Unknown"
        lifestyle_data_dict['id'] = cityid

        try:
            json_string = read_json_from_url(url)
            parsed_json = json.loads(json_string)
        except Exception as e:
            print "read json error:", str(e)
            return observe_data_dict

        tmp_list = parsed_json['HeWeather6'][0]
        if tmp_list:
            if tmp_list['status'] == "ok":
                if tmp_list.has_key('basic'):
                    basic_dict = tmp_list['basic']
                    if (isinstance(basic_dict, dict)):
                        observe_data_dict['location'] = basic_dict.get('location', "Unknown")
                        forecast_data_dict['location'] = observe_data_dict['location']
                        observe_data_dict['parent_city'] = basic_dict.get('parent_city', "Unknown")
                        observe_data_dict['admin_area'] = basic_dict.get('admin_area', "Unknown")
                        observe_data_dict['cnty'] = basic_dict.get('cnty', "Unknown")
                        observe_data_dict['lat'] = basic_dict.get('lat', "Unknown")
                        observe_data_dict['lon'] = basic_dict.get('lon', "Unknown")
                        observe_data_dict['tz'] = basic_dict.get('tz', "Unknown")

                if tmp_list.has_key('update'):
                    time_dict = tmp_list['update']
                    if (isinstance(time_dict, dict)):
                        observe_data_dict['update_loc'] = time_dict.get('loc', "2018-08-28 22:00")
                        forecast_data_dict['update_loc'] = observe_data_dict['update_loc']
                        observe_data_dict['update_utc'] = time_dict.get('utc', "2018-08-28 22:00")

                if tmp_list.has_key('now'):
                    now_dict = tmp_list['now']
                    if (isinstance(now_dict, dict)):
                        observe_data_dict['cloud'] = now_dict.get('cloud', "Unknown")
                        observe_data_dict['cond_code'] = now_dict.get('cond_code', "Unknown")
                        observe_data_dict['cond_txt'] = now_dict.get('cond_txt', "Unknown")
                        observe_data_dict['fl'] = now_dict.get('fl', "Unknown")
                        observe_data_dict['hum'] = now_dict.get('hum', "Unknown")
                        observe_data_dict['pcpn'] = now_dict.get('pcpn', "Unknown")
                        observe_data_dict['pres'] = now_dict.get('pres', "Unknown")
                        observe_data_dict['tmp'] = now_dict.get('tmp', "Unknown")
                        observe_data_dict['vis'] = now_dict.get('vis', "Unknown")
                        observe_data_dict['wind_deg'] = now_dict.get('wind_deg', "Unknown")
                        observe_data_dict['wind_dir'] = now_dict.get('wind_dir', "Unknown")
                        observe_data_dict['wind_sc'] = now_dict.get('wind_sc', "Unknown")
                        observe_data_dict['wind_spd'] = now_dict.get('wind_spd', "Unknown")

                if tmp_list.has_key('daily_forecast'):
                    forecast_len = len(tmp_list['daily_forecast'])#3 days forecast
                    if forecast_len > 0:
                        i = 0;
                        daily_forecast = tmp_list.get('daily_forecast', "")
                        if daily_forecast not in (False, None, {}, '', "", '[]', "['']"):
                            for data in daily_forecast:#//3 days weatherforecast
                                if (i == 0):#first day
                                    if (isinstance(data, dict)):
                                        forecast_data_dict['cond_code_d0'] = data.get('cond_code_d', "Unknown")
                                        forecast_data_dict['cond_code_n0'] = data.get('cond_code_n', "Unknown")
                                        forecast_data_dict['cond_txt_d0'] = data.get('cond_txt_d', "Unknown")
                                        forecast_data_dict['cond_txt_n0'] = data.get('cond_txt_n', "Unknown")
                                        forecast_data_dict['forcast_date0'] = data.get('date', "Unknown")
                                        forecast_data_dict['hum0'] = data.get('hum', "Unknown")
                                        forecast_data_dict['mr_ms0'] = data.get('mr', "Unknown") + "+" + data.get('ms', "Unknown")
                                        forecast_data_dict['pcpn0'] = data.get('pcpn', "Unknown")
                                        forecast_data_dict['pop0'] = data.get('pop', "Unknown")
                                        forecast_data_dict['pres0'] = data.get('pres', "Unknown")
                                        forecast_data_dict['sr_ss0'] = data.get('sr', "Unknown") + "+" + data.get('ss', "Unknown")
                                        forecast_data_dict['tmp_max0'] = data.get('tmp_max', "Unknown")
                                        forecast_data_dict['tmp_min0'] = data.get('tmp_min', "Unknown")
                                        forecast_data_dict['uv_index0'] = data.get('uv_index', "Unknown")
                                        forecast_data_dict['vis0'] = data.get('vis', "Unknown")
                                        forecast_data_dict['wind_deg0'] = data.get('wind_deg', "Unknown")
                                        forecast_data_dict['wind_dir0'] = data.get('wind_dir', "Unknown")
                                        forecast_data_dict['wind_sc0'] = data.get('wind_sc', "Unknown")
                                        forecast_data_dict['wind_spd0'] = data.get('wind_spd', "Unknown")
                                elif (i == 1):
                                    if (isinstance(data, dict)):
                                        forecast_data_dict['cond_code_d1'] = data.get('cond_code_d', "Unknown")
                                        forecast_data_dict['cond_code_n1'] = data.get('cond_code_n', "Unknown")
                                        forecast_data_dict['cond_txt_d1'] = data.get('cond_txt_d', "Unknown")
                                        forecast_data_dict['cond_txt_n1'] = data.get('cond_txt_n', "Unknown")
                                        forecast_data_dict['forcast_date1'] = data.get('date', "Unknown")
                                        forecast_data_dict['hum1'] = data.get('hum', "Unknown")
                                        forecast_data_dict['mr_ms1'] = data.get('mr', "Unknown") + "+" + data.get('ms', "Unknown")
                                        forecast_data_dict['pcpn1'] = data.get('pcpn', "Unknown")
                                        forecast_data_dict['pop1'] = data.get('pop', "Unknown")
                                        forecast_data_dict['pres1'] = data.get('pres', "Unknown")
                                        forecast_data_dict['sr_ss1'] = data.get('sr', "Unknown") + "+" + data.get('ss', "Unknown")
                                        forecast_data_dict['tmp_max1'] = data.get('tmp_max', "Unknown")
                                        forecast_data_dict['tmp_min1'] = data.get('tmp_min', "Unknown")
                                        forecast_data_dict['uv_index1'] = data.get('uv_index', "Unknown")
                                        forecast_data_dict['vis1'] = data.get('vis', "Unknown")
                                        forecast_data_dict['wind_deg1'] = data.get('wind_deg', "Unknown")
                                        forecast_data_dict['wind_dir1'] = data.get('wind_dir', "Unknown")
                                        forecast_data_dict['wind_sc1'] = data.get('wind_sc', "Unknown")
                                        forecast_data_dict['wind_spd1'] = data.get('wind_spd', "Unknown")
                                elif (i == 2):
                                    if (isinstance(data, dict)):
                                        forecast_data_dict['cond_code_d2'] = data.get('cond_code_d', "Unknown")
                                        forecast_data_dict['cond_code_n2'] = data.get('cond_code_n', "Unknown")
                                        forecast_data_dict['cond_txt_d2'] = data.get('cond_txt_d', "Unknown")
                                        forecast_data_dict['cond_txt_n2'] = data.get('cond_txt_n', "Unknown")
                                        forecast_data_dict['forcast_date2'] = data.get('date', "Unknown")
                                        forecast_data_dict['hum2'] = data.get('hum', "Unknown")
                                        forecast_data_dict['mr_ms2'] = data.get('mr', "Unknown") + "+" + data.get('ms', "Unknown")
                                        forecast_data_dict['pcpn2'] = data.get('pcpn', "Unknown")
                                        forecast_data_dict['pop2'] = data.get('pop', "Unknown")
                                        forecast_data_dict['pres2'] = data.get('pres', "Unknown")
                                        forecast_data_dict['sr_ss2'] = data.get('sr', "Unknown") + "+" + data.get('ss', "Unknown")
                                        forecast_data_dict['tmp_max2'] = data.get('tmp_max', "Unknown")
                                        forecast_data_dict['tmp_min2'] = data.get('tmp_min', "Unknown")
                                        forecast_data_dict['uv_index2'] = data.get('uv_index', "Unknown")
                                        forecast_data_dict['vis2'] = data.get('vis', "Unknown")
                                        forecast_data_dict['wind_deg2'] = data.get('wind_deg', "Unknown")
                                        forecast_data_dict['wind_dir2'] = data.get('wind_dir', "Unknown")
                                        forecast_data_dict['wind_sc2'] = data.get('wind_sc', "Unknown")
                                        forecast_data_dict['wind_spd2'] = data.get('wind_spd', "Unknown")
                                i = i+1

                if tmp_list.has_key('lifestyle'):
                    suggestion_dict = tmp_list['lifestyle']
                    for i in range(len(suggestion_dict)):
                        sub_dict = suggestion_dict[i]
                        if (isinstance(sub_dict, dict)):
                            if sub_dict.get('type', "") == "comf":
                                lifestyle_data_dict['comf_brf'] = sub_dict.get('brf', "Unknown")
                                lifestyle_data_dict['comf_txt'] = sub_dict.get('txt', "Unknown")
                            elif sub_dict.get('type', "") == "cw":
                                lifestyle_data_dict['cw_brf'] = sub_dict.get('brf', "Unknown")
                                lifestyle_data_dict['cw_txt'] = sub_dict.get('txt', "Unknown")
                            elif sub_dict.get('type', "") == "drsg":
                                lifestyle_data_dict['drsg_brf'] = sub_dict.get('brf', "Unknown")
                                lifestyle_data_dict['drsg_txt'] = sub_dict.get('txt', "Unknown")
                            elif sub_dict.get('type', "") == "flu":
                                lifestyle_data_dict['flu_brf'] = sub_dict.get('brf', "Unknown")
                                lifestyle_data_dict['flu_txt'] = sub_dict.get('txt', "Unknown")
                            elif sub_dict.get('type', "") == "sport":
                                lifestyle_data_dict['sport_brf'] = sub_dict.get('brf', "Unknown")
                                lifestyle_data_dict['sport_txt'] = sub_dict.get('txt', "Unknown")
                            elif sub_dict.get('type', "") == "trav":
                                lifestyle_data_dict['trav_brf'] = sub_dict.get('brf', "Unknown")
                                lifestyle_data_dict['trav_txt'] = sub_dict.get('txt', "Unknown")
                            elif sub_dict.get('type', "") == "uv":
                                lifestyle_data_dict['uv_brf'] = sub_dict.get('brf', "Unknown")
                                lifestyle_data_dict['uv_txt'] = sub_dict.get('txt', "Unknown")
                            elif sub_dict.get('type', "") == "air":
                                lifestyle_data_dict['air_brf'] = sub_dict.get('brf', "Unknown")
                                lifestyle_data_dict['air_txt'] = sub_dict.get('txt', "Unknown")

        self.insert_or_update_heweather_observe_to_db(observe_data_dict, isInsert)

        forecast_db_record = self.db.search_heweather_forecast_s6_record(cityid)
        if forecast_db_record != []:
            self.insert_or_update_heweather_forecast_to_db(forecast_data_dict, False)
        else:
            self.insert_or_update_heweather_forecast_to_db(forecast_data_dict, True)

        lifestyle_db_record = self.db.search_heweather_lifestyle_s6_record(cityid)
        if lifestyle_db_record != []:
            self.insert_or_update_heweather_lifestyle_to_db(lifestyle_data_dict, False)
        else:
            self.insert_or_update_heweather_lifestyle_to_db(lifestyle_data_dict, True)

        if isObserve:
            return observe_data_dict
        else:
            return forecast_data_dict

    def update_heweather_api_air_now(self, currentDate, cityid):
        isNeedNew = False
        air_dict = {}
        db_time = None
        db_time_list = self.db.search_heweather_air_s6_record_update_time(cityid)
        if db_time_list in (False, None, [], '', '[]', "['']"):
            air_dict = self.access_heweather_api_air_now_interface(cityid, False)
            return air_dict;

        db_time = db_time_list[0][0]

        if db_time is not None:#2018-08-29 08:45
            db_time_list = db_time.split(" ")
            now_date_list = currentDate.split(" ")
            # compare now_time with db_time ,when they are different, then access weather data again
            if db_time_list[0] != now_date_list[0]:#different day
                isNeedNew = True
            else:# same day
                dbHour = int(db_time_list[1].split(":")[0])#16
                nowHour = int(now_date_list[1].split(":")[0])#19
                if abs(nowHour - dbHour) > 1:
                    isNeedNew = True

            if isNeedNew:
                isNeedNew = False
                air_dict = self.access_heweather_api_air_now_interface(cityid, False)
            else:
                return air_dict
        else:
            air_dict = self.access_heweather_api_air_now_interface(cityid, False)

        return air_dict

    def update_heweather_api_weather(self, currentDate, cityid, isObserve):
        isNeedNew = False
        weather_dict = {}
        db_time = None
        if isObserve:
            db_time_list = self.db.search_heweather_observe_s6_record_update_time(cityid)
        else:
            db_time_list = self.db.search_heweather_forecast_s6_record_update_time(cityid)
        if db_time_list in (False, None, [], '', '[]', "['']"):
            if isObserve:
                weather_dict = self.access_heweather_api_weather_interface(cityid, False, True)#fisrt False:update, second True:observe weather
            else:
                weather_dict = self.access_heweather_api_weather_interface(cityid, False, False)#fisrt False:update, second False:forecast weather

        db_time = db_time_list[0][0]
        if db_time is not None:#2018-08-29 08:45
            db_time_list = db_time.split(" ")
            now_date_list = currentDate.split(" ")
            # compare now_time with db_time ,when they are different, then access weather data again
            if db_time_list[0] != now_date_list[0]:#different day
                isNeedNew = True
            else:# same day
                dbHour = int(db_time_list[1].split(":")[0])#16
                nowHour = int(now_date_list[1].split(":")[0])#19
                if abs(nowHour - dbHour) > 1:
                    isNeedNew = True

            if isNeedNew:
                if isObserve:
                    weather_dict = self.access_heweather_api_weather_interface(cityid, False, True)#fisrt False:update, second True:observe weather
                else:
                    weather_dict = self.access_heweather_api_weather_interface(cityid, False, False)#fisrt False:update, second False:forecast weather
            else:
                return weather_dict
        else:
            if isObserve:
                weather_dict = self.access_heweather_api_weather_interface(cityid, False, True)#fisrt False:update, second True:observe weather
            else:
                weather_dict = self.access_heweather_api_weather_interface(cityid, False, False)#fisrt False:update, second False:forecast weather

        return weather_dict;

    def get_heweather_observe_s6(self, cityid):
        '''
        对应于load和loads，dump的第一个参数是对象字典，第二个参数是文件对象，可以直接将转换后的json数据写入文件，dumps的第一个参数是对象字典，其余都是可选参数。dump和dumps的可选参数相同，这些参数都相当实用，现将用到的参数记录如下：
        ensure_ascii 默认为True，保证转换后的json字符串中全部是ascii字符，非ascii字符都会被转义。如果数据中存在中文或其他非ascii字符，最好将ensure_ascii设置为False，保证输出结果正常。
        indent 缩进，默认为None，没有缩进，设置为正整数时，输出的格式将按照indent指定的半角空格数缩进，相当实用。
        separators 设置分隔符，默认的分隔符是(',', ': ')，如果需要自定义json中的分隔符，例如调整冒号前后的空格数，可以按照(item_separator, key_separator)的形式设置。
        sort_keys 默认为False，设为True时，输出结果将按照字典中的key排序。

        loads()：将json数据转化成dict数据
        dumps()：将dict数据转化成json数据   sort_keys：根据key排序   indent：以4个空格缩进，输出阅读友好型    ensure_ascii: 可以序列化非ascii码（中文等）
        load()：读取json文件数据，转成dict数据
        dump()：将dict数据转化成json数据后写入json文件
        '''
        observe_dict = {}
        combination_dict = {}
        air_dict = {}
        now_dict = {}
        # key list remove 'id'
        air_key_list = ['location','pub_time','aqi','qlty','main','pm25','pm10','no2','so2','co','o3']
        observe_key_list = ['location','parent_city','admin_area','cnty','lat','lon','tz','update_loc','update_utc','cloud','cond_code','cond_txt','fl','hum','pcpn','pres','tmp','vis','wind_deg','wind_dir','wind_sc','wind_spd']
        now_date = get_local_format_time()

        air_db_record = self.db.search_heweather_air_s6_record(cityid)
        if air_db_record != []:
            air_dict = self.update_heweather_api_air_now(str(now_date), cityid)
            if air_dict in (False, None, {}, '', '[]', "['']"):
                for i in range(0, len(air_db_record[0])):
                    air_dict[air_key_list[i]] = air_db_record[0][i]
                air_dict['id'] = cityid#air_dict['id'].append(cityid)
        else:
            air_dict = self.access_heweather_api_air_now_interface(cityid, True)

        observe_db_record = self.db.search_heweather_observe_s6_record(cityid)
        if observe_db_record != []:
            now_dict = self.update_heweather_api_weather(str(now_date), cityid, True)
            if now_dict in (False, None, {}, '', '[]', "['']"):
                for i in range(0, len(observe_db_record[0])):
                    now_dict[observe_key_list[i]] = observe_db_record[0][i]
                now_dict['id'] = cityid
        else:
            now_dict = self.access_heweather_api_weather_interface(cityid, True, True)#first True:insert, second True:observe weather

        if 'id' not in now_dict.keys() or now_dict['id'] == "Unknown":
            if air_dict.has_key('id'):
                now_dict["id"] = air_dict["id"]
            else:
                now_dict['id'] = "Unknown"

        if air_dict.has_key('id'):
            del air_dict["id"]
        if air_dict.has_key('location'):
            del air_dict["location"]
        if air_dict.has_key('pub_time'):
            del air_dict["pub_time"]

        combination_dict['weather'] = now_dict;
        combination_dict['air'] = air_dict;
        observe_dict['KylinWeather'] = combination_dict

        observe_json = json.dumps(observe_dict, ensure_ascii=False, sort_keys=True, indent=4)
        #print check_json_format("""{"a":1}""")#True
        #print check_json_format("""{'a':1}""")#False
        #print check_json_format({'a': 1})#False
        #print check_json_format(100)#False
        return observe_json

    def get_heweather_forecast_s6(self, cityid):
        '''
        mydict = {}
        dict1 = {}
        dict2 = {}
        dict3 = {}
        mydict = dict(dict1.items() + dict2.items() + dict3.items())

        #mydict.update(dict1)
        #mydict.update(dict2)
        #mydict.update(dict3)

        #for k,v in dict1.items()
        #    mydict[k] = v
        #for k,v in dict2.items()
        #    mydict[k] = v
        #for k,v in dict2.items()
        #    mydict[k] = v
        '''
        forecast_dict = {}
        combination_dict = {}
        days_dict = {}
        lifestyle_dict = {}
        # key list remove 'id'
        forecast_key_list = ['location','update_loc','cond_code_d0','cond_code_n0','cond_txt_d0','cond_txt_n0','forcast_date0','hum0','mr_ms0','pcpn0','pop0','pres0','sr_ss0','tmp_max0','tmp_min0','uv_index0','vis0','wind_deg0','wind_dir0','wind_sc0','wind_spd0','cond_code_d1','cond_code_n1','cond_txt_d1','cond_txt_n1','forcast_date1','hum1','mr_ms1','pcpn1','pop1','pres1','sr_ss1','tmp_max1','tmp_min1','uv_index1','vis1','wind_deg1','wind_dir1','wind_sc1','wind_spd1','cond_code_d2','cond_code_n2','cond_txt_d2','cond_txt_n2','forcast_date2','hum2','mr_ms2','pcpn2','pop2','pres2','sr_ss2','tmp_max2','tmp_min2','uv_index2','vis2','wind_deg2','wind_dir2','wind_sc2','wind_spd2']
        lifestyle_key_list = ['comf_brf','comf_txt','drsg_brf','drsg_txt','flu_brf','flu_txt','sport_brf','sport_txt','trav_brf','trav_txt','uv_brf','uv_txt','cw_brf','cw_txt','air_brf','air_txt']
        now_date = get_local_format_time()

        forecast_db_record = self.db.search_heweather_forecast_s6_record(cityid)
        if forecast_db_record != []:
            days_dict = self.update_heweather_api_weather(str(now_date), cityid, False)
            if days_dict in (False, None, {}, '', '[]', "['']"):
                for i in range(0, len(forecast_db_record[0])):
                    days_dict[forecast_key_list[i]] = forecast_db_record[0][i]
                days_dict['id'] = cityid
        else:
            days_dict = self.access_heweather_api_weather_interface(cityid, True, False)#fisrt True:insert, second False:forecast weather

        # Attention: lifestyle_dict remove 'id'
        lifestyle_key_list = ['comf_brf','comf_txt','drsg_brf','drsg_txt','flu_brf','flu_txt','sport_brf','sport_txt','trav_brf','trav_txt','uv_brf','uv_txt','cw_brf','cw_txt','air_brf','air_txt']
        for i in range(0, len(lifestyle_key_list)):
            lifestyle_dict[lifestyle_key_list[i]] = "Unknown"

        lifestyle_db_record = self.db.search_heweather_lifestyle_s6_record(cityid)
        if len(lifestyle_db_record) >= 1:
            for i in range(0, len(lifestyle_db_record[0])):
                lifestyle_dict[lifestyle_key_list[i]] = lifestyle_db_record[0][i]
        #lifestyle_dict['id'] = cityid

        combination_dict['forecast'] = days_dict;
        combination_dict['lifestyle'] = lifestyle_dict;
        forecast_dict['KylinWeather'] = combination_dict

        forecast_json = json.dumps(forecast_dict, ensure_ascii=False, sort_keys=True, indent=4)
        return forecast_json


    def check_json_format(self, raw_msg):
        '''
        用于判断一个字符串是否符合Json格式
        :param self:
        :return:
        '''
        if isinstance(raw_msg, str):#首先判断变量是否为字符串
            try:
                json.loads(raw_msg, encoding='utf-8')
            except ValueError:
                return False
            return True
        else:
            return False
#----------------------------------------------------------------------------














    # 20200307---------------------------------------
    def insert_or_update_s6_heweather_lifestyle_to_db(self, dict_data, isInsert):
        if isInsert:
            self.db.insert_s6_heweather_lifestyle(str(dict_data['id']),str(dict_data['comf_brf']),str(dict_data['comf_txt']),str(dict_data['drsg_brf']),str(dict_data['drsg_txt']),str(dict_data['flu_brf']),str(dict_data['flu_txt']),str(dict_data['sport_brf']),str(dict_data['sport_txt']),str(dict_data['trav_brf']),str(dict_data['trav_txt']),str(dict_data['uv_brf']),str(dict_data['uv_txt']),str(dict_data['cw_brf']),str(dict_data['cw_txt']),str(dict_data['air_brf']),str(dict_data['air_txt']))
        else:
            self.db.update_s6_heweather_lifestyle(str(dict_data['comf_brf']),str(dict_data['comf_txt']),str(dict_data['drsg_brf']),str(dict_data['drsg_txt']),str(dict_data['flu_brf']),str(dict_data['flu_txt']),str(dict_data['sport_brf']),str(dict_data['sport_txt']),str(dict_data['trav_brf']),str(dict_data['trav_txt']),str(dict_data['uv_brf']),str(dict_data['uv_txt']),str(dict_data['cw_brf']),str(dict_data['cw_txt']),str(dict_data['air_brf']),str(dict_data['air_txt']),str(dict_data['id']))

    def insert_or_update_s6_heweather_data_to_db(self, dict_data, isInsert):
        if isInsert:
            self.db.insert_s6_heweather_weather_data(str(dict_data['id']),str(dict_data['location']),str(dict_data['admin_area']),str(dict_data['cnty']),str(dict_data['update_time']),int(dict_data['forecast_days']),str(dict_data['aqi']),str(dict_data['now']),str(dict_data['forecast']))
        else:
            self.db.update_s6_heweather_weather_data(str(dict_data['id']),str(dict_data['update_time']),int(dict_data['forecast_days']),str(dict_data['aqi']),str(dict_data['now']),str(dict_data['forecast']))

    # 从和风天气api接口获取数据
    def access_s6_heweather_all_data(self, cityid, readtime):
        needRefresh = False
        aqi_url = HEWEATHER_AIR_NOW_URL % (cityid)
        weather_url = HEWEATHER_WEATHER_URL % (cityid)
        weather_data = {}
        lifestyle_data = {}
        weather_key_list = ['id', 'location', 'admin_area', 'cnty', 'update_time', 'forecast_days', 'aqi', 'now', 'forecast']
        lifestyle_key_list = ['id','comf_brf','comf_txt','drsg_brf','drsg_txt','flu_brf','flu_txt','sport_brf','sport_txt','trav_brf','trav_txt','uv_brf','uv_txt','cw_brf','cw_txt','air_brf','air_txt']

        # init value
        for i in range(0, len(weather_key_list)):
            weather_data[weather_key_list[i]] = "-"
        weather_data['forecast_days'] = 0
        weather_data['id'] = cityid
        weather_data['update_time'] = "2020-03-08 22:00"

        for i in range(0, len(lifestyle_key_list)):
            lifestyle_data[lifestyle_key_list[i]] = "-"
        lifestyle_data['id'] = cityid

        if readtime:
            #从数据库中读取记录的时间
            now_date = str(get_local_format_time())
            db_time = None
            db_time_list = self.db.search_s6_heweather_update_time(cityid)
            if db_time_list in (False, None, [], '', '[]', "['']"):#数据库中没有找到更新的时间，重新读取数据
                needRefresh = True
            else:
                db_time = db_time_list[0][0]
                if db_time is not None:#2018-08-29 08:45
                    db_time_list = db_time.split(" ")
                    now_date_list = now_date.split(" ")
                    # compare now_time with db_time ,when they are different, then access weather data again
                    if db_time_list[0] != now_date_list[0]:#different day
                        needRefresh = True
                    else:# same day
                        dbHour = int(db_time_list[1].split(":")[0])#16
                        nowHour = int(now_date_list[1].split(":")[0])#19
                        if abs(nowHour - dbHour) >= 3:
                            needRefresh = True
        else:
            needRefresh = True


        if needRefresh == False:
            return (False, weather_data, lifestyle_data)
        else:
            try:
                json_aqi_string = read_json_from_url(aqi_url)
                parsed_aqi_json = json.loads(json_aqi_string)

                json_string = read_json_from_url(weather_url)
                parsed_json = json.loads(json_string)
            except Exception as e:
                print "read json error:", str(e)
                return (False, weather_data, lifestyle_data)

            tmp_aqi_list = parsed_aqi_json['HeWeather6'][0]
            if tmp_aqi_list:
                if tmp_aqi_list['status'] == "ok":
                    if tmp_aqi_list.has_key('air_now_city'):
                        aqi_dict = tmp_aqi_list['air_now_city']
                        if (isinstance(aqi_dict, dict)):
                            weather_data['aqi'] = ''
                            for k,v in aqi_dict.items():
                                aqi_tmp_value = k + "=" + v + ","
                                weather_data['aqi'] += aqi_tmp_value

            tmp_list = parsed_json['HeWeather6'][0]
            if tmp_list:
                if tmp_list['status'] == "ok":
                    # basic
                    if tmp_list.has_key('basic'):
                        basic_dict = tmp_list['basic']
                        if (isinstance(basic_dict, dict)):
                            if basic_dict.has_key('location'):
                                weather_data['location'] = basic_dict.get('location', "-")
                            if basic_dict.has_key('admin_area'):
                                weather_data['admin_area'] = basic_dict.get('admin_area', "-")
                            if basic_dict.has_key('cnty'):
                                weather_data['cnty'] = basic_dict.get('cnty', "-")

                    # update
                    if tmp_list.has_key('update'):
                        time_dict = tmp_list['update']
                        if (isinstance(time_dict, dict)):
                            if time_dict.has_key('loc'):
                                weather_data['update_time'] = time_dict.get('loc', "-")

                    # now
                    if tmp_list.has_key('now'):
                        now_dict = tmp_list.get('now', "")
                        if (isinstance(now_dict, dict)):
                            weather_data['now'] = ''
                            for k,v in now_dict.items():
                                now_tmp_value = k + "=" + v + ","
                                weather_data['now'] += now_tmp_value

                    # daily_forecast
                    if tmp_list.has_key('daily_forecast'):
                        daily_forecast = tmp_list.get('daily_forecast', "")
                        forecast_len = len(daily_forecast)#3 or 7 days forecast
                        weather_data['forecast_days'] = forecast_len
                        weather_data['forecast'] = ''
                        for i in range(forecast_len):
                            data_dict = daily_forecast[i]
                            if (isinstance(data_dict, dict)):
                                forecast_value = ''
                                for k,v in data_dict.items():
                                    forecast_tmp_value = k + "=" + v + ","
                                    forecast_value += forecast_tmp_value
                                weather_data['forecast'] += "%s;" % forecast_value

                    # lifestyle
                    if tmp_list.has_key('lifestyle'):
                        suggestion_dict = tmp_list['lifestyle']
                        for i in range(len(suggestion_dict)):
                            sub_dict = suggestion_dict[i]
                            if (isinstance(sub_dict, dict)):
                                if sub_dict.get('type', "") == "comf":
                                    lifestyle_data['comf_brf'] = sub_dict.get('brf', "未知")#舒适度指数  简介
                                    lifestyle_data['comf_txt'] = sub_dict.get('txt', "未知")#舒适度指数  详细描述
                                elif sub_dict.get('type', "") == "drsg":
                                    lifestyle_data['drsg_brf'] = sub_dict.get('brf', "未知")#穿衣指数  简介
                                    lifestyle_data['drsg_txt'] = sub_dict.get('txt', "未知")#穿衣指数  详细描述
                                elif sub_dict.get('type', "") == "flu":
                                    lifestyle_data['flu_brf'] = sub_dict.get('brf', "未知")#感冒指数  简介
                                    lifestyle_data['flu_txt'] = sub_dict.get('txt', "未知")#感冒指数  详细描述
                                elif sub_dict.get('type', "") == "sport":
                                    lifestyle_data['sport_brf'] = sub_dict.get('brf', "未知")#运动指数  简介
                                    lifestyle_data['sport_txt'] = sub_dict.get('txt', "未知")#运动指数  详细描述
                                elif sub_dict.get('type', "") == "trav":
                                    lifestyle_data['trav_brf'] = sub_dict.get('brf', "未知")#旅游指数  简介
                                    lifestyle_data['trav_txt'] = sub_dict.get('txt', "未知")#旅游指数  详细描述
                                elif sub_dict.get('type', "") == "uv":
                                    lifestyle_data['uv_brf'] = sub_dict.get('brf', "未知")#紫外线指数  简介
                                    lifestyle_data['uv_txt'] = sub_dict.get('txt', "未知")#紫外线指数  详细描述
                                elif sub_dict.get('type', "") == "cw":
                                    lifestyle_data['cw_brf'] = sub_dict.get('brf', "未知")#洗车指数  简介
                                    lifestyle_data['cw_txt'] = sub_dict.get('txt', "未知")#洗车指数  详细描述
                                elif sub_dict.get('type', "") == "air":
                                    lifestyle_data['air_brf'] = sub_dict.get('brf', "未知")#空气指数  简介
                                    lifestyle_data['air_txt'] = sub_dict.get('txt', "未知")#空气指数  详细描述

            return (True, weather_data, lifestyle_data)


    def heweather_s6_analysis_data_from_db_and_server(self, cityid):
        weather_dict = {}
        lifestyle_dict = {}

        # key list remove 'id'
        weather_key_list = ['location', 'admin_area', 'cnty', 'update_time', 'forecast_days', 'aqi', 'now', 'forecast']
        lifestyle_key_list = ['comf_brf','comf_txt','drsg_brf','drsg_txt','flu_brf','flu_txt','sport_brf','sport_txt','trav_brf','trav_txt','uv_brf','uv_txt','cw_brf','cw_txt','air_brf','air_txt']

        # 从数据库的表heweather_s6_now_forecast中读取now、forecast、aqi数据集，以及lifestyle数据集
        weather_db_record = self.db.search_s6_heweather_data_record(cityid)
        lifestyle_db_record = self.db.search_s6_heweather_lifestyle_record(cityid)

        if weather_db_record != []:#数据库中已存在天气数据
            (ret, weather_dict, lifestyle_dict) = self.access_s6_heweather_all_data(cityid, True)
            if ret:#更新数据成功了，使用新数据插入数据库并返回给调用的client
                self.insert_or_update_s6_heweather_data_to_db(weather_dict, False)#update
                if lifestyle_db_record != []:#数据库中已存在lifestyle，则更新
                    self.insert_or_update_s6_heweather_lifestyle_to_db(lifestyle_dict, False)
                else:#数据库中不存在lifestyle，则插入
                    self.insert_or_update_s6_heweather_lifestyle_to_db(lifestyle_dict, True)
            else:#更新数据失败了，使用数据库中的老数据返回给调用的client
                if weather_db_record != []:
                    for i in range(0, len(weather_db_record[0])):
                        weather_dict[weather_key_list[i]] = weather_db_record[0][i]
                    weather_dict['id'] = cityid

                if lifestyle_db_record != []:
                    for i in range(0, len(lifestyle_db_record[0])):
                        lifestyle_dict[lifestyle_key_list[i]] = lifestyle_db_record[0][i]
                    lifestyle_dict['id'] = cityid
        else:#数据库中不存在天气数据
            (ret, weather_dict, lifestyle_dict) = self.access_s6_heweather_all_data(cityid, False)
            if ret:#获取数据成功了，将该数据插入数据库并返回给调用的client
                self.insert_or_update_s6_heweather_data_to_db(weather_dict, True)#insert

                if lifestyle_db_record != []:#数据库中已存在lifestyle，则更新
                    self.insert_or_update_s6_heweather_lifestyle_to_db(lifestyle_dict, False)
                else:#数据库中不存在lifestyle，则插入
                    self.insert_or_update_s6_heweather_lifestyle_to_db(lifestyle_dict, True)
            else:#更新数据失败了
                if lifestyle_db_record != []:
                    for i in range(0, len(lifestyle_db_record[0])):
                        lifestyle_dict[lifestyle_key_list[i]] = lifestyle_db_record[0][i]
                    lifestyle_dict['id'] = cityid

        return (weather_dict, lifestyle_dict)

    # 入口，返回所有天气数据，包括now、forecast、air和lifestyle
    def heweather_s6_all_data_api(self, cityid):
        '''
        对应于load和loads，dump的第一个参数是对象字典，第二个参数是文件对象，可以直接将转换后的json数据写入文件，dumps的第一个参数是对象字典，其余都是可选参数。dump和dumps的可选参数相同，这些参数都相当实用，现将用到的参数记录如下：
        ensure_ascii 默认为True，保证转换后的json字符串中全部是ascii字符，非ascii字符都会被转义。如果数据中存在中文或其他非ascii字符，最好将ensure_ascii设置为False，保证输出结果正常。
        indent 缩进，默认为None，没有缩进，设置为正整数时，输出的格式将按照indent指定的半角空格数缩进，相当实用。
        separators 设置分隔符，默认的分隔符是(',', ': ')，如果需要自定义json中的分隔符，例如调整冒号前后的空格数，可以按照(item_separator, key_separator)的形式设置。
        sort_keys 默认为False，设为True时，输出结果将按照字典中的key排序。

        loads()：将json数据转化成dict数据
        dumps()：将dict数据转化成json数据   sort_keys：根据key排序   indent：以4个空格缩进，输出阅读友好型    ensure_ascii: 可以序列化非ascii码（中文等）
        load()：读取json文件数据，转成dict数据
        dump()：将dict数据转化成json数据后写入json文件
        '''
        combination_dict = {}
        all_dict = {}
        weather_dict = {}
        lifestyle_dict = {}

        if cityid in (None, ''):
            combination_dict['weather'] = '';
            combination_dict['lifestyle'] = '';
            all_dict['KylinWeather'] = combination_dict
            all_json = json.dumps(all_dict, ensure_ascii=False, sort_keys=True, indent=4)
            return all_json

        (weather_dict, lifestyle_dict) = self.heweather_s6_analysis_data_from_db_and_server(cityid)

        combination_dict['weather'] = weather_dict;
        combination_dict['lifestyle'] = lifestyle_dict;
        all_dict['KylinWeather'] = combination_dict

        all_json = json.dumps(all_dict, ensure_ascii=False, sort_keys=True, indent=4)
        #print check_json_format("""{"a":1}""")#True
        #print check_json_format("""{'a':1}""")#False
        #print check_json_format({'a': 1})#False
        #print check_json_format(100)#False
        return all_json




    # 入口，返回城市列表的天气数据，包括城市id，城市名，温度和天气状态
    def heweather_s6_simple_data_api(self, cities_str):
        simple_dict = {}
        combination_dict = {}
        combination_dict['weather'] = ''
        citylist = []

        #TODO:判断城市id是否存在
        if cities_str.find(' '):
            line = cities_str.split(' ')
            for cityid in line:
                citylist.append(cityid)

        if len(citylist) == 0:
            simple_dict['KylinWeather'] = combination_dict
            simple_json = json.dumps(simple_dict, ensure_ascii=False, sort_keys=True, indent=4)
            return simple_json

        for i in range(0, len(citylist)):
            weather_dict = {}
            lifestyle_dict = {}
            if citylist[i] in (None, ''):
                continue

            (weather_dict, lifestyle_dict) = self.heweather_s6_analysis_data_from_db_and_server(citylist[i])
            if (isinstance(weather_dict, dict)):
                id_str = ''
                location_str = ''
                now_str = ''

                if weather_dict.has_key('id'):
                    id_str = weather_dict.get('id', citylist[i])
                else:
                    id_str = citylist[i]

                if weather_dict.has_key('location'):
                    location_str = weather_dict.get('location', '-')
                else:
                    location_str = '-'

                if weather_dict.has_key('now'):
                    now_str = weather_dict.get('now', '-,')
                else:
                    now_str = '-,'

                if now_str.endswith(','):
                    combination_str = now_str + "id=" + id_str + ",location=" + location_str
                else:
                    combination_str = now_str + ",id=" + id_str + ",location=" + location_str
                combination_dict['weather'] += "%s;" % combination_str

        simple_dict['KylinWeather'] = combination_dict

        simple_json = json.dumps(simple_dict, ensure_ascii=False, sort_keys=True, indent=4)
        return simple_json
        # 20200307---------------------------------------






    def access_cma_forecast3d_weather(self, cityid, insertflag):
        '''
        insertflag = True:insert db data
        insertflag = False:update db data
        '''
        forecast3d_dict = {}
        forecastdata = get_smartweather_forecast(cityid, "forecast3d")
        if forecastdata not in (False, None, {}, '', '[]', "['']"):
            for i in range(0, len(forecastdata)):
                if str(forecastdata.keys()[i]) == 'c':
                    for j in range(0, len(forecastdata.values()[i])):
                        forecast3d_dict[str(forecastdata.values()[i].keys()[j])] = str(forecastdata.values()[i].values()[j])
                elif str(forecastdata.keys()[i]) == 'f':
                    for k in range(0, len(forecastdata.values()[i])):
                        if str(forecastdata.values()[i].keys()[k]) == 'f0':
                            forecast3d_dict['f0'] = str(forecastdata.values()[i].values()[k])
                        if str(forecastdata.values()[i].keys()[k]) == 'f1':
                            list_len = len(forecastdata.values()[i].values()[k])
                            # print forecastdata.values()[i].values()[k]
                            for index in range(0, list_len):
                                for m in range(0, len(forecastdata.values()[i].values()[k][index])):
                                    forecast3d_dict[str(forecastdata.values()[i].values()[k][index].keys()[m])  + str(index)] = str(forecastdata.values()[i].values()[k][index].values()[m])

            now_date = get_local_format_time()
            if 'c16' not in forecast3d_dict.keys():
                forecast3d_dict['c16'] = '未知'
            if insertflag:
                self.db.insert_forecast3d_data(cityid,forecast3d_dict['c3'],forecast3d_dict['c5'],forecast3d_dict['c7'],forecast3d_dict['c9'],forecast3d_dict['c10'], \
                                             forecast3d_dict['c11'],forecast3d_dict['c12'],forecast3d_dict['c13'],forecast3d_dict['c14'],forecast3d_dict['c15'], \
                                             forecast3d_dict['c16'],forecast3d_dict['c17'],forecast3d_dict['f0'],now_date,"zh_CN",forecast3d_dict['fi0'], \
                                             forecast3d_dict['fa0'],forecast3d_dict['fb0'],forecast3d_dict['fc0'],forecast3d_dict['fd0'],forecast3d_dict['fe0'], \
                                             forecast3d_dict['ff0'],forecast3d_dict['fg0'],forecast3d_dict['fh0'],forecast3d_dict['fi1'],forecast3d_dict['fa1'], \
                                             forecast3d_dict['fb1'],forecast3d_dict['fc1'],forecast3d_dict['fd1'],forecast3d_dict['fe1'],forecast3d_dict['ff1'], \
                                             forecast3d_dict['fg1'],forecast3d_dict['fh1'],forecast3d_dict['fi2'],forecast3d_dict['fa2'],forecast3d_dict['fb2'], \
                                             forecast3d_dict['fc2'],forecast3d_dict['fd2'],forecast3d_dict['fe2'],forecast3d_dict['ff2'],forecast3d_dict['fg2'], \
                                             forecast3d_dict['fh2'],forecast3d_dict['c2'],forecast3d_dict['c4'],forecast3d_dict['c6'],forecast3d_dict['c8'])
            else:
                self.db.update_forecast3d_data(forecast3d_dict['c13'],forecast3d_dict['c14'],forecast3d_dict['c15'], \
                                             forecast3d_dict['c16'],forecast3d_dict['c17'],forecast3d_dict['f0'],now_date,forecast3d_dict['fi0'], \
                                             forecast3d_dict['fa0'],forecast3d_dict['fb0'],forecast3d_dict['fc0'],forecast3d_dict['fd0'],forecast3d_dict['fe0'], \
                                             forecast3d_dict['ff0'],forecast3d_dict['fg0'],forecast3d_dict['fh0'],forecast3d_dict['fi1'],forecast3d_dict['fa1'], \
                                             forecast3d_dict['fb1'],forecast3d_dict['fc1'],forecast3d_dict['fd1'],forecast3d_dict['fe1'],forecast3d_dict['ff1'], \
                                             forecast3d_dict['fg1'],forecast3d_dict['fh1'],forecast3d_dict['fi2'],forecast3d_dict['fa2'],forecast3d_dict['fb2'], \
                                             forecast3d_dict['fc2'],forecast3d_dict['fd2'],forecast3d_dict['fe2'],forecast3d_dict['ff2'],forecast3d_dict['fg2'], \
                                             forecast3d_dict['fh2'],cityid)
        return forecast3d_dict


    def get_cma_forecast3d_weather(self, cityid):
        '''
        如果没有数据，则直接获取后插入数据库中
        如果有数据，则比较时间，如果日期不同，则重新获取后更新数据库；如果日期相同，小时不同，则重写获取后更新数据库；否则使用数据库中数据
        '''
        forecast3d_dict = {}
        key_list = ['c3','c5','c7','c9','c10','c11','c12','c13','c14','c15','c16','c17','f0','fi0','fa0','fb0','fc0','fd0','fe0','ff0','fg0','fh0','fi1','fa1','fb1','fc1','fd1','fe1','ff1','fg1','fh1','fi2','fa2','fb2','fc2','fd2','fe2','ff2','fg2','fh2','c2','c4','c6','c8']
        db_record = self.db.search_forecast3d_record(cityid)
        if db_record != []:#update data
            print 'a1111'
            db_time_list = self.db.search_forecast3d_record_update_time(cityid)
            db_time = None
            if len(db_time_list) >= 1:
                db_time = db_time_list[0][0]
            now_date = get_local_format_time()
            # compare now_time with db_time ,when they are different, then access weather data again
            db_time_list = db_time.split(" ")
            now_date_list = now_date.split(" ")
            # compare now_time with db_time ,when they are different, then access weather data again
            again = False
            if db_time_list[0] != now_date_list[0]:#different day
                again = True
            else:# same day
                if db_time_list[1].split(":")[0] == now_date_list[1].split(":")[0]:#same day and same hour
                    again = False
                else:#same day and different hour
                    again = True
            if again:
                again = False
                forecast3d_dict = self.access_cma_forecast3d_weather(cityid, False)#update
                # if update failed, then use db data to show
                if forecast3d_dict == {}:
                    if len(db_record) >= 1:
                        for i in range(0, len(db_record[0])):
                            # print db_record[0][i]
                            forecast3d_dict[key_list[i]] = db_record[0][i]
            else:
                if len(db_record) >= 1:
                    for i in range(0, len(db_record[0])):
                        forecast3d_dict[key_list[i]] = db_record[0][i]
        else:#insert data
            forecast3d_dict = self.access_cma_forecast3d_weather(cityid, True)#insert
        return forecast3d_dict

    # Now api
    def access_cma_forecast6d_weather(self, cityid, insertflag):
        '''
        insertflag = True:insert db data
        insertflag = False:update db data
        '''
        # fp2 = open("/tmp/read2.txt", "w")
        # print >> fp2, "--------------"
        forecast6d_dict = {}
        forecast6d_dict = get_open_forecast6d_weather(cityid)
        if forecast6d_dict not in (False, None, {}, '', '[]', "['']"):
            now_date = get_local_format_time()
            if insertflag:
                #print 'insert.....'
                self.db.insert_forecast6d_data(cityid,forecast6d_dict['city'],forecast6d_dict['city_en'],forecast6d_dict['date_y'],forecast6d_dict['date'],forecast6d_dict['week'],forecast6d_dict['fchh'],now_date, \
                         forecast6d_dict['temp1'],forecast6d_dict['temp2'],forecast6d_dict['temp3'],forecast6d_dict['temp4'],forecast6d_dict['temp5'],forecast6d_dict['temp6'], \
                         forecast6d_dict['tempF1'],forecast6d_dict['tempF2'],forecast6d_dict['tempF3'],forecast6d_dict['tempF4'],forecast6d_dict['tempF5'],forecast6d_dict['tempF6'], \
                         forecast6d_dict['weather1'],forecast6d_dict['weather2'],forecast6d_dict['weather3'],forecast6d_dict['weather4'],forecast6d_dict['weather5'],forecast6d_dict['weather6'], \
                         forecast6d_dict['img1'],forecast6d_dict['img2'],forecast6d_dict['img3'],forecast6d_dict['img4'],forecast6d_dict['img5'],forecast6d_dict['img6'], \
                         forecast6d_dict['img7'],forecast6d_dict['img8'],forecast6d_dict['img9'],forecast6d_dict['img10'],forecast6d_dict['img11'],forecast6d_dict['img12'], \
                         forecast6d_dict['img_single'],forecast6d_dict['img_title_single'],forecast6d_dict['img_title1'],forecast6d_dict['img_title2'],forecast6d_dict['img_title3'],forecast6d_dict['img_title4'],forecast6d_dict['img_title5'],forecast6d_dict['img_title6'], \
                         forecast6d_dict['img_title7'],forecast6d_dict['img_title8'],forecast6d_dict['img_title9'],forecast6d_dict['img_title10'],forecast6d_dict['img_title11'],forecast6d_dict['img_title12'], \
                         forecast6d_dict['wind1'],forecast6d_dict['wind2'],forecast6d_dict['wind3'],forecast6d_dict['wind4'],forecast6d_dict['wind5'],forecast6d_dict['wind6'], \
                         forecast6d_dict['fx1'],forecast6d_dict['fx2'],forecast6d_dict['fl1'],forecast6d_dict['fl2'],forecast6d_dict['fl3'],forecast6d_dict['fl4'],forecast6d_dict['fl5'],forecast6d_dict['fl6'], \
                         forecast6d_dict['index_clothes'],forecast6d_dict['index_d'],forecast6d_dict['index_uv'],forecast6d_dict['index_xc'],forecast6d_dict['index_tr'],forecast6d_dict['index_co'],forecast6d_dict['index_cl'],forecast6d_dict['index_ls'],forecast6d_dict['index_ag'])
            else:
                #print 'update forecast...'
                self.db.update_forecast6d_data(forecast6d_dict['date_y'],forecast6d_dict['date'],forecast6d_dict['week'],forecast6d_dict['fchh'],now_date, \
                         forecast6d_dict['temp1'],forecast6d_dict['temp2'],forecast6d_dict['temp3'],forecast6d_dict['temp4'],forecast6d_dict['temp5'],forecast6d_dict['temp6'], \
                         forecast6d_dict['tempF1'],forecast6d_dict['tempF2'],forecast6d_dict['tempF3'],forecast6d_dict['tempF4'],forecast6d_dict['tempF5'],forecast6d_dict['tempF6'], \
                         forecast6d_dict['weather1'],forecast6d_dict['weather2'],forecast6d_dict['weather3'],forecast6d_dict['weather4'],forecast6d_dict['weather5'],forecast6d_dict['weather6'], \
                         forecast6d_dict['img1'],forecast6d_dict['img2'],forecast6d_dict['img3'],forecast6d_dict['img4'],forecast6d_dict['img5'],forecast6d_dict['img6'], \
                         forecast6d_dict['img7'],forecast6d_dict['img8'],forecast6d_dict['img9'],forecast6d_dict['img10'],forecast6d_dict['img11'],forecast6d_dict['img12'], \
                         forecast6d_dict['img_single'],forecast6d_dict['img_title_single'],forecast6d_dict['img_title1'],forecast6d_dict['img_title2'],forecast6d_dict['img_title3'],forecast6d_dict['img_title4'],forecast6d_dict['img_title5'],forecast6d_dict['img_title6'], \
                         forecast6d_dict['img_title7'],forecast6d_dict['img_title8'],forecast6d_dict['img_title9'],forecast6d_dict['img_title10'],forecast6d_dict['img_title11'],forecast6d_dict['img_title12'], \
                         forecast6d_dict['wind1'],forecast6d_dict['wind2'],forecast6d_dict['wind3'],forecast6d_dict['wind4'],forecast6d_dict['wind5'],forecast6d_dict['wind6'], \
                         forecast6d_dict['fx1'],forecast6d_dict['fx2'],forecast6d_dict['fl1'],forecast6d_dict['fl2'],forecast6d_dict['fl3'],forecast6d_dict['fl4'],forecast6d_dict['fl5'],forecast6d_dict['fl6'], \
                         forecast6d_dict['index_clothes'],forecast6d_dict['index_d'],forecast6d_dict['index_uv'],forecast6d_dict['index_xc'],forecast6d_dict['index_tr'],forecast6d_dict['index_co'],forecast6d_dict['index_cl'],forecast6d_dict['index_ls'],forecast6d_dict['index_ag'],cityid)
        # fp2.close()
            #print 'get_or_update....'
            #print forecast6d_dict
        else:
            print 'get_smartweather_forecast failed....'
        return forecast6d_dict


    def get_cma_forecast6d_weather(self, cityid):
        '''
        如果没有数据，则直接获取后插入数据库中
        如果有数据，则比较时间，如果日期不同，则重新获取后更新数据库；如果日期相同，小时不同，则重写获取后更新数据库；否则使用数据库中数据
        '''
        # fp1 = open("/tmp/read.txt", "w")
        # print >> fp1, "--------------"
        forecast6d_dict = {}
        key_list = ['city', 'date_y', 'date', 'week', 'fchh', 'temp1', 'temp2', 'temp3', 'temp4', 'temp5', 'temp6', \
        'weather1', 'weather2', 'weather3', 'weather4', 'weather5', 'weather6', \
        'img1', 'img2', 'img3', 'img4', 'img5', 'img6', 'img7', 'img8', 'img9', 'img10', 'img11', 'img12',\
        'wind1', 'wind2', 'wind3', 'wind4', 'wind5', 'wind6', \
        'index_clothes', 'index_d', 'index_uv', 'index_xc', 'index_tr', 'index_co', 'index_cl', 'index_ls', 'index_ag']
        db_record = self.db.search_forecast6d_record(cityid)
        print '777---------------------------'
        print db_record
        # print db_record
        if db_record != []:#update data
            db_time_list = self.db.search_forecast6d_record_update_time(cityid)
            db_time = None
            if len(db_time_list) >= 1:
                db_time = db_time_list[0][0]
            # db_time = '2014-05-07 13:51:30'
            now_date = get_local_format_time()
            # compare now_time with db_time ,when they are different, then access weather data again
            db_time_list = db_time.split(" ")
            now_date_list = now_date.split(" ")
            # compare now_time with db_time ,when they are different, then access weather data again
            again = False
            if db_time_list[0] != now_date_list[0]:#different day
                again = True
            else:# same day
                if db_time_list[1].split(":")[0] == now_date_list[1].split(":")[0]:#same day and same hour
                    again = False
                else:#same day and different hour
                    again = True
            if again:
                again = False
                forecast6d_dict = self.access_cma_forecast6d_weather(cityid, False)#update
                # if update failed, then use db data to show
                if forecast6d_dict == {}:
                    if len(db_record) >= 1:
                        for i in range(0, len(db_record[0])):
                            # print db_record[0][i]
                            forecast6d_dict[key_list[i]] = db_record[0][i]
            else:
                if len(db_record) >= 1:
                    for i in range(0, len(db_record[0])):
                        # print 'a1---------------------------'
                        # print key_list[i]
                        forecast6d_dict[key_list[i]] = db_record[0][i]
        else:#insert data
            forecast6d_dict = self.access_cma_forecast6d_weather(cityid, True)#insert
        # fp1.close()
        print 'real dict ->'
        print forecast6d_dict
        return forecast6d_dict

    # 2018 和风天气api s6版本：client的主界面切换城市时从server端获取数据, called by get_cma_observe_weather
    def access_cma_current_weather(self, cityid, cityname, insertflag):
        '''
        insertflag = True:insert db data
        insertflag = False:update db data
        '''
        weather_dict = {}
        # get pm 2.5
        pm = get_pm(str(cityname))
        # get current weather
        weather_dict = get_open_weather(cityid)
        if weather_dict not in (False, None, {}, '', '[]', "['']"):
            if 'error' in pm or pm == False:
                weather_dict['aqi'] = '无数据'#'N/A'
            else:
                weather_dict['aqi'] = pm['quality'] + '(' + str(pm['aqi']) + ')'
            now_date = get_local_format_time()
            if insertflag:
                self.db.insert_observe_data(cityid,weather_dict['city'],weather_dict['ptime'],weather_dict['time'],now_date,weather_dict['WD'],weather_dict['WS'],weather_dict['SD'],weather_dict['weather'],weather_dict['img1'],weather_dict['img2'],weather_dict['temp'],weather_dict['temp1'],weather_dict['temp2'],weather_dict['aqi'])
            else:
                self.db.update_observe_data(weather_dict['ptime'],weather_dict['time'],now_date,weather_dict['WD'],weather_dict['WS'],weather_dict['SD'],weather_dict['weather'],weather_dict['img1'],weather_dict['img2'],weather_dict['temp'],weather_dict['temp1'],weather_dict['temp2'],weather_dict['aqi'],cityid)
        return weather_dict

    # 2018 和风天气api s6版本：client的主界面切换城市时从server端获取数据
    def get_cma_observe_weather(self, cityid, cityname):
        '''
        如果没有数据，则直接获取后插入数据库中
        如果有数据，则比较时间，如果日期不同，则重新获取后更新数据库；如果日期相同，小时不同，则重写获取后更新数据库；否则使用数据库中数据
        '''
        weather_dict = {}
        key_list = ['city', 'ptime', 'time', 'WD', 'WS', 'SD', 'weather', 'img1', 'img2', 'temp', 'temp1', 'temp2', 'aqi']
        db_record = self.db.search_observe_record(cityid)
        if db_record != []:#update data
            db_time_list = self.db.search_observe_record_update_time(cityid)
            db_time = None
            if len(db_time_list) >= 1:
                db_time = db_time_list[0][0]
            # db_time = '2014-05-07 13:51:30'
            now_date = get_local_format_time()
            db_time_list = db_time.split(" ")
            now_date_list = now_date.split(" ")
            # compare now_time with db_time ,when they are different, then access weather data again
            again = False
            if db_time_list[0] != now_date_list[0]:#different day
                again = True
            else:# same day
                if db_time_list[1].split(":")[0] == now_date_list[1].split(":")[0]:#same day and same hour
                    again = False
                else:#same day and different hour
                    again = True
            if again:
                again = False
                weather_dict = self.access_cma_current_weather(cityid, cityname, False)#update
                # if update failed, then use db data to show
                if weather_dict == {}:
                    if len(db_record) >= 1:
                        for i in range(0, len(db_record[0])):
                            weather_dict[key_list[i]] = db_record[0][i]
            else:
                if len(db_record) >= 1:
                    for i in range(0, len(db_record[0])):
                        weather_dict[key_list[i]] = db_record[0][i]
        else:#insert data
            weather_dict = self.access_cma_current_weather(cityid, cityname, True)#insert

        return weather_dict


if __name__ == "__main__":
    app = AppServer()
#    aa = app.get_cma_forecast6d_weather('101071205')
#    dict_data = app.get_heweather_observe_weather("101250101")
#    print "dict_data=",dict_data
