CREATE DATABASE travel_spider DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
create  table poi_detail(
id  varchar(1000) COMMENT 'id',
head  varchar(1000) COMMENT '层级信息',
title  varchar(1000) COMMENT '中文名称',
title_en  varchar(1000) COMMENT '英文名称',
rank  varchar(1000) COMMENT '排名',
poi_detail  varchar(4000) COMMENT '详情',
poi_tips  varchar(4000) COMMENT '描述',
address  varchar(1000) COMMENT '地址',
arrive_method  varchar(1000) COMMENT '到达方式',
open_time  varchar(1000) COMMENT '开放时间',
ticket  varchar(1000) COMMENT '门票',
phone  varchar(1000) COMMENT '电话',
website  varchar(1000) COMMENT '网址',
poi_tip_content  varchar(1000) COMMENT '小提示',
url varchar(300) comment '网址'
) comment = 'poi详情';
