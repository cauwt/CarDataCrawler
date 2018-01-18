create database car_data
GO
select distinct dealer_id,dealer_name,dealer_url from car_data.dealer_raw where cast(create_time as date)=cast(now() as date)
GO
"INSERT INTO dbo.tbYiCheCutPrice ([DealerID],[Dealername],[Modelid] ,[Modelname],[Modeldowmurl],[Title],[PublishDate],[BeginDate],[EndDate],[StyleID],[Stylename],[Stylemsrp],[Stylepro],[Styleprice],[Stylestore],[CreateTime] )"
GO
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

INSERT INTO promotion_price (id, dealer_id, dealer_name, Modelid, model_name, model_down_url, title, publish_date, begin_date, end_date, style_id, style_name, style_msrp, style_promo, style_price, style_store, create_time) VALUES (0, 0, '', 0, '', '', '', '', '', '', 0, '', '', '', '', '', '');
insert into car_data.promotion_price (dealer_id, dealer_name, model_id, model_name, model_down_url, title, publish_date, begin_date, end_date, style_id, style_name, style_msrp, style_promo, style_price,  style_store, create_time) 
values( 10005227, '奥迪腾达店', 2353, '奥迪A6', 'http://dealer.bitauto.com/10005227/audia6', '年终大促',
        '2018-1-12', '2018-1-12', '2018-2-10', 130256, '2018款 奥迪A6 2018 标准版', '23.25', '22.25', '23.25',
        '库存充足', now())
        
 select * from car_data.promotion_price
 
