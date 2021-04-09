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

import os
import sys
import urllib2, urllib
import json
reload(sys)
sys.setdefaultencoding("utf-8")

import threading
import MySQLdb as kdb
import time, httplib

HEWEATHER_AIR_NOW_URL = 'https://free-api.heweather.com/s6/air/now?location=CN%s&key=a3c0a9ef33b44257a6c8f2643a42e5b3'
HEWEATHER_WEATHER_URL = 'https://free-api.heweather.com/s6/weather?location=CN%s&key=40cc3ec6bbbf4de6a04029e207c986fd'

def get_local_format_time():
    '''
    year-month-day hour:minute:second
    2014-05-07 13:51:30
    '''
    local_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return local_date

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



#all: https://free-api.heweather.com/s6/weather?location=CN101250101&key=4ff2e595e593439380e52d2519523d0a
#now(在all里面存在，可不单独获取): https://free-api.heweather.com/s6/weather/now?location=CN101250101&key=4ff2e595e593439380e52d2519523d0a
#20180827 heweather s6 version   http://www.heweather.com/documents/api/s6/weather-now
CREATE_HEWEATHER_OBSERVE_S6 = "create table heweather_observe (id varchar(32) primary key,location varchar(64), \
              parent_city varchar(62),admin_area varchar(32),cnty varchar(32),lat varchar(16),lon varchar(16),tz varchar(10), \
              update_loc varchar(32),update_utc varchar(32),cloud varchar(32),cond_code varchar(10),cond_txt varchar(32), \
              fl varchar(10),hum varchar(10),pcpn varchar(10),pres varchar(10),tmp varchar(10), \
              vis varchar(10),wind_deg varchar(10),wind_dir varchar(32),wind_sc varchar(10),wind_spd varchar(10))ENGINE = INNODB DEFAULT CHARSET=utf8 COLLATE=utf8_bin"

#num 23
INSERT_HEWEATHER_OBSERVE_S6 = "insert into heweather_observe (id,location,parent_city,admin_area,cnty,lat,lon,tz,update_loc,update_utc,cloud,cond_code,cond_txt,fl,hum,pcpn,pres,tmp,vis,wind_deg,wind_dir,wind_sc,wind_spd) values \
              ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
#num 22
QUERY_HEWEATHER_OBSERVE_S6 = "select location,parent_city,admin_area,cnty,lat,lon,tz,update_loc,update_utc,cloud,cond_code,cond_txt,fl,hum,pcpn,pres,tmp,vis,wind_deg,wind_dir,wind_sc,wind_spd \
               from heweather_observe where id='%s'"
QUERY_HEWEATHER_OBSERVE_TIME_S6 = "select update_loc from heweather_observe where id='%s'"
#22
UPDATE_HEWEATHER_OBSERVE_S6 = "update heweather_observe set location='%s',parent_city='%s',admin_area='%s',cnty='%s',lat='%s',lon='%s',tz='%s',update_loc='%s',update_utc='%s',cloud='%s',cond_code='%s',cond_txt='%s',fl='%s',hum='%s',pcpn='%s',pres='%s',tmp='%s',vis='%s',wind_deg='%s',wind_dir='%s',wind_sc='%s',wind_spd='%s' \
                where id='%s'"


#air: https://free-api.heweather.com/s6/air/now?location=CN101250101&key=4ff2e595e593439380e52d2519523d0a
CREATE_HEWEATHER_AIR_S6 = "create table heweather_air (id varchar(32) primary key,location varchar(64),pub_time varchar(32), \
              aqi varchar(10),qlty varchar(32),main varchar(10), \
              pm25 varchar(10),pm10 varchar(10), no2 varchar(10), \
              so2 varchar(10),co varchar(10),o3 varchar(10))ENGINE = INNODB DEFAULT CHARSET=utf8 COLLATE=utf8_bin"

INSERT_HEWEATHER_AIR_S6 = "insert into heweather_air (id,location,pub_time,aqi,qlty,main,pm25,pm10,no2,so2,co,o3) values \
              ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
QUERY_HEWEATHER_AIR_S6 = "select location,pub_time,aqi,qlty,main,pm25,pm10,no2,so2,co,o3 \
               from heweather_air where id='%s'"
QUERY_HEWEATHER_AIR_TIME_S6 = "select pub_time from heweather_air where id='%s'"
UPDATE_HEWEATHER_AIR_S6 = "update heweather_air set pub_time='%s',aqi='%s',qlty='%s',main='%s',pm25='%s',pm10='%s',no2='%s',so2='%s',co='%s',o3='%s' \
                where id='%s'"

#forecast(在all里面存在，可不单独获取): https://free-api.heweather.com/s6/weather/forecast?location=CN101250101&key=898b4f748e104ca09cbd161125421a86
#60
CREATE_HEWEATHER_FORECAST_S6 = "create table heweather_forecast (id varchar(32) primary key,location varchar(64),update_loc varchar(32), \
              cond_code_d0 varchar(10),cond_code_n0 varchar(10),cond_txt_d0 varchar(32),cond_txt_n0 varchar(32),forcast_date0 varchar(16), \
              hum0 varchar(10),mr_ms0 varchar(16),pcpn0 varchar(10),pop0 varchar(10),pres0 varchar(10),sr_ss0 varchar(16),tmp_max0 varchar(10),tmp_min0 varchar(10), \
              uv_index0 varchar(10),vis0 varchar(10),wind_deg0 varchar(10),wind_dir0 varchar(32),wind_sc0 varchar(10),wind_spd0 varchar(10), \
              cond_code_d1 varchar(10),cond_code_n1 varchar(10),cond_txt_d1 varchar(32),cond_txt_n1 varchar(32),forcast_date1 varchar(16), \
              hum1 varchar(10),mr_ms1 varchar(16),pcpn1 varchar(10),pop1 varchar(10),pres1 varchar(10),sr_ss1 varchar(16),tmp_max1 varchar(10),tmp_min1 varchar(10), \
              uv_index1 varchar(10),vis1 varchar(10),wind_deg1 varchar(10),wind_dir1 varchar(32),wind_sc1 varchar(10),wind_spd1 varchar(10), \
              cond_code_d2 varchar(10),cond_code_n2 varchar(10),cond_txt_d2 varchar(32),cond_txt_n2 varchar(32),forcast_date2 varchar(16), \
              hum2 varchar(10),mr_ms2 varchar(16),pcpn2 varchar(10),pop2 varchar(10),pres2 varchar(10),sr_ss2 varchar(16),tmp_max2 varchar(10),tmp_min2 varchar(10), \
              uv_index2 varchar(10),vis2 varchar(10),wind_deg2 varchar(10),wind_dir2 varchar(32),wind_sc2 varchar(10),wind_spd2 varchar(10))ENGINE = INNODB DEFAULT CHARSET=utf8 COLLATE=utf8_bin"
#60
INSERT_HEWEATHER_FORECAST_S6 = "insert into heweather_forecast (id,location,update_loc,cond_code_d0,cond_code_n0,cond_txt_d0,cond_txt_n0,forcast_date0,hum0,mr_ms0,pcpn0,pop0,pres0,sr_ss0,tmp_max0,tmp_min0,uv_index0,vis0,wind_deg0,wind_dir0,wind_sc0,wind_spd0,cond_code_d1,cond_code_n1,cond_txt_d1,cond_txt_n1,forcast_date1,hum1,mr_ms1,pcpn1,pop1,pres1,sr_ss1,tmp_max1,tmp_min1,uv_index1,vis1,wind_deg1,wind_dir1,wind_sc1,wind_spd1,cond_code_d2,cond_code_n2,cond_txt_d2,cond_txt_n2,forcast_date2,hum2,mr_ms2,pcpn2,pop2,pres2,sr_ss2,tmp_max2,tmp_min2,uv_index2,vis2,wind_deg2,wind_dir2,wind_sc2,wind_spd2) values \
              ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
#59
QUERY_HEWEATHER_FORECAST_S6 = "select location,update_loc,cond_code_d0,cond_code_n0,cond_txt_d0,cond_txt_n0,forcast_date0,hum0,mr_ms0,pcpn0,pop0,pres0,sr_ss0,tmp_max0,tmp_min0,uv_index0,vis0,wind_deg0,wind_dir0,wind_sc0,wind_spd0,cond_code_d1,cond_code_n1,cond_txt_d1,cond_txt_n1,forcast_date1,hum1,mr_ms1,pcpn1,pop1,pres1,sr_ss1,tmp_max1,tmp_min1,uv_index1,vis1,wind_deg1,wind_dir1,wind_sc1,wind_spd1,cond_code_d2,cond_code_n2,cond_txt_d2,cond_txt_n2,forcast_date2,hum2,mr_ms2,pcpn2,pop2,pres2,sr_ss2,tmp_max2,tmp_min2,uv_index2,vis2,wind_deg2,wind_dir2,wind_sc2,wind_spd2 \
               from heweather_forecast where id='%s'"
QUERY_HEWEATHER_FORECAST_TIME_S6 = "select update_loc from heweather_forecast where id='%s'"
#59
UPDATE_HEWEATHER_FORECAST_S6 = "update heweather_forecast set location='%s',update_loc='%s',cond_code_d0='%s',cond_code_n0='%s',cond_txt_d0='%s',cond_txt_n0='%s',forcast_date0='%s',hum0='%s',mr_ms0='%s',pcpn0='%s',pop0='%s',pres0='%s',sr_ss0='%s',tmp_max0='%s',tmp_min0='%s',uv_index0='%s',vis0='%s',wind_deg0='%s',wind_dir0='%s',wind_sc0='%s',wind_spd0='%s', \
                    cond_code_d1='%s',cond_code_n1='%s',cond_txt_d1='%s',cond_txt_n1='%s',forcast_date1='%s',hum1='%s',mr_ms1='%s',pcpn1='%s',pop1='%s',pres1='%s',sr_ss1='%s',tmp_max1='%s',tmp_min1='%s',uv_index1='%s',vis1='%s',wind_deg1='%s',wind_dir1='%s',wind_sc1='%s',wind_spd1='%s', \
                    cond_code_d2='%s',cond_code_n2='%s',cond_txt_d2='%s',cond_txt_n2='%s',forcast_date2='%s',hum2='%s',mr_ms2='%s',pcpn2='%s',pop2='%s',pres2='%s',sr_ss2='%s',tmp_max2='%s',tmp_min2='%s',uv_index2='%s',vis2='%s',wind_deg2='%s',wind_dir2='%s',wind_sc2='%s',wind_spd2='%s' \
                    where id='%s'"


#lifestyle(在all里面存在，可不单独获取): https://free-api.heweather.com/s6/weather/lifestyle?location=CN101250101&key=4ff2e595e593439380e52d2519523d0a
CREATE_HEWEATHER_LIFESTYLE_S6 = "create table heweather_lifestyle (id varchar(32) primary key, \
              comf_brf varchar(32),comf_txt varchar(256),drsg_brf varchar(32),drsg_txt varchar(256), \
              flu_brf varchar(32),flu_txt varchar(256),sport_brf varchar(32),sport_txt varchar(256), \
              trav_brf varchar(32),trav_txt varchar(256),uv_brf varchar(32),uv_txt varchar(256), \
              cw_brf varchar(32),cw_txt varchar(256),air_brf varchar(32),air_txt varchar(256))ENGINE = INNODB DEFAULT CHARSET=utf8 COLLATE=utf8_bin"

INSERT_HEWEATHER_LIFESTYLE_S6 = "insert into heweather_lifestyle (id,comf_brf,comf_txt,drsg_brf,drsg_txt,flu_brf,flu_txt,sport_brf,sport_txt,trav_brf,trav_txt,uv_brf,uv_txt,cw_brf,cw_txt,air_brf,air_txt) values \
              ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
QUERY_HEWEATHER_LIFESTYLE_S6 = "select comf_brf,comf_txt,drsg_brf,drsg_txt,flu_brf,flu_txt,sport_brf,sport_txt,trav_brf,trav_txt,uv_brf,uv_txt,cw_brf,cw_txt,air_brf,air_txt \
               from heweather_lifestyle where id='%s'"
UPDATE_HEWEATHER_LIFESTYLE_S6 = "update heweather_lifestyle set comf_brf='%s',comf_txt='%s',drsg_brf='%s',drsg_txt='%s',flu_brf='%s',flu_txt='%s',sport_brf='%s',sport_txt='%s',trav_brf='%s',trav_txt='%s',uv_brf='%s',uv_txt='%s',cw_brf='%s',cw_txt='%s',air_brf='%s',air_txt='%s' \
                where id='%s'"



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

    #-------------------------20180827 heweather s6 version-------------------------------
    def init_heweather_air_s6_table(self):
        self.cursor.execute(CREATE_HEWEATHER_AIR_S6)

    def init_heweather_observe_s6_table(self):
        self.cursor.execute(CREATE_HEWEATHER_OBSERVE_S6)

    def init_heweather_forecast_s6_table(self):
        self.cursor.execute(CREATE_HEWEATHER_FORECAST_S6)

    def init_heweather_lifestyle_s6_table(self):
        self.cursor.execute(CREATE_HEWEATHER_LIFESTYLE_S6)

    #10
    def search_heweather_air_s6_record(self, id):
        self.cursor.execute(QUERY_HEWEATHER_AIR_S6 % (id))
        res = self.cursor.fetchall()
        if len(res) == 0:
            return []
        else:
            return res

    def search_heweather_air_s6_record_update_time(self, id):
        self.cursor.execute(QUERY_HEWEATHER_AIR_TIME_S6 % (id))
        res = self.cursor.fetchall()
        if len(res) == 0:
            return []
        else:
            return res

    #12
    def insert_heweather_air_s6_data(self,id,location,pub_time,aqi,qlty,main,pm25,pm10,no2,so2,co,o3):
        self.cursor.execute(INSERT_HEWEATHER_AIR_S6 % (id,str(location),str(pub_time),str(aqi),str(qlty),str(main),str(pm25),str(pm10),str(no2),str(so2),str(co),str(o3)))
        self.connect.commit()

    #11
    def update_heweather_air_s6_data(self,pub_time,aqi,qlty,main,pm25,pm10,no2,so2,co,o3,id):
        self.cursor.execute(UPDATE_HEWEATHER_AIR_S6 % (str(pub_time),str(aqi),str(qlty),str(main),str(pm25),str(pm10),str(no2),str(so2),str(co),str(o3),str(id)))
        self.connect.commit()

    #16
    def search_heweather_lifestyle_s6_record(self, id):
        self.cursor.execute(QUERY_HEWEATHER_LIFESTYLE_S6 % (id))
        res = self.cursor.fetchall()
        if len(res) == 0:
            return []
        else:
            return res

    #17
    def insert_heweather_lifestyle_s6_data(self,id,comf_brf,comf_txt,drsg_brf,drsg_txt,flu_brf,flu_txt,sport_brf,sport_txt,trav_brf,trav_txt,uv_brf,uv_txt,cw_brf,cw_txt,air_brf,air_txt):
        self.cursor.execute(INSERT_HEWEATHER_LIFESTYLE_S6 % (id,comf_brf,comf_txt,drsg_brf,drsg_txt,flu_brf,flu_txt,sport_brf,sport_txt,trav_brf,trav_txt,uv_brf,uv_txt,cw_brf,cw_txt,air_brf,air_txt))
        self.connect.commit()

    #16
    def update_heweather_lifestyle_s6_data(self,comf_brf,comf_txt,drsg_brf,drsg_txt,flu_brf,flu_txt,sport_brf,sport_txt,trav_brf,trav_txt,uv_brf,uv_txt,cw_brf,cw_txt,air_brf,air_txt,id):
        self.cursor.execute(UPDATE_HEWEATHER_LIFESTYLE_S6 % (comf_brf,comf_txt,drsg_brf,drsg_txt,flu_brf,flu_txt,sport_brf,sport_txt,trav_brf,trav_txt,uv_brf,uv_txt,cw_brf,cw_txt,air_brf,air_txt,id))
        self.connect.commit()

    #22
    def search_heweather_observe_s6_record(self, id):
        self.cursor.execute(QUERY_HEWEATHER_OBSERVE_S6 % (id))
        res = self.cursor.fetchall()
        if len(res) == 0:
            return []
        else:
            return res

    def search_heweather_observe_s6_record_update_time(self, id):
        self.cursor.execute(QUERY_HEWEATHER_OBSERVE_TIME_S6 % (id))
        res = self.cursor.fetchall()
        if len(res) == 0:
            return []
        else:
            return res

    #23
    def insert_heweather_observe_s6_data(self,id,location,parent_city,admin_area,cnty,lat,lon,tz,update_loc,update_utc,cloud,cond_code,cond_txt,fl,hum,pcpn,pres,tmp,vis,wind_deg,wind_dir,wind_sc,wind_spd):
        self.cursor.execute(INSERT_HEWEATHER_OBSERVE_S6 % (id,location,parent_city,admin_area,cnty,lat,lon,tz,update_loc,update_utc,cloud,cond_code,cond_txt,fl,hum,pcpn,pres,tmp,vis,wind_deg,wind_dir,wind_sc,wind_spd))
        self.connect.commit()

    #22
    def update_heweather_observe_s6_data(self,location,parent_city,admin_area,cnty,lat,lon,tz,update_loc,update_utc,cloud,cond_code,cond_txt,fl,hum,pcpn,pres,tmp,vis,wind_deg,wind_dir,wind_sc,wind_spd,id):
        self.cursor.execute(UPDATE_HEWEATHER_OBSERVE_S6 % (location,parent_city,admin_area,cnty,lat,lon,tz,update_loc,update_utc,cloud,cond_code,cond_txt,fl,hum,pcpn,pres,tmp,vis,wind_deg,wind_dir,wind_sc,wind_spd,id))
        self.connect.commit()

    #59
    def search_heweather_forecast_s6_record(self, cityid):
        self.cursor.execute(QUERY_HEWEATHER_FORECAST_S6 % (cityid))
        res = self.cursor.fetchall()
        if len(res) == 0:
            return []
        else:
            return res

    def search_heweather_forecast_s6_record_update_time(self, cityid):
        self.cursor.execute(QUERY_HEWEATHER_FORECAST_TIME_S6 % (cityid))
        res = self.cursor.fetchall()
        if len(res) == 0:
            return []
        else:
            return res

    def insert_heweather_forecast_s6_data(self,id,location,update_loc,cond_code_d0,cond_code_n0,cond_txt_d0,cond_txt_n0,forcast_date0,hum0,mr_ms0,pcpn0,pop0,pres0,sr_ss0,tmp_max0,tmp_min0,uv_index0,vis0,wind_deg0,wind_dir0,wind_sc0,wind_spd0,cond_code_d1,cond_code_n1,cond_txt_d1,cond_txt_n1,forcast_date1,hum1,mr_ms1,pcpn1,pop1,pres1,sr_ss1,tmp_max1,tmp_min1,uv_index1,vis1,wind_deg1,wind_dir1,wind_sc1,wind_spd1,cond_code_d2,cond_code_n2,cond_txt_d2,cond_txt_n2,forcast_date2,hum2,mr_ms2,pcpn2,pop2,pres2,sr_ss2,tmp_max2,tmp_min2,uv_index2,vis2,wind_deg2,wind_dir2,wind_sc2,wind_spd2):
        self.cursor.execute(INSERT_HEWEATHER_FORECAST_S6 % (id,location,update_loc,cond_code_d0,cond_code_n0,cond_txt_d0,cond_txt_n0,forcast_date0,hum0,mr_ms0,pcpn0,pop0,pres0,sr_ss0,tmp_max0,tmp_min0,uv_index0,vis0,wind_deg0,wind_dir0,wind_sc0,wind_spd0,cond_code_d1,cond_code_n1,cond_txt_d1,cond_txt_n1,forcast_date1,hum1,mr_ms1,pcpn1,pop1,pres1,sr_ss1,tmp_max1,tmp_min1,uv_index1,vis1,wind_deg1,wind_dir1,wind_sc1,wind_spd1,cond_code_d2,cond_code_n2,cond_txt_d2,cond_txt_n2,forcast_date2,hum2,mr_ms2,pcpn2,pop2,pres2,sr_ss2,tmp_max2,tmp_min2,uv_index2,vis2,wind_deg2,wind_dir2,wind_sc2,wind_spd2))
        self.connect.commit()

    def update_heweather_forecast_s6_data(self,location,update_loc,cond_code_d0,cond_code_n0,cond_txt_d0,cond_txt_n0,forcast_date0,hum0,mr_ms0,pcpn0,pop0,pres0,sr_ss0,tmp_max0,tmp_min0,uv_index0,vis0,wind_deg0,wind_dir0,wind_sc0,wind_spd0,cond_code_d1,cond_code_n1,cond_txt_d1,cond_txt_n1,forcast_date1,hum1,mr_ms1,pcpn1,pop1,pres1,sr_ss1,tmp_max1,tmp_min1,uv_index1,vis1,wind_deg1,wind_dir1,wind_sc1,wind_spd1,cond_code_d2,cond_code_n2,cond_txt_d2,cond_txt_n2,forcast_date2,hum2,mr_ms2,pcpn2,pop2,pres2,sr_ss2,tmp_max2,tmp_min2,uv_index2,vis2,wind_deg2,wind_dir2,wind_sc2,wind_spd2,id):
        self.cursor.execute(UPDATE_HEWEATHER_FORECAST_S6 % (location,update_loc,cond_code_d0,cond_code_n0,cond_txt_d0,cond_txt_n0,forcast_date0,hum0,mr_ms0,pcpn0,pop0,pres0,sr_ss0,tmp_max0,tmp_min0,uv_index0,vis0,wind_deg0,wind_dir0,wind_sc0,wind_spd0,cond_code_d1,cond_code_n1,cond_txt_d1,cond_txt_n1,forcast_date1,hum1,mr_ms1,pcpn1,pop1,pres1,sr_ss1,tmp_max1,tmp_min1,uv_index1,vis1,wind_deg1,wind_dir1,wind_sc1,wind_spd1,cond_code_d2,cond_code_n2,cond_txt_d2,cond_txt_n2,forcast_date2,hum2,mr_ms2,pcpn2,pop2,pres2,sr_ss2,tmp_max2,tmp_min2,uv_index2,vis2,wind_deg2,wind_dir2,wind_sc2,wind_spd2,id))
        self.connect.commit()

#    def insert_heweather_forecast_s6_data(self, dict_data):
#        self.cursor.execute(INSERT_HEWEATHER_FORECAST_S6 % (dict_data['id'],dict_data['location'],dict_data['update_loc'], \
#                                               dict_data['cond_code_d0'],dict_data['cond_code_n0'],dict_data['cond_txt_d0'],dict_data['cond_txt_n0'],dict_data['forcast_date0'],dict_data['hum0'],dict_data['mr_ms0'],dict_data['pcpn0'],dict_data['pop0'],dict_data['pres0'], \
#                                               dict_data['sr_ss0'],dict_data['tmp_max0'],dict_data['tmp_min0'],dict_data['uv_index0'],dict_data['vis0'],dict_data['wind_deg0'],dict_data['wind_dir0'],dict_data['wind_sc0'],dict_data['wind_spd0'], \
#                                               dict_data['cond_code_d1'],dict_data['cond_code_n1'],dict_data['cond_txt_d1'],dict_data['cond_txt_n1'],dict_data['forcast_date1'],dict_data['hum1'],dict_data['mr_ms1'],dict_data['pcpn1'],dict_data['pop1'],dict_data['pres1'], \
#                                               dict_data['sr_ss1'],dict_data['tmp_max1'],dict_data['tmp_min1'],dict_data['uv_index1'],dict_data['vis1'],dict_data['wind_deg1'],dict_data['wind_dir1'],dict_data['wind_sc1'],dict_data['wind_spd1'], \
#                                               dict_data['cond_code_d2'],dict_data['cond_code_n2'],dict_data['cond_txt_d2'],dict_data['cond_txt_n2'],dict_data['forcast_date2'],dict_data['hum2'],dict_data['mr_ms2'],dict_data['pcpn2'],dict_data['pop2'],dict_data['pres2'], \
#                                               dict_data['sr_ss2'],dict_data['tmp_max2'],dict_data['tmp_min2'],dict_data['uv_index2'],dict_data['vis2'],dict_data['wind_deg2'],dict_data['wind_dir2'],dict_data['wind_sc2'],dict_data['wind_spd2']))
#        self.connect.commit()

#    def update_heweather_forecast_s6_data(self, dict_data):
#        self.cursor.execute(UPDATE_HEWEATHER_FORECAST_S6 % (dict_data['location'],dict_data['update_loc'], \
#        dict_data['cond_code_d0'],dict_data['cond_code_n0'],dict_data['cond_txt_d0'],dict_data['cond_txt_n0'],dict_data['forcast_date0'],dict_data['hum0'],dict_data['mr_ms0'],dict_data['pcpn0'],dict_data['pop0'],dict_data['pres0'], \
#        dict_data['sr_ss0'],dict_data['tmp_max0'],dict_data['tmp_min0'],dict_data['uv_index0'],dict_data['vis0'],dict_data['wind_deg0'],dict_data['wind_dir0'],dict_data['wind_sc0'],dict_data['wind_spd0'], \
#        dict_data['cond_code_d1'],dict_data['cond_code_n1'],dict_data['cond_txt_d1'],dict_data['cond_txt_n1'],dict_data['forcast_date1'],dict_data['hum1'],dict_data['mr_ms1'],dict_data['pcpn1'],dict_data['pop1'],dict_data['pres1'], \
#        dict_data['sr_ss1'],dict_data['tmp_max1'],dict_data['tmp_min1'],dict_data['uv_index1'],dict_data['vis1'],dict_data['wind_deg1'],dict_data['wind_dir1'],dict_data['wind_sc1'],dict_data['wind_spd1'], \
#        dict_data['cond_code_d2'],dict_data['cond_code_n2'],dict_data['cond_txt_d2'],dict_data['cond_txt_n2'],dict_data['forcast_date2'],dict_data['hum2'],dict_data['mr_ms2'],dict_data['pcpn2'],dict_data['pop2'],dict_data['pres2'], \
#        dict_data['sr_ss2'],dict_data['tmp_max2'],dict_data['tmp_min2'],dict_data['uv_index2'],dict_data['vis2'],dict_data['wind_deg2'],dict_data['wind_dir2'],dict_data['wind_sc2'],dict_data['wind_spd2'],dict_data['id']))
#        self.connect.commit()
    #-------------------------20180827 heweather s6 version-------------------------------




class AppServer:
    def __init__(self):
        self.db = DataBase()

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


if __name__ == "__main__":
    app = AppServer()
#    print os.path.split(os.path.realpath(sys.argv[0]))[0]
#    print os.getcwd()
    print "Observe:\n", app.get_heweather_observe_s6("101250101")
    print "Forecast:\n", app.get_heweather_forecast_s6("101250101")
