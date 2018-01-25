create table if not exists car_data.promotion_price(
`id`  bigint not null auto_increment,-- 自增主键
`dealer_id` bigint not null,-- 商家id
`dealer_name` varchar(200) default null,-- 商家名称
`model_id` int(11) ,-- 车型id
`model_name` varchar(200),-- 车型名
`model_down_url` varchar(200),-- 车型降价新闻url
`title` varchar(200),-- 降价标题
`publish_date` date,-- 发布日期
`begin_date` date,-- 开始日期
`end_date` date,-- 结束日期
`style_id` int(11),-- 车款ID
`style_name` varchar(200),-- 车款
`style_msrp` varchar(50),-- 厂商指导价
`style_promo` varchar(50),-- 降价
`style_price` varchar(50),-- 价格
`style_store` varchar(50),-- 库存
`create_time` datetime,-- 时间
primary key (`id`)
) engine = InnoDB default charset=utf8 auto_increment =1
