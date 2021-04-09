#!/usr/bin/python
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


#20170626
#sudo apt-get install python-mysqldb
#mysql -u root -p
#create database weatherdb;
#python database.py
#use weatherdb;
#show tables;
#desc heweather_air;
#delete from heweather_observe where id = '101250101';

#删除表   drop table 表名
#清空表   delete from 表名
import os, sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb as kdb
import json
import urllib2, urllib
import time

#HEWEATHER_AIR_NOW_URL = 'https://free-api.heweather.com/s6/air/now?location=CN%s&key=a3c0a9ef33b44257a6c8f2643a42e5b3'
#HEWEATHER_WEATHER_URL = 'https://free-api.heweather.com/s6/weather?location=CN%s&key=40cc3ec6bbbf4de6a04029e207c986fd'


#HEWEATHER_AIR_NOW_URL = 'https://free-api.heweather.net/s6/air/now?location=CN%s&key=a3c0a9ef33b44257a6c8f2643a42e5b3'
#HEWEATHER_WEATHER_URL = 'https://free-api.heweather.net/s6/weather?location=CN%s&key=40cc3ec6bbbf4de6a04029e207c986fd'

#email: lixiang@kylinos.cn      phone: 15116165128
HEWEATHER_AIR_NOW_URL = 'https://free-api.heweather.net/s6/air/now?location=CN%s&key=9d230098dd0546c5bfd8e55ae4499f18'
HEWEATHER_WEATHER_URL = 'https://free-api.heweather.net/s6/weather?location=CN%s&key=9d230098dd0546c5bfd8e55ae4499f18'

#https://free-api.heweather.net/s6/air/now?location=CN101250101&key=a3c0a9ef33b44257a6c8f2643a42e5b3
#https://free-api.heweather.net/s6/weather?location=CN101250101&key=40cc3ec6bbbf4de6a04029e207c986fd
#https://free-api.heweather.net/s6/weather?location=CN101250101&key=4ff2e595e593439380e52d2519523d0a

CREATE_S6_HEWEATHER_NOW_AND_FORECAST = "CREATE TABLE IF NOT EXISTS heweather_s6_now_forecast (id varchar(32) primary key not null,location VARCHAR(64), \
                admin_area VARCHAR(64),cnty VARCHAR(32),update_time VARCHAR(32),forecast_days INTEGER, \
                aqi VARCHAR(256),aqi_station VARCHAR(4096),now VARCHAR(512),forecast VARCHAR(4096))ENGINE = INNODB DEFAULT CHARSET=utf8 COLLATE=utf8_bin"
INSERT_S6_HEWEATHER_NOW_AND_FORECAST = "insert into heweather_s6_now_forecast (id,location,admin_area,cnty,update_time,forecast_days,aqi,now,forecast) values \
            ('%s','%s','%s','%s','%s','%d','%s','%s','%s')"
QUERY_S6_HEWEATHER_NOW_AND_FORECAST = "select location,admin_area,cnty,update_time,forecast_days,aqi,now,forecast \
             from heweather_s6_now_forecast where id='%s'"
QUERY_S6_HEWEATHER_TIME = "select update_time from heweather_s6_now_forecast where id='%s'"
UPDATE_S6_HEWEATHER_NOW_AND_FORECAST = "update heweather_s6_now_forecast set update_time='%s',forecast_days='%d',aqi='%s',now='%s',forecast='%s' \
              where id='%s'"

CREATE_S6_HEWEATHER_LIFESTYLE = "CREATE TABLE IF NOT EXISTS heweather_s6_lifestyle (id VARCHAR(32) primary key not null, \
            comf_brf VARCHAR(32),comf_txt VARCHAR(256),drsg_brf VARCHAR(32),drsg_txt VARCHAR(256), \
            flu_brf VARCHAR(32),flu_txt VARCHAR(256),sport_brf VARCHAR(32),sport_txt VARCHAR(256), \
            trav_brf VARCHAR(32),trav_txt VARCHAR(256),uv_brf VARCHAR(32),uv_txt VARCHAR(256), \
            cw_brf VARCHAR(32),cw_txt VARCHAR(256),air_brf VARCHAR(32),air_txt VARCHAR(256))ENGINE = INNODB DEFAULT CHARSET=utf8 COLLATE=utf8_bin"
INSERT_S6_HEWEATHER_LIFESTYLE = "insert into heweather_s6_lifestyle (id,comf_brf,comf_txt,drsg_brf,drsg_txt,flu_brf,flu_txt,sport_brf,sport_txt,trav_brf,trav_txt,uv_brf,uv_txt,cw_brf,cw_txt,air_brf,air_txt) values \
            ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
QUERY_S6_HEWEATHER_LIFESTYLE = "select comf_brf,comf_txt,drsg_brf,drsg_txt,flu_brf,flu_txt,sport_brf,sport_txt,trav_brf,trav_txt,uv_brf,uv_txt,cw_brf,cw_txt,air_brf,air_txt \
             from heweather_s6_lifestyle where id='%s'"
UPDATE_S6_HEWEATHER_LIFESTYLE = "update heweather_s6_lifestyle set comf_brf='%s',comf_txt='%s',drsg_brf='%s',drsg_txt='%s',flu_brf='%s',flu_txt='%s',sport_brf='%s',sport_txt='%s',trav_brf='%s',trav_txt='%s',uv_brf='%s',uv_txt='%s',cw_brf='%s',cw_txt='%s',air_brf='%s',air_txt='%s' \
              where id='%s'"


def read_json_from_url(url):
    # returns weather info by json_string
    request = urllib2.Request(url, headers={'User-Agent' : 'Magic Browser'})
    f = urllib2.urlopen(request)
    json_string = f.read()
    f.close()
    return json_string


def get_local_format_time():
    '''
    year-month-day hour:minute:second
    2014-05-07 13:51:30
    '''
    local_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return local_date

class DataBase:
    def __init__(self):

        #建立和数据库系统的连接
        try:
            self.connect = kdb.connect(host='localhost', user='root', passwd='123123', charset='utf8')#, db='weatherdb'
            #获取操作游标
            self.cursor = self.connect.cursor()
            #self.cursor.execute('create database if not exists weatherdb')
            self.connect.select_db('weatherdb')
        except kdb.Error,e:
            print 'Mysql error %d:%s' %(e.args[0],e.args[1])

    # ------------------------------20200307------------------------------
    def init_s6_heweather_now_and_forecast_table(self):
        self.cursor.execute(CREATE_S6_HEWEATHER_NOW_AND_FORECAST)

    def init_s6_heweather_lifestyle_table(self):
        self.cursor.execute(CREATE_S6_HEWEATHER_LIFESTYLE)

    def search_s6_heweather_data_record(self, id):
        self.cursor.execute(QUERY_S6_HEWEATHER_NOW_AND_FORECAST % (id))
        res = self.cursor.fetchall()
        if len(res) == 0:
            return []
        else:
            return res

    def search_s6_heweather_update_time(self, id):
        self.cursor.execute(QUERY_S6_HEWEATHER_TIME % (id))
        res = self.cursor.fetchall()
        if len(res) == 0:
            return []
        else:
            return res

    def insert_s6_heweather_weather_data(self,id,location,admin_area,cnty,update_time,forecast_days,aqi,now,forecast):
        self.cursor.execute(INSERT_S6_HEWEATHER_NOW_AND_FORECAST % (id,str(location),str(admin_area),str(cnty),str(update_time),int(forecast_days),str(aqi),str(now),str(forecast)))
        self.connect.commit()

    def update_s6_heweather_weather_data(self,id,update_time,forecast_days,aqi,now,forecast):
        self.cursor.execute(UPDATE_S6_HEWEATHER_NOW_AND_FORECAST % (str(update_time),int(forecast_days),str(aqi),str(now),str(forecast),str(id)))
        self.connect.commit()

    def search_s6_heweather_lifestyle_record(self, id):
        self.cursor.execute(QUERY_S6_HEWEATHER_LIFESTYLE % (id))
        res = self.cursor.fetchall()
        if len(res) == 0:
            return []
        else:
            return res

    def insert_s6_heweather_lifestyle(self,id,comf_brf,comf_txt,drsg_brf,drsg_txt,flu_brf,flu_txt,sport_brf,sport_txt,trav_brf,trav_txt,uv_brf,uv_txt,cw_brf,cw_txt,air_brf,air_txt):
        self.cursor.execute(INSERT_S6_HEWEATHER_LIFESTYLE % (id,comf_brf,comf_txt,drsg_brf,drsg_txt,flu_brf,flu_txt,sport_brf,sport_txt,trav_brf,trav_txt,uv_brf,uv_txt,cw_brf,cw_txt,air_brf,air_txt))
        self.connect.commit()

    def update_s6_heweather_lifestyle(self,comf_brf,comf_txt,drsg_brf,drsg_txt,flu_brf,flu_txt,sport_brf,sport_txt,trav_brf,trav_txt,uv_brf,uv_txt,cw_brf,cw_txt,air_brf,air_txt,id):
        self.cursor.execute(UPDATE_S6_HEWEATHER_LIFESTYLE % (comf_brf,comf_txt,drsg_brf,drsg_txt,flu_brf,flu_txt,sport_brf,sport_txt,trav_brf,trav_txt,uv_brf,uv_txt,cw_brf,cw_txt,air_brf,air_txt,id))
        self.connect.commit()
    # ------------------------------20200307------------------------------



class AppServer:
    def __init__(self):
        self.db = DataBase()

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
#    def access_s6_heweather_all_data(self, cityid, readtime):
#        needRefresh = False
#        aqi_url = HEWEATHER_AIR_NOW_URL % (cityid)
#        weather_url = HEWEATHER_WEATHER_URL % (cityid)
#        weather_data = {}
#        lifestyle_data = {}
#        weather_key_list = ['id', 'location', 'admin_area', 'cnty', 'update_time', 'forecast_days', 'aqi', 'now', 'forecast']
#        lifestyle_key_list = ['id','comf_brf','comf_txt','drsg_brf','drsg_txt','flu_brf','flu_txt','sport_brf','sport_txt','trav_brf','trav_txt','uv_brf','uv_txt','cw_brf','cw_txt','air_brf','air_txt']

#        # init value
#        for i in range(0, len(weather_key_list)):
#            weather_data[weather_key_list[i]] = "-"
#        weather_data['forecast_days'] = 0
#        weather_data['id'] = cityid
#        weather_data['update_time'] = "2020-03-08 22:00"

#        for i in range(0, len(lifestyle_key_list)):
#            lifestyle_data[lifestyle_key_list[i]] = "-"
#        lifestyle_data['id'] = cityid

#        if readtime:
#            #从数据库中读取记录的时间
#            now_date = str(get_local_format_time())
#            db_time = None
#            db_time_list = self.db.search_s6_heweather_update_time(cityid)
#            if db_time_list in (False, None, [], '', '[]', "['']"):#数据库中没有找到更新的时间，重新读取数据
#                needRefresh = True
#            else:
#                db_time = db_time_list[0][0]
#                if db_time is not None:#2018-08-29 08:45
#                    db_time_list = db_time.split(" ")
#                    now_date_list = now_date.split(" ")
#                    # compare now_time with db_time ,when they are different, then access weather data again
#                    if db_time_list[0] != now_date_list[0]:#different day
#                        needRefresh = True
#                    else:# same day
#                        dbHour = int(db_time_list[1].split(":")[0])#16
#                        nowHour = int(now_date_list[1].split(":")[0])#19
#                        if abs(nowHour - dbHour) >= 3:
#                            needRefresh = True
#        else:
#            needRefresh = True


#        if needRefresh == False:
#            return (False, weather_data, lifestyle_data)
#        else:
#            try:
#                json_aqi_string = read_json_from_url(aqi_url)
#                parsed_aqi_json = json.loads(json_aqi_string)

#                json_string = read_json_from_url(weather_url)
#                parsed_json = json.loads(json_string)
#            except Exception as e:
#                print "read json error:", str(e)
#                return (False, weather_data, lifestyle_data)

#            tmp_aqi_list = parsed_aqi_json['HeWeather6'][0]
#            if tmp_aqi_list:
#                if tmp_aqi_list['status'] == "ok":
#                    if tmp_aqi_list.has_key('air_now_city'):
#                        aqi_dict = tmp_aqi_list['air_now_city']
#                        if (isinstance(aqi_dict, dict)):
#                            weather_data['aqi'] = ''
#                            for k,v in aqi_dict.items():
#                                aqi_tmp_value = k + "=" + v + ","
#                                weather_data['aqi'] += aqi_tmp_value

#            tmp_list = parsed_json['HeWeather6'][0]
#            if tmp_list:
#                if tmp_list['status'] == "ok":
#                    # basic
#                    if tmp_list.has_key('basic'):
#                        basic_dict = tmp_list['basic']
#                        if (isinstance(basic_dict, dict)):
#                            if basic_dict.has_key('location'):
#                                weather_data['location'] = basic_dict.get('location', "-")
#                            if basic_dict.has_key('admin_area'):
#                                weather_data['admin_area'] = basic_dict.get('admin_area', "-")
#                            if basic_dict.has_key('cnty'):
#                                weather_data['cnty'] = basic_dict.get('cnty', "-")

#                    # update
#                    if tmp_list.has_key('update'):
#                        time_dict = tmp_list['update']
#                        if (isinstance(time_dict, dict)):
#                            if time_dict.has_key('loc'):
#                                weather_data['update_time'] = time_dict.get('loc', "-")

#                    # now
#                    if tmp_list.has_key('now'):
#                        now_dict = tmp_list.get('now', "")
#                        if (isinstance(now_dict, dict)):
#                            weather_data['now'] = ''
#                            for k,v in now_dict.items():
#                                now_tmp_value = k + "=" + v + ","
#                                weather_data['now'] += now_tmp_value

#                    # daily_forecast
#                    if tmp_list.has_key('daily_forecast'):
#                        daily_forecast = tmp_list.get('daily_forecast', "")
#                        forecast_len = len(daily_forecast)#3 or 7 days forecast
#                        weather_data['forecast_days'] = forecast_len
#                        weather_data['forecast'] = ''
#                        for i in range(forecast_len):
#                            data_dict = daily_forecast[i]
#                            if (isinstance(data_dict, dict)):
#                                forecast_value = ''
#                                for k,v in data_dict.items():
#                                    forecast_tmp_value = k + "=" + v + ","
#                                    forecast_value += forecast_tmp_value
#                                weather_data['forecast'] += "%s;" % forecast_value

#                    # lifestyle
#                    if tmp_list.has_key('lifestyle'):
#                        suggestion_dict = tmp_list['lifestyle']
#                        for i in range(len(suggestion_dict)):
#                            sub_dict = suggestion_dict[i]
#                            if (isinstance(sub_dict, dict)):
#                                if sub_dict.get('type', "") == "comf":
#                                    lifestyle_data['comf_brf'] = sub_dict.get('brf', "未知")#舒适度指数  简介
#                                    lifestyle_data['comf_txt'] = sub_dict.get('txt', "未知")#舒适度指数  详细描述
#                                elif sub_dict.get('type', "") == "drsg":
#                                    lifestyle_data['drsg_brf'] = sub_dict.get('brf', "未知")#穿衣指数  简介
#                                    lifestyle_data['drsg_txt'] = sub_dict.get('txt', "未知")#穿衣指数  详细描述
#                                elif sub_dict.get('type', "") == "flu":
#                                    lifestyle_data['flu_brf'] = sub_dict.get('brf', "未知")#感冒指数  简介
#                                    lifestyle_data['flu_txt'] = sub_dict.get('txt', "未知")#感冒指数  详细描述
#                                elif sub_dict.get('type', "") == "sport":
#                                    lifestyle_data['sport_brf'] = sub_dict.get('brf', "未知")#运动指数  简介
#                                    lifestyle_data['sport_txt'] = sub_dict.get('txt', "未知")#运动指数  详细描述
#                                elif sub_dict.get('type', "") == "trav":
#                                    lifestyle_data['trav_brf'] = sub_dict.get('brf', "未知")#旅游指数  简介
#                                    lifestyle_data['trav_txt'] = sub_dict.get('txt', "未知")#旅游指数  详细描述
#                                elif sub_dict.get('type', "") == "uv":
#                                    lifestyle_data['uv_brf'] = sub_dict.get('brf', "未知")#紫外线指数  简介
#                                    lifestyle_data['uv_txt'] = sub_dict.get('txt', "未知")#紫外线指数  详细描述
#                                elif sub_dict.get('type', "") == "cw":
#                                    lifestyle_data['cw_brf'] = sub_dict.get('brf', "未知")#洗车指数  简介
#                                    lifestyle_data['cw_txt'] = sub_dict.get('txt', "未知")#洗车指数  详细描述
#                                elif sub_dict.get('type', "") == "air":
#                                    lifestyle_data['air_brf'] = sub_dict.get('brf', "未知")#空气指数  简介
#                                    lifestyle_data['air_txt'] = sub_dict.get('txt', "未知")#空气指数  详细描述

#            return (True, weather_data, lifestyle_data)

#    # 入口，返回所有天气数据，包括now、forecast、air和lifestyle
#    def heweather_s6_all_data_api(self, cityid):
#        '''
#        对应于load和loads，dump的第一个参数是对象字典，第二个参数是文件对象，可以直接将转换后的json数据写入文件，dumps的第一个参数是对象字典，其余都是可选参数。dump和dumps的可选参数相同，这些参数都相当实用，现将用到的参数记录如下：
#        ensure_ascii 默认为True，保证转换后的json字符串中全部是ascii字符，非ascii字符都会被转义。如果数据中存在中文或其他非ascii字符，最好将ensure_ascii设置为False，保证输出结果正常。
#        indent 缩进，默认为None，没有缩进，设置为正整数时，输出的格式将按照indent指定的半角空格数缩进，相当实用。
#        separators 设置分隔符，默认的分隔符是(',', ': ')，如果需要自定义json中的分隔符，例如调整冒号前后的空格数，可以按照(item_separator, key_separator)的形式设置。
#        sort_keys 默认为False，设为True时，输出结果将按照字典中的key排序。

#        loads()：将json数据转化成dict数据
#        dumps()：将dict数据转化成json数据   sort_keys：根据key排序   indent：以4个空格缩进，输出阅读友好型    ensure_ascii: 可以序列化非ascii码（中文等）
#        load()：读取json文件数据，转成dict数据
#        dump()：将dict数据转化成json数据后写入json文件
#        '''
#        combination_dict = {}
#        all_dict = {}
#        weather_dict = {}
#        lifestyle_dict = {}
#        # key list remove 'id'
#        weather_key_list = ['location', 'admin_area', 'cnty', 'update_time', 'forecast_days', 'aqi', 'now', 'forecast']
#        lifestyle_key_list = ['comf_brf','comf_txt','drsg_brf','drsg_txt','flu_brf','flu_txt','sport_brf','sport_txt','trav_brf','trav_txt','uv_brf','uv_txt','cw_brf','cw_txt','air_brf','air_txt']

#        # 从数据库的表heweather_s6_now_forecast中读取now、forecast、aqi数据集，以及lifestyle数据集
#        weather_db_record = self.db.search_s6_heweather_data_record(cityid)
#        lifestyle_db_record = self.db.search_s6_heweather_lifestyle_record(cityid)

#        if weather_db_record != []:#数据库中已存在天气数据
#            (ret, weather_dict, lifestyle_dict) = self.access_s6_heweather_all_data(cityid, True)
#            if ret:#更新数据成功了，使用新数据插入数据库并返回给调用的client
#                self.insert_or_update_s6_heweather_data_to_db(weather_dict, False)#update
#                if lifestyle_db_record != []:#数据库中已存在lifestyle，则更新
#                    self.insert_or_update_s6_heweather_lifestyle_to_db(lifestyle_dict, False)
#                else:#数据库中不存在lifestyle，则插入
#                    self.insert_or_update_s6_heweather_lifestyle_to_db(lifestyle_dict, True)
#            else:#更新数据失败了，使用数据库中的老数据返回给调用的client
#                for i in range(0, len(weather_db_record[0])):
#                    weather_dict[weather_key_list[i]] = weather_db_record[0][i]
#                weather_dict['id'] = cityid

#                for i in range(0, len(lifestyle_db_record[0])):
#                    lifestyle_dict[lifestyle_key_list[i]] = lifestyle_db_record[0][i]
#                lifestyle_dict['id'] = cityid
#        else:#数据库中不存在天气数据
#            (ret, weather_dict, lifestyle_dict) = self.access_s6_heweather_all_data(cityid, False)
#            if ret:#获取数据成功了，将该数据插入数据库并返回给调用的client
#                self.insert_or_update_s6_heweather_data_to_db(weather_dict, True)#insert

#                if lifestyle_db_record != []:#数据库中已存在lifestyle，则更新
#                    self.insert_or_update_s6_heweather_lifestyle_to_db(lifestyle_dict, False)
#                else:#数据库中不存在lifestyle，则插入
#                    self.insert_or_update_s6_heweather_lifestyle_to_db(lifestyle_dict, True)
#            else:#更新数据失败了
#                for i in range(0, len(lifestyle_db_record[0])):
#                    lifestyle_dict[lifestyle_key_list[i]] = lifestyle_db_record[0][i]
#                lifestyle_dict['id'] = cityid

#        combination_dict['weather'] = weather_dict;
#        combination_dict['lifestyle'] = lifestyle_dict;
#        all_dict['KylinWeather'] = combination_dict

#        all_json = json.dumps(all_dict, ensure_ascii=False, sort_keys=True, indent=4)

#        return all_json





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
                for i in range(0, len(weather_db_record[0])):
                    weather_dict[weather_key_list[i]] = weather_db_record[0][i]
                weather_dict['id'] = cityid

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
        if cities_str.find('+'):
            line = cities_str.split('+')
            for cityid in line:
                citylist.append(cityid)

        if len(citylist) == 0:
            simple_dict['KylinWeather'] = combination_dict
            simple_json = json.dumps(simple_dict, ensure_ascii=False, sort_keys=True, indent=4)
            return simple_json

        for i in range(0, len(citylist)):
            weather_dict = {}
            lifestyle_dict = {}
            print "citylist[i]======", citylist[i]
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
                print "combination_dict=======", combination_dict

        simple_dict['KylinWeather'] = combination_dict

        simple_json = json.dumps(simple_dict, ensure_ascii=False, sort_keys=True, indent=4)
        return simple_json
        # 20200307---------------------------------------


if __name__ == "__main__":
    db = DataBase()
    #20200307 create new database table
    db.init_s6_heweather_now_and_forecast_table()
    db.init_s6_heweather_lifestyle_table()

    app = AppServer()
    aa = app.heweather_s6_all_data_api('101250101')#'101071205'
    print "aa:", aa

    citylist = []
    citylist.append('101250101')
    citylist.append('101010100')
    citylist.append('101030100')
    citylist.append('101020100')
    cityies_str = "+".join(citylist)
    print "cityies_str:", cityies_str
    bb = app.heweather_s6_simple_data_api(cityies_str)
    print "bb:", bb
