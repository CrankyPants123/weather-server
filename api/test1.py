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


CHN_CITY_LIST_FILE = 'locations.txt'

import threading
import MySQLdb as kdb
import time, httplib

#example:   https://free-api.heweather.net/s6/weather?location=CN101250101&key=a3c0a9ef33b44257a6c8f2643a42e5b3

#Changelog:   free-api.heweather.com  ------>  free-api.heweather.net

WEATHER_UK_AQI_URL = 'https://free-api.heweather.net/s6/air/now?location=CN%s&key=a3c0a9ef33b44257a6c8f2643a42e5b3'
WEATHER_UK_URL = 'https://free-api.heweather.net/s6/weather?location=CN%s&key=a3c0a9ef33b44257a6c8f2643a42e5b3'
WEATHER_HB_AQI_URL = 'https://free-api.heweather.net/s6/air/now?location=CN%s&key=40cc3ec6bbbf4de6a04029e207c986fd'
WEATHER_HB_URL = 'https://free-api.heweather.net/s6/weather?location=CN%s&key=40cc3ec6bbbf4de6a04029e207c986fd'


WEATHER_TEST_AQI_URL = 'https://free-api.heweather.net/s6/air/now?location=CN%s&key=4ff2e595e593439380e52d2519523d0a'
WEATHER_TEST_URL = 'https://free-api.heweather.net/s6/weather?location=CN%s&key=4ff2e595e593439380e52d2519523d0a'


#weather now
#https://free-api.heweather.net/s6/weather/now?location=CN101250101&key=4ff2e595e593439380e52d2519523d0a

#weather forecast
#https://free-api.heweather.net/s6/weather/forecast?location=CN101250101&key=4ff2e595e593439380e52d2519523d0a

#weather hourly
#https://free-api.heweather.net/s6/weather/hourly?location=CN101250101&key=4ff2e595e593439380e52d2519523d0a

#weather lifestyle
#https://free-api.heweather.net/s6/weather/lifestyle?location=CN101250101&key=4ff2e595e593439380e52d2519523d0a

#weather all(now + forecast + hourly + lifestyle)
#https://free-api.heweather.net/s6/weather?location=CN101250101&key=4ff2e595e593439380e52d2519523d0a




# =============aqi=============
#aqi now
#https://free-api.heweather.net/s6/air/now?location=CN101250101&key=4ff2e595e593439380e52d2519523d0a

#aqi forecast
#https://free-api.heweather.net/s6/air/forecast?location=CN101250101&key=4ff2e595e593439380e52d2519523d0a

#aqi hourly
#https://free-api.heweather.net/s6/air/hourly?location=CN101250101&key=4ff2e595e593439380e52d2519523d0a



def get_local_format_time():
    '''
    year-month-day hour:minute:second
    2014-05-07 13:51:30
    '''
    local_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return local_date



CREATE_OBSERVE = "create table observe (id varchar(32) primary key,city varchar(64), \
              ptime varchar(32),time varchar(32),update_time varchar(64),WD varchar(32),WS varchar(32),SD varchar(32), \
              weather varchar(64),img1 varchar(32), img2 varchar(32), \
              temp varchar(32),temp1 varchar(32),temp2 varchar(32),aqi varchar(64))ENGINE = INNODB DEFAULT CHARSET=utf8 COLLATE=utf8_bin"

INSERT_OBSERVE = "insert into observe (id,city,ptime,time,update_time,WD,WS,SD,weather,img1,img2,temp,temp1,temp2,aqi) values \
              ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
QUERY_OBSERVE = "select city,ptime,time,WD,WS,SD,weather,img1,img2,temp,temp1,temp2,aqi \
               from observe where id='%s'"
QUERY_TIME_OBSERVE = "select update_time from observe where id='%s'"
UPDATE_OBSERVE = "update observe set ptime='%s',time='%s',update_time='%s',WD='%s',WS='%s',SD='%s',weather='%s',img1='%s',img2='%s',temp='%s',temp1='%s',temp2='%s',aqi='%s' \
                where id='%s'"

CREATE_FORECAST3D = "create table forecast3d (id varchar(32) primary key,city_zh varchar(64),city_name_zh varchar(64), \
              province_zh varchar(64),country_zh varchar(32),city_level varchar(32),area_code varchar(32),\
              zip_code varchar(64),longitude varchar(32),latitude varchar(32),altitude varchar(32), \
              radar_station varchar(32),time_zone varchar(32),release_time varchar(32),update_time varchar(64),language varchar(32), \
              sunrise_sunset_1 varchar(32),d1_weaher varchar(32),n1_weaher varchar(32),d1_temperature varchar(32),n1_temperature varchar(32), \
              d1_wind_direction varchar(32),n1_wind_direction varchar(32),d1_wind_power varchar(32),n1_wind_power varchar(32), \
              sunrise_sunset_2 varchar(32),d2_weaher varchar(32),n2_weaher varchar(32),d2_temperature varchar(32),n2_temperature varchar(32), \
              d2_wind_direction varchar(32),n2_wind_direction varchar(32),d2_wind_power varchar(32),n2_wind_power varchar(32), \
              sunrise_sunset_3 varchar(32),d3_weaher varchar(32),n3_weaher varchar(32),d3_temperature varchar(32),n3_temperature varchar(32), \
              d3_wind_direction varchar(32),n3_wind_direction varchar(32),d3_wind_power varchar(32),n3_wind_power varchar(32), \
              city_en varchar(64),city_name_en varchar(64),province_en varchar(64),country_en varchar(32))ENGINE = INNODB DEFAULT CHARSET=utf8 COLLATE=utf8_bin"


INSERT_FORECAST3D = "insert into forecast3d (id,city_zh,city_name_zh,province_zh,country_zh,city_level,area_code,zip_code,longitude,latitude,altitude,radar_station,time_zone,release_time,update_time,language,sunrise_sunset_1,d1_weaher,n1_weaher,d1_temperature,n1_temperature,d1_wind_direction,n1_wind_direction,d1_wind_power,n1_wind_power,sunrise_sunset_2,d2_weaher,n2_weaher,d2_temperature,n2_temperature,d2_wind_direction,n2_wind_direction,d2_wind_power,n2_wind_power,sunrise_sunset_3,d3_weaher,n3_weaher,d3_temperature,n3_temperature,d3_wind_direction,n3_wind_direction,d3_wind_power,n3_wind_power,city_en,city_name_en,province_en,country_en) values \
              ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
QUERY_FORECAST3D = "select city_zh,city_name_zh,province_zh,country_zh,city_level,area_code,zip_code,longitude,latitude,altitude,radar_station,time_zone,release_time,sunrise_sunset_1,d1_weaher,n1_weaher,d1_temperature,n1_temperature,d1_wind_direction,n1_wind_direction,d1_wind_power,n1_wind_power,sunrise_sunset_2,d2_weaher,n2_weaher,d2_temperature,n2_temperature,d2_wind_direction,n2_wind_direction,d2_wind_power,n2_wind_power,sunrise_sunset_3,d3_weaher,n3_weaher,d3_temperature,n3_temperature,d3_wind_direction,n3_wind_direction,d3_wind_power,n3_wind_power \
               from forecast3d where id='%s'"
QUERY_TIME_FORECAST3D = "select update_time from forecast3d where id='%s'"
UPDATE_FORECAST3D = "update forecast3d set longitude='%s',latitude='%s',altitude='%s',radar_station='%s',time_zone='%s',release_time='%s',update_time='%s',sunrise_sunset_1='%s',d1_weaher='%s',n1_weaher='%s',d1_temperature='%s',n1_temperature='%s',d1_wind_direction='%s',n1_wind_direction='%s',d1_wind_power='%s',n1_wind_power='%s',sunrise_sunset_2='%s',d2_weaher='%s',n2_weaher='%s',d2_temperature='%s',n2_temperature='%s',d2_wind_direction='%s',n2_wind_direction='%s',d2_wind_power='%s',n2_wind_power='%s',sunrise_sunset_3='%s',d3_weaher='%s',n3_weaher='%s',d3_temperature='%s',n3_temperature='%s',d3_wind_direction='%s',n3_wind_direction='%s',d3_wind_power='%s',n3_wind_power='%s' \
                where id='%s'"



CREATE_FORECAST6D = "create table forecast6d (cityid varchar(32) primary key,city varchar(64),city_en varchar(64), \
              date_y varchar(64),date varchar(32),week varchar(32),fchh varchar(32),update_time varchar(64), \
              temp1 varchar(32),temp2 varchar(32),temp3 varchar(32),temp4 varchar(32), temp5 varchar(32),temp6 varchar(32), \
              tempF1 varchar(32),tempF2 varchar(32),tempF3 varchar(32),tempF4 varchar(32),tempF5 varchar(32),tempF6 varchar(32), \
              weather1 varchar(64),weather2 varchar(64),weather3 varchar(64),weather4 varchar(64),weather5 varchar(64),weather6 varchar(64), \
              img1 varchar(10),img2 varchar(10),img3 varchar(10),img4 varchar(10), img5 varchar(10),img6 varchar(10), \
              img7 varchar(10),img8 varchar(10),img9 varchar(10), img10 varchar(10),img11 varchar(10),img12 varchar(10),img_single varchar(10),img_title_single varchar(64), \
              img_title1 varchar(32),img_title2 varchar(32),img_title3 varchar(32),img_title4 varchar(32),img_title5 varchar(32),img_title6 varchar(32), \
              img_title7 varchar(32),img_title8 varchar(32),img_title9 varchar(32),img_title10 varchar(32),img_title11 varchar(32),img_title12 varchar(32), \
              wind1 varchar(64),wind2 varchar(64),wind3 varchar(64),wind4 varchar(64),wind5 varchar(64),wind6 varchar(64), \
              fx1 varchar(64),fx2 varchar(64),fl1 varchar(64),fl2 varchar(64),fl3 varchar(64),fl4 varchar(64),fl5 varchar(64),fl6 varchar(64), \
              index_clothes varchar(32),index_d varchar(256),index_uv varchar(32),index_xc varchar(32),index_tr varchar(32),index_co varchar(32),index_cl varchar(32),index_ls varchar(32),index_ag varchar(32))ENGINE = INNODB DEFAULT CHARSET=utf8 COLLATE=utf8_bin"
#75
INSERT_FORECAST6D = "insert into forecast6d (cityid,city,city_en,date_y,date,week,fchh,update_time,temp1,temp2,temp3,temp4,temp5,temp6,tempF1,tempF2,tempF3,tempF4,tempF5,tempF6,weather1,weather2,weather3,weather4,weather5,weather6,img1,img2,img3,img4,img5,img6,img7,img8,img9,img10,img11,img12,img_single,img_title_single,img_title1,img_title2,img_title3,img_title4,img_title5,img_title6,img_title7,img_title8,img_title9,img_title10,img_title11,img_title12,wind1,wind2,wind3,wind4,wind5,wind6,fx1,fx2,fl1,fl2,fl3,fl4,fl5,fl6,index_clothes,index_d,index_uv,index_xc,index_tr,index_co,index_cl,index_ls,index_ag) values \
              ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
#45
QUERY_FORECAST6D = "select city,date_y,date,week,fchh,temp1,temp2,temp3,temp4,temp5,temp6,weather1,weather2,weather3,weather4,weather5,weather6,img1,img2,img3,img4,img5,img6,img7,img8,img9,img10,img11,img12,wind1,wind2,wind3,wind4,wind5,wind6,index_clothes,index_d,index_uv,index_xc,index_tr,index_co,index_cl,index_ls,index_ag \
               from forecast6d where cityid='%s'"
QUERY_TIME_FORECAST6D = "select update_time from forecast6d where cityid='%s'"
#73
UPDATE_FORECAST6D = "update forecast6d set date_y='%s',date='%s',week='%s',fchh='%s',update_time='%s',temp1='%s',temp2='%s',temp3='%s',temp4='%s',temp5='%s',temp6='%s',tempF1='%s',tempF2='%s',tempF3='%s',tempF4='%s',tempF5='%s',tempF6='%s',weather1='%s',weather2='%s',weather3='%s',weather4='%s',weather5='%s',weather6='%s',img1='%s',img2='%s',img3='%s',img4='%s',img5='%s',img6='%s',img7='%s',img8='%s',img9='%s',img10='%s',img11='%s',img12='%s',img_single='%s',img_title_single='%s',img_title1='%s',img_title2='%s',img_title3='%s',img_title4='%s',img_title5='%s',img_title6='%s',img_title7='%s',img_title8='%s',img_title9='%s',img_title10='%s',img_title11='%s',img_title12='%s',wind1='%s',wind2='%s',wind3='%s',wind4='%s',wind5='%s',wind6='%s',fx1='%s',fx2='%s',fl1='%s',fl2='%s',fl3='%s',fl4='%s',fl5='%s',fl6='%s',index_clothes='%s',index_d='%s',index_uv='%s',index_xc='%s',index_tr='%s',index_co='%s',index_cl='%s',index_ls='%s',index_ag='%s' \
                    where cityid='%s'"

#20170627
CREATE_HEWEATHER_FORECAST = "create table heforecast (cityid varchar(32) primary key,city varchar(64),prov varchar(64),cnty varchar(64),update_time varchar(64),insert_time varchar(64), \
              date0 varchar(32),astro_mr0 varchar(10),astro_ms0 varchar(10),astro_sr0 varchar(10),astro_ss0 varchar(10), \
              code_d0 varchar(10),code_n0 varchar(10),txt_d0 varchar(32),txt_n0 varchar(32),hum0 varchar(10),pcpn0 varchar(10),pop0 varchar(10),pres0 varchar(10),tmp_max0 varchar(10),tmp_min0 varchar(10),uv0 varchar(10),vis0 varchar(10),wind_deg0 varchar(10),wind_dir_sc0 varchar(32),wind_spd0 varchar(10), \
              date1 varchar(32),astro_mr1 varchar(10),astro_ms1 varchar(10),astro_sr1 varchar(10),astro_ss1 varchar(10), \
              code_d1 varchar(10),code_n1 varchar(10),txt_d1 varchar(32),txt_n1 varchar(32),hum1 varchar(10),pcpn1 varchar(10),pop1 varchar(10),pres1 varchar(10),tmp_max1 varchar(10),tmp_min1 varchar(10),uv1 varchar(10),vis1 varchar(10),wind_deg1 varchar(10),wind_dir_sc1 varchar(32),wind_spd1 varchar(10), \
              date2 varchar(32),astro_mr2 varchar(10),astro_ms2 varchar(10),astro_sr2 varchar(10),astro_ss2 varchar(10), \
              code_d2 varchar(10),code_n2 varchar(10),txt_d2 varchar(32),txt_n2 varchar(32),hum2 varchar(10),pcpn2 varchar(10),pop2 varchar(10),pres2 varchar(10),tmp_max2 varchar(10),tmp_min2 varchar(10),uv2 varchar(10),vis2 varchar(10),wind_deg2 varchar(10),wind_dir_sc2 varchar(32),wind_spd2 varchar(10), \
              comf_brf varchar(32),comf_txt varchar(256),cw_brf varchar(32),cw_txt varchar(256),drsg_brf varchar(32),drsg_txt varchar(256),flu_brf varchar(32),flu_txt varchar(256),sport_brf varchar(32),sport_txt varchar(256),trav_brf varchar(32),trav_txt varchar(256),uv_brf varchar(32),uv_txt varchar(256))ENGINE = INNODB DEFAULT CHARSET=utf8 COLLATE=utf8_bin"

INSERT_HEWEATHER_FORECAST = "insert into heforecast (cityid,city,prov,cnty,update_time,insert_time,date0,astro_mr0,astro_ms0,astro_sr0,astro_ss0,code_d0,code_n0,txt_d0,txt_n0,hum0,pcpn0,pop0,pres0,tmp_max0,tmp_min0,uv0,vis0,wind_deg0,wind_dir_sc0,wind_spd0,date1,astro_mr1,astro_ms1,astro_sr1,astro_ss1,code_d1,code_n1,txt_d1,txt_n1,hum1,pcpn1,pop1,pres1,tmp_max1,tmp_min1,uv1,vis1,wind_deg1,wind_dir_sc1,wind_spd1,date2,astro_mr2,astro_ms2,astro_sr2,astro_ss2,code_d2,code_n2,txt_d2,txt_n2,hum2,pcpn2,pop2,pres2,tmp_max2,tmp_min2,uv2,vis2,wind_deg2,wind_dir_sc2,wind_spd2,comf_brf,comf_txt,cw_brf,cw_txt,drsg_brf,drsg_txt,flu_brf,flu_txt,sport_brf,sport_txt,trav_brf,trav_txt,uv_brf,uv_txt) values \
              ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
QUERY_TIME_HEWEATHER_FORECAST = "select update_time from heforecast where cityid='%s'"
QUERY_HEWEATHER_FORECAST = "select city,prov,cnty,update_time,insert_time,date0,astro_mr0,astro_ms0,astro_sr0,astro_ss0,code_d0,code_n0,txt_d0,txt_n0,hum0,pcpn0,pop0,pres0,tmp_max0,tmp_min0,uv0,vis0,wind_deg0,wind_dir_sc0,wind_spd0,date1,astro_mr1,astro_ms1,astro_sr1,astro_ss1,code_d1,code_n1,txt_d1,txt_n1,hum1,pcpn1,pop1,pres1,tmp_max1,tmp_min1,uv1,vis1,wind_deg1,wind_dir_sc1,wind_spd1,date2,astro_mr2,astro_ms2,astro_sr2,astro_ss2,code_d2,code_n2,txt_d2,txt_n2,hum2,pcpn2,pop2,pres2,tmp_max2,tmp_min2,uv2,vis2,wind_deg2,wind_dir_sc2,wind_spd2,comf_brf,comf_txt,cw_brf,cw_txt,drsg_brf,drsg_txt,flu_brf,flu_txt,sport_brf,sport_txt,trav_brf,trav_txt,uv_brf,uv_txt \
               from heforecast where cityid='%s'"
UPDATE_HEWEATHER_FORECAST = "update heforecast set update_time='%s',insert_time='%s',date0='%s',astro_mr0='%s',astro_ms0='%s',astro_sr0='%s',astro_ss0='%s',code_d0='%s',code_n0='%s',txt_d0='%s',txt_n0='%s',hum0='%s',pcpn0='%s',pop0='%s',pres0='%s',tmp_max0='%s',tmp_min0='%s',uv0='%s',vis0='%s',wind_deg0='%s',wind_dir_sc0='%s',wind_spd0='%s',date1='%s',astro_mr1='%s',astro_ms1='%s',astro_sr1='%s',astro_ss1='%s',code_d1='%s',code_n1='%s',txt_d1='%s',txt_n1='%s',hum1='%s',pcpn1='%s',pop1='%s',pres1='%s',tmp_max1='%s',tmp_min1='%s',uv1='%s',vis1='%s',wind_deg1='%s',wind_dir_sc1='%s',wind_spd1='%s',date2='%s',astro_mr2='%s',astro_ms2='%s',astro_sr2='%s',astro_ss2='%s',code_d2='%s',code_n2='%s',txt_d2='%s',txt_n2='%s',hum2='%s',pcpn2='%s',pop2='%s',pres2='%s',tmp_max2='%s',tmp_min2='%s',uv2='%s',vis2='%s',wind_deg2='%s',wind_dir_sc2='%s',wind_spd2='%s',comf_brf='%s',comf_txt='%s',cw_brf='%s',cw_txt='%s',drsg_brf='%s',drsg_txt='%s',flu_brf='%s',flu_txt='%s',sport_brf='%s',sport_txt='%s',trav_brf='%s',trav_txt='%s',uv_brf='%s',uv_txt='%s' \
                    where cityid='%s'"

def read_json_from_url(url):
    # returns weather info by json_string
    request = urllib2.Request(url, headers={'User-Agent' : 'Magic Browser'})
    f = urllib2.urlopen(request)
    json_string = f.read()
    f.close()
    return json_string

class AppServer:
    def __init__(self):
        pass

    def access_heweather_forecast_and_observe(self, cityid):
        weather_data = {}
        weather_key_list = ['cityid', 'city', 'prov', 'cnty', 'update_time', 'forecast', 'now', 'aqi', 'comf_brf','comf_txt','cw_brf','cw_txt','drsg_brf','drsg_txt','flu_brf','flu_txt','sport_brf','sport_txt','trav_brf','trav_txt','uv_brf','uv_txt', 'air_brf', 'air_txt']

        weather_data['days'] = 0
        for i in range(0, len(weather_key_list)):
            weather_data[weather_key_list[i]] = "-"

        try:
            print "AAAAAAAAAAAAAAA"

            url = WEATHER_TEST_URL % (cityid)
            url_aqi = WEATHER_TEST_AQI_URL % (cityid)

            json_string = read_json_from_url(url)
            parsed_json = json.loads(json_string)

            json_aqi_string = read_json_from_url(url_aqi)
            parsed_aqi_json = json.loads(json_aqi_string)

            #print "#############parsed_json", parsed_json
            #print "#############parsed_aqi_json", parsed_aqi_json

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

            # 和风天气api s6版本
            tmp_list = parsed_json['HeWeather6'][0]
            if tmp_list:
                if tmp_list['status'] == "ok":
                    weather_data['cityid'] = cityid
                    # basic
                    if tmp_list.has_key('basic'):
                        basic_dict = tmp_list['basic']
                        if (isinstance(basic_dict, dict)):
                            if basic_dict.has_key('location'):
                                weather_data['city'] = basic_dict.get('location', "-")
                            if basic_dict.has_key('admin_area'):
                                weather_data['prov'] = basic_dict.get('admin_area', "-")
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
                        weather_data['days'] = forecast_len
                        weather_data['forecast'] = ''
                        for i in range(forecast_len):
                            data_dict = daily_forecast[i]
                            if (isinstance(data_dict, dict)):
                                forecast_value = ''
                                for k,v in data_dict.items():
                                    forecast_tmp_value = k + "=" + v + ","
                                    forecast_value += forecast_tmp_value
                                weather_data['forecast'] += "%s;" % forecast_value

#                        for data in daily_forecast:#3 or 7 days forecast
#                            if (isinstance(data, dict)):
#                                for k,v in data.items():
#                                    focast_tmp_value = k + "=" + v + ","
#                                    weather_data['forecast'] += focast_tmp_value

                    # lifestyle
                    if tmp_list.has_key('lifestyle'):
                        suggestion_dict = tmp_list['lifestyle']
                        for i in range(len(suggestion_dict)):
                            sub_dict = suggestion_dict[i]
                            if (isinstance(sub_dict, dict)):
                                if sub_dict.get('type', "") == "comf":
                                    weather_data['comf_brf'] = sub_dict.get('brf', "未知")#舒适度指数  简介
                                    weather_data['comf_txt'] = sub_dict.get('txt', "未知")#舒适度指数  详细描述
                                elif sub_dict.get('type', "") == "drsg":
                                    weather_data['drsg_brf'] = sub_dict.get('brf', "未知")#穿衣指数  简介
                                    weather_data['drsg_txt'] = sub_dict.get('txt', "未知")#穿衣指数  详细描述
                                elif sub_dict.get('type', "") == "flu":
                                    weather_data['flu_brf'] = sub_dict.get('brf', "未知")#感冒指数  简介
                                    weather_data['flu_txt'] = sub_dict.get('txt', "未知")#感冒指数  详细描述
                                elif sub_dict.get('type', "") == "sport":
                                    weather_data['sport_brf'] = sub_dict.get('brf', "未知")#运动指数  简介
                                    weather_data['sport_txt'] = sub_dict.get('txt', "未知")#运动指数  详细描述
                                elif sub_dict.get('type', "") == "trav":
                                    weather_data['trav_brf'] = sub_dict.get('brf', "未知")#旅游指数  简介
                                    weather_data['trav_txt'] = sub_dict.get('txt', "未知")#旅游指数  详细描述
                                elif sub_dict.get('type', "") == "uv":
                                    weather_data['uv_brf'] = sub_dict.get('brf', "未知")#紫外线指数  简介
                                    weather_data['uv_txt'] = sub_dict.get('txt', "未知")#紫外线指数  详细描述
                                elif sub_dict.get('type', "") == "cw":
                                    weather_data['cw_brf'] = sub_dict.get('brf', "未知")#洗车指数  简介
                                    weather_data['cw_txt'] = sub_dict.get('txt', "未知")#洗车指数  详细描述
                                elif sub_dict.get('type', "") == "air":
                                    weather_data['air_brf'] = sub_dict.get('brf', "未知")#空气指数  简介
                                    weather_data['air_txt'] = sub_dict.get('txt', "未知")#空气指数  详细描述

            return (True, weather_data)
        except Exception as e:
            print "Exception:", e
            return (False, weather_data)
        return (False, weather_data)

    def get_heweather_forecast_weather(self, cityid):
        weather_dict = {}
        (ret, weather_dict) = self.access_heweather_forecast_and_observe(cityid)
        return weather_dict

if __name__ == "__main__":

#    string1='1234567'
#    string2=string1[:-1]#去掉尾部一个字符
#    string3=string1[1:-1]#去掉头尾各一个字符
#    string4=string1[1:]#去掉头部一个字符
#    string5='##1234567##'
#    string6=string5.rstrip('#')#去掉尾部所有#
#    string7=string5.strip('#')#去掉头尾所有#
#    string8=string5.lstrip('#')#去掉头部所有#

    app = AppServer()
    dict_data = app.get_heweather_forecast_weather("101250101")
    print "==================dict_data:",dict_data
