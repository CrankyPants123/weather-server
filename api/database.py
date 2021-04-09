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

CREATE_OBSERVE = "CREATE TABLE IF NOT EXISTS observe (id varchar(32) primary key not null,city varchar(64), \
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

CREATE_FORECAST3D = "CREATE TABLE IF NOT EXISTS forecast3d (id varchar(32) primary key not null,city_zh varchar(64),city_name_zh varchar(64), \
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



CREATE_FORECAST6D = "CREATE TABLE IF NOT EXISTS forecast6d (cityid varchar(32) primary key not null,city varchar(64),city_en varchar(64), \
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
CREATE_HEWEATHER_FORECAST = "CREATE TABLE IF NOT EXISTS heforecast (cityid varchar(32) primary key not null,city varchar(64),prov varchar(64),cnty varchar(64),update_time varchar(64),insert_time varchar(64), \
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




#all: https://free-api.heweather.com/s6/weather?location=CN101250101&key=4ff2e595e593439380e52d2519523d0a
#now(在all里面存在，可不单独获取): https://free-api.heweather.com/s6/weather/now?location=CN101250101&key=4ff2e595e593439380e52d2519523d0a
#20180827 heweather s6 version   http://www.heweather.com/documents/api/s6/weather-now
CREATE_HEWEATHER_OBSERVE_S6 = "CREATE TABLE IF NOT EXISTS heweather_observe (id varchar(32) primary key not null,location varchar(64), \
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
CREATE_HEWEATHER_AIR_S6 = "CREATE TABLE IF NOT EXISTS heweather_air (id varchar(32) primary key not null,location varchar(64),pub_time varchar(32), \
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
CREATE_HEWEATHER_FORECAST_S6 = "CREATE TABLE IF NOT EXISTS heweather_forecast (id varchar(32) primary key not null,location varchar(64),update_loc varchar(32), \
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
CREATE_HEWEATHER_LIFESTYLE_S6 = "CREATE TABLE IF NOT EXISTS heweather_lifestyle (id varchar(32) primary key not null, \
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






# -------------------------20200307-------------------------
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
# -------------------------20200307-------------------------




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

    def init_forecast3d_table(self):
        self.cursor.execute(CREATE_FORECAST3D)

    def init_forecast6d_table(self):
        self.cursor.execute(CREATE_FORECAST6D)

    def init_observe_table(self):
        self.cursor.execute(CREATE_OBSERVE)

    #20170627
    def init_heweather_forecast_table(self):
        self.cursor.execute(CREATE_HEWEATHER_FORECAST)



    #-------------------------20180827 heweather s6 version-------------------------------
    def init_heweather_air_s6_table(self):
        self.cursor.execute(CREATE_HEWEATHER_AIR_S6)

    def init_heweather_observe_s6_table(self):
        self.cursor.execute(CREATE_HEWEATHER_OBSERVE_S6)

    def init_heweather_forecast_s6_table(self):
        self.cursor.execute(CREATE_HEWEATHER_FORECAST_S6)

    def init_heweather_lifestyle_s6_table(self):
        self.cursor.execute(CREATE_S6_HEWEATHER_LIFESTYLE)





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












    # ------------------observe------------------
    def search_observe_record(self, id):
        self.cursor.execute(QUERY_OBSERVE % (id))
        res = self.cursor.fetchall()
        if len(res) == 0:
            return []
        else:
            return res

    def search_observe_record_update_time(self, id):
        self.cursor.execute(QUERY_TIME_OBSERVE % (id))
        res = self.cursor.fetchall()
        if len(res) == 0:
            return []
        else:
            return res

    def insert_observe_data(self,id,city,ptime,time,update_time,WD,WS,SD,weather,img1,img2,temp,temp1,temp2,aqi):
        self.cursor.execute(INSERT_OBSERVE % (id,str(city),str(ptime),str(time),update_time,str(WD),str(WS),str(SD),str(weather),str(img1),str(img2),str(temp),str(temp1),str(temp2),str(aqi)))
        self.connect.commit()

    def update_observe_data(self,ptime,time,update_time,WD,WS,SD,weather,img1,img2,temp,temp1,temp2,aqi,id):
        self.cursor.execute(UPDATE_OBSERVE % (str(ptime),str(time),update_time,str(WD),str(WS),str(SD),str(weather),str(img1),str(img2),str(temp),str(temp1),str(temp2),str(aqi),id))
        self.connect.commit()


    # ------------------forecast3d------------------
    def search_forecast3d_record(self, id):
        self.cursor.execute(QUERY_FORECAST3D % (id))
        res = self.cursor.fetchall()
        if len(res) == 0:
            return []
        else:
            return res

    def search_forecast3d_record_update_time(self, id):
        self.cursor.execute(QUERY_TIME_FORECAST3D % (id))
        res = self.cursor.fetchall()
        if len(res) == 0:
            return []
        else:
            return res

    def insert_forecast3d_data(self,id,city_zh,city_name_zh,province_zh,country_zh,city_level,area_code,zip_code, \
                             longitude,latitude,altitude,radar_station,time_zone,release_time,update_time,language,sunrise_sunset_1, \
                             d1_weaher,n1_weaher,d1_temperature,n1_temperature,d1_wind_direction,n1_wind_direction, \
                             d1_wind_power,n1_wind_power,sunrise_sunset_2,d2_weaher,n2_weaher,d2_temperature,n2_temperature, \
                             d2_wind_direction,n2_wind_direction,d2_wind_power,n2_wind_power,sunrise_sunset_3,d3_weaher, \
                             n3_weaher,d3_temperature,n3_temperature,d3_wind_direction,n3_wind_direction,d3_wind_power, \
                             n3_wind_power,city_en,city_name_en,province_en,country_en):

        self.cursor.execute(INSERT_FORECAST3D % (id,city_zh,city_name_zh,province_zh,country_zh,city_level,area_code,zip_code, \
                                               longitude,latitude,altitude,radar_station,time_zone,release_time,update_time,language,sunrise_sunset_1, \
                                               d1_weaher,n1_weaher,d1_temperature,n1_temperature,d1_wind_direction,n1_wind_direction, \
                                               d1_wind_power,n1_wind_power,sunrise_sunset_2,d2_weaher,n2_weaher,d2_temperature,n2_temperature, \
                                               d2_wind_direction,n2_wind_direction,d2_wind_power,n2_wind_power,sunrise_sunset_3,d3_weaher, \
                                               n3_weaher,d3_temperature,n3_temperature,d3_wind_direction,n3_wind_direction,d3_wind_power, \
                                               n3_wind_power,city_en,city_name_en,province_en,country_en))
        self.connect.commit()

    def update_forecast3d_data(self,longitude,latitude,altitude,radar_station,time_zone,release_time,update_time, \
                             sunrise_sunset_1,d1_weaher,n1_weaher,d1_temperature,n1_temperature,d1_wind_direction, \
                             n1_wind_direction,d1_wind_power,n1_wind_power,sunrise_sunset_2,d2_weaher,n2_weaher, \
                             d2_temperature,n2_temperature,d2_wind_direction,n2_wind_direction,d2_wind_power, \
                             n2_wind_power,sunrise_sunset_3,d3_weaher,n3_weaher,d3_temperature,n3_temperature, \
                             d3_wind_direction,n3_wind_direction,d3_wind_power,n3_wind_power,id):
        self.cursor.execute(UPDATE_FORECAST3D % (longitude,latitude,altitude,radar_station,time_zone,release_time,update_time, \
                                               sunrise_sunset_1,d1_weaher,n1_weaher,d1_temperature,n1_temperature,d1_wind_direction, \
                                               n1_wind_direction,d1_wind_power,n1_wind_power,sunrise_sunset_2,d2_weaher,n2_weaher, \
                                               d2_temperature,n2_temperature,d2_wind_direction,n2_wind_direction,d2_wind_power, \
                                               n2_wind_power,sunrise_sunset_3,d3_weaher,n3_weaher,d3_temperature,n3_temperature, \
                                               d3_wind_direction,n3_wind_direction,d3_wind_power,n3_wind_power,id))
        self.connect.commit()





    # ------------------forecast6d------------------
    def search_forecast6d_record(self, cityid):
        self.cursor.execute(QUERY_FORECAST6D % (cityid))
        res = self.cursor.fetchall()
        if len(res) == 0:
            return []
        else:
            return res

    def search_forecast6d_record_update_time(self, cityid):
        self.cursor.execute(QUERY_TIME_FORECAST6D % (cityid))
        res = self.cursor.fetchall()
        if len(res) == 0:
            return []
        else:
            return res

    def insert_forecast6d_data(self,cityid,city,city_en,date_y,date,week,fchh,update_time, \
                               temp1,temp2,temp3,temp4,temp5,temp6,tempF1,tempF2,tempF3,tempF4,tempF5,tempF6, \
                               weather1,weather2,weather3,weather4,weather5,weather6,img1,img2,img3,img4,img5,img6, \
                               img7,img8,img9,img10,img11,img12,img_single,img_title_single, \
                               img_title1,img_title2,img_title3,img_title4,img_title5,img_title6, \
                               img_title7,img_title8,img_title9,img_title10,img_title11,img_title12, \
                               wind1,wind2,wind3,wind4,wind5,wind6,fx1,fx2,fl1,fl2,fl3,fl4,fl5,fl6, \
                               index_clothes,index_d,index_uv,index_xc,index_tr,index_co,index_cl,index_ls,index_ag):
        self.cursor.execute(INSERT_FORECAST6D % (cityid,city,city_en,date_y,date,week,fchh,update_time, \
                                               temp1,temp2,temp3,temp4,temp5,temp6,tempF1,tempF2,tempF3,tempF4,tempF5,tempF6, \
                                               weather1,weather2,weather3,weather4,weather5,weather6,img1,img2,img3,img4,img5,img6, \
                                               img7,img8,img9,img10,img11,img12,img_single,img_title_single, \
                                               img_title1,img_title2,img_title3,img_title4,img_title5,img_title6, \
                                               img_title7,img_title8,img_title9,img_title10,img_title11,img_title12, \
                                               wind1,wind2,wind3,wind4,wind5,wind6,fx1,fx2,fl1,fl2,fl3,fl4,fl5,fl6, \
                                               index_clothes,index_d,index_uv,index_xc,index_tr,index_co,index_cl,index_ls,index_ag))
        self.connect.commit()

    def update_forecast6d_data(self,date_y,date,week,fchh,update_time, \
                             temp1,temp2,temp3,temp4,temp5,temp6,tempF1,tempF2,tempF3,tempF4,tempF5,tempF6, \
                             weather1,weather2,weather3,weather4,weather5,weather6,img1,img2,img3,img4,img5,img6, \
                             img7,img8,img9,img10,img11,img12,img_single,img_title_single, \
                             img_title1,img_title2,img_title3,img_title4,img_title5,img_title6, \
                             img_title7,img_title8,img_title9,img_title10,img_title11,img_title12, \
                             wind1,wind2,wind3,wind4,wind5,wind6,fx1,fx2,fl1,fl2,fl3,fl4,fl5,fl6, \
                             index_clothes,index_d,index_uv,index_xc,index_tr,index_co,index_cl,index_ls,index_ag,cityid):
        self.cursor.execute(UPDATE_FORECAST6D % (date_y,date,week,fchh,update_time, \
                                               temp1,temp2,temp3,temp4,temp5,temp6,tempF1,tempF2,tempF3,tempF4,tempF5,tempF6, \
                                               weather1,weather2,weather3,weather4,weather5,weather6,img1,img2,img3,img4,img5,img6, \
                                               img7,img8,img9,img10,img11,img12,img_single,img_title_single, \
                                               img_title1,img_title2,img_title3,img_title4,img_title5,img_title6, \
                                               img_title7,img_title8,img_title9,img_title10,img_title11,img_title12, \
                                               wind1,wind2,wind3,wind4,wind5,wind6,fx1,fx2,fl1,fl2,fl3,fl4,fl5,fl6, \
                                               index_clothes,index_d,index_uv,index_xc,index_tr,index_co,index_cl,index_ls,index_ag,cityid))
        self.connect.commit()

    # ------------------heweather------------------
    def search_heweather_forecast_record(self, cityid):
        self.cursor.execute(QUERY_HEWEATHER_FORECAST % (cityid))
        res = self.cursor.fetchall()
        if len(res) == 0:
            return []
        else:
            return res

    def search_heweather_forecast_record_update_time(self, cityid):
        self.cursor.execute(QUERY_TIME_HEWEATHER_FORECAST % (cityid))
        res = self.cursor.fetchall()
        if len(res) == 0:
            return []
        else:
            return res

    def insert_heweather_forecast_data(self, dict_data, now_date):
        self.cursor.execute(INSERT_HEWEATHER_FORECAST % (dict_data['cityid'],dict_data['city'],dict_data['prov'],dict_data['cnty'],dict_data['update_time'],now_date, \
                                               dict_data['date0'],dict_data['astro_mr0'],dict_data['astro_ms0'],dict_data['astro_sr0'],dict_data['astro_ss0'],dict_data['code_d0'],dict_data['code_n0'],dict_data['txt_d0'],dict_data['txt_n0'], \
                                               dict_data['hum0'],dict_data['pcpn0'],dict_data['pop0'],dict_data['pres0'],dict_data['tmp_max0'],dict_data['tmp_min0'],dict_data['uv0'],dict_data['vis0'],dict_data['wind_deg0'],dict_data['wind_dir_sc0'],dict_data['wind_spd0'], \
                                               dict_data['date1'],dict_data['astro_mr1'],dict_data['astro_ms1'],dict_data['astro_sr1'],dict_data['astro_ss1'],dict_data['code_d1'],dict_data['code_n1'],dict_data['txt_d1'],dict_data['txt_n1'], \
                                               dict_data['hum1'],dict_data['pcpn1'],dict_data['pop1'],dict_data['pres1'],dict_data['tmp_max1'],dict_data['tmp_min1'],dict_data['uv1'],dict_data['vis1'],dict_data['wind_deg1'],dict_data['wind_dir_sc1'],dict_data['wind_spd1'], \
                                               dict_data['date2'],dict_data['astro_mr2'],dict_data['astro_ms2'],dict_data['astro_sr2'],dict_data['astro_ss2'],dict_data['code_d2'],dict_data['code_n2'],dict_data['txt_d2'],dict_data['txt_n2'], \
                                               dict_data['hum2'],dict_data['pcpn2'],dict_data['pop2'],dict_data['pres2'],dict_data['tmp_max2'],dict_data['tmp_min2'],dict_data['uv2'],dict_data['vis2'],dict_data['wind_deg2'],dict_data['wind_dir_sc2'],dict_data['wind_spd2'], \
                                               dict_data['comf_brf'],dict_data['comf_txt'],dict_data['cw_brf'],dict_data['cw_txt'],dict_data['drsg_brf'],dict_data['drsg_txt'],dict_data['flu_brf'],dict_data['flu_txt'],dict_data['sport_brf'],dict_data['sport_txt'],dict_data['trav_brf'],dict_data['trav_txt'],dict_data['uv_brf'],dict_data['uv_txt']))
        self.connect.commit()

    def update_heweather_forecast_data(self, dict_data, now_date):
        self.cursor.execute(UPDATE_HEWEATHER_FORECAST % (dict_data['update_time'],now_date, \
                                                dict_data['date0'],dict_data['astro_mr0'],dict_data['astro_ms0'],dict_data['astro_sr0'],dict_data['astro_ss0'],dict_data['code_d0'],dict_data['code_n0'],dict_data['txt_d0'],dict_data['txt_n0'], \
                                                dict_data['hum0'],dict_data['pcpn0'],dict_data['pop0'],dict_data['pres0'],dict_data['tmp_max0'],dict_data['tmp_min0'],dict_data['uv0'],dict_data['vis0'],dict_data['wind_deg0'],dict_data['wind_dir_sc0'],dict_data['wind_spd0'], \
                                                dict_data['date1'],dict_data['astro_mr1'],dict_data['astro_ms1'],dict_data['astro_sr1'],dict_data['astro_ss1'],dict_data['code_d1'],dict_data['code_n1'],dict_data['txt_d1'],dict_data['txt_n1'], \
                                                dict_data['hum1'],dict_data['pcpn1'],dict_data['pop1'],dict_data['pres1'],dict_data['tmp_max1'],dict_data['tmp_min1'],dict_data['uv1'],dict_data['vis1'],dict_data['wind_deg1'],dict_data['wind_dir_sc1'],dict_data['wind_spd1'], \
                                                dict_data['date2'],dict_data['astro_mr2'],dict_data['astro_ms2'],dict_data['astro_sr2'],dict_data['astro_ss2'],dict_data['code_d2'],dict_data['code_n2'],dict_data['txt_d2'],dict_data['txt_n2'], \
                                                dict_data['hum2'],dict_data['pcpn2'],dict_data['pop2'],dict_data['pres2'],dict_data['tmp_max2'],dict_data['tmp_min2'],dict_data['uv2'],dict_data['vis2'],dict_data['wind_deg2'],dict_data['wind_dir_sc2'],dict_data['wind_spd2'], \
                                                dict_data['comf_brf'],dict_data['comf_txt'],dict_data['cw_brf'],dict_data['cw_txt'],dict_data['drsg_brf'],dict_data['drsg_txt'],dict_data['flu_brf'],dict_data['flu_txt'],dict_data['sport_brf'],dict_data['sport_txt'],dict_data['trav_brf'],dict_data['trav_txt'],dict_data['uv_brf'],dict_data['uv_txt'],dict_data['cityid']))
        self.connect.commit()

if __name__ == "__main__":
    db = DataBase()
#    db.init_heweather_forecast_table()
#    db.init_forecast3d_table()
#    db.init_observe_table()
#    db.init_forecast6d_table()


#    db.init_heweather_air_s6_table()
#    db.init_heweather_observe_s6_table()
#    db.init_heweather_forecast_s6_table()
#    db.init_heweather_lifestyle_s6_table()

    #20200307 create new database table
    db.init_s6_heweather_now_and_forecast_table()
    db.init_s6_heweather_lifestyle_table()
