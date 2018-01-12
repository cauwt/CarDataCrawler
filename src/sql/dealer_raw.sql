-- INSERT INTO dbo.tbYiCheDealertest

create table if not exists dealer_raw (
`id` int(11) not null auto_increment comment '自增主键' ,
`main_brand_id` INT(11) default null comment '品牌ID',
`main_brand_name` varchar(50) default null comment '品牌',
`main_brand_show` VARCHAR(50) default null comment '品牌拼音',

`brand_name` varchar(50) default null comment '品牌',
`brand_show` VARCHAR(50) default null comment '品牌拼音',

`province_name` varchar(50) default null comment '省份名称',
`province_show` varchar(50) default null comment '省份拼音',

`city_name` varchar(50) default null comment '城市名称',

`location_name`varchar(50) default null comment '区县名称',

`dealer_type` VARCHAR(50) default null comment '商家类型',
`dealer_url` VARCHAR(200) default null comment '商家url',
`dealer_name` varchar(100) default null comment '商家名字',
`dealer_id` BIGINT(11)  default null comment '商家ID',
`dealer_brand` varchar(500) default null comment '商家主营品牌',
`dealer_pro_title` varchar(500) default null comment '商家正在进行中的降价新闻标题',
`dealer_pro_url` varchar(200) default null comment '商家正在进行中的降价新闻Url',
`dealer_pro_day` varchar(50) default null comment '剩余天数',
`dealer_add` varchar(500) default null comment '商家地址',
`dealer_tel`  VARCHAR(50) default null comment '商家电话',
`sale_area` varchar(50) default null comment '售卖地区',
`url`  varchar(200) default null comment '抓取页面',
`create_time` datetime default null comment '抓取时间',
primary key (`id`)
) engine = InnoDB DEFAULT charset=utf8 auto_increment =1
