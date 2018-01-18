insert into main_brand(`id`,`name`,`url`) values(9,'奥迪','/tree/mb/9')

delete from main_brand

-- dealer_raw
insert into dealer_raw(
`main_brand_id`,`main_brand_name`,`main_brand_show`,`brand_name`,`brand_show`,`province_name`,`province_show`,
`city_name`,`location_name`,`dealer_type`,`dealer_url`,`dealer_name`,`dealer_id`,`dealer_brand`,`dealer_pro_title`,
`dealer_pro_url`,`dealer_pro_day`,`dealer_add`,`dealer_tel`,`sale_area`,`url`,`create_time`
)
values(
2,'奥迪','audi','奥迪A6','audia6','北京','beijing',
'北京','北京','4S店','http://dealer.bitauto.com/10005227','奥迪腾达店',10005227,'dealer_raw','年终大促',
'http://dealer.bitauto.com/10005227/news/2000111223','20','西直门外大街25号向南100米','400-880-0134','京津冀','http://dealer.bitauto.com/10005227',now()
)
select * from dealer_raw

GO
-- promotion_price
insert into car_data.promotion_price (dealer_id, dealer_name, model_id, model_name, model_down_url, title, publish_date, begin_date, end_date, style_id, style_name, style_msrp, style_promo, style_price,  style_store, create_time)
values( 10005227, '奥迪腾达店', 2353, '奥迪A6', 'http://dealer.bitauto.com/10005227/audia6', '年终大促',
        '2018-1-12', '2018-1-12', '2018-2-10', 130256, '2018款 奥迪A6 2018 标准版', '23.25', '22.25', '23.25',
        '库存充足', now())