CREATE DATABASE travel_spider DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
create  table poi_detail(
id  varchar(100) COMMENT 'id',
catename  varchar(100) COMMENT '活动类型',
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


create table lvmamam_poi_detail(
country  varchar(1000)  comment '',
head  varchar(1000)  comment ' 头',
title  varchar(1000)  comment ' 中文标题',
title_en  varchar(1000)  comment ' 英文标题',
vcomon  varchar(1000)  comment ' 景点类型',
active  varchar(1000)  comment ' 活动内容',
poi_detail  text  comment ' 景点导览',
poi_brief  text  comment ' 景点介绍',
address  varchar(1000)  comment ' 地　　址',
arrive_method  varchar(1000)  comment '',
open_time  varchar(1000)  comment ' 开放时间',
playtime  varchar(1000)  comment ' 游玩时间',
website  varchar(1000)  comment '官方网址',
traffic  varchar(1000)  comment ' 交通',
ticket  varchar(1000)  comment ' 门票说明',
phone  varchar(1000)  comment ' 联系电话：',
poi_tip_content  varchar(4000)  comment ' 小贴士',
url  varchar(1000)  comment ''
) comment 'lvmama poi详情';


CREATE table haoqiao_hotel_list (
title  varchar(200) comment '酒店名',
title_en  varchar(200) comment '酒店英文名',
city  varchar(200) comment '所在城市',
city_id  varchar(200) comment 'city id',
url  varchar(500)
) comment '好巧酒店列表';

CREATE table ctrip_hotel_list (
title  varchar(200) comment '酒店名',
title_en  varchar(200) comment '酒店英文名',
city  varchar(200) comment '所在城市',
city_id  varchar(200) comment 'city id',
url  varchar(500)
) comment '携程酒店列表';


