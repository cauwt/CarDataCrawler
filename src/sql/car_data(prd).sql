SELECT
    Host,
    USER,
    Password
FROM
    USER;
CREATE USER 'zkpk'@'localhost' IDENTIFIED BY 'zkpk';
GO USE myql;
CREATE database car_data;
GO USE car_data GO
CREATE USER 'crawler'@'localhost' IDENTIFIED BY 'crawler';
GO USE mysql;
GO GRANT ALL PRIVILEGES ON car_data.* TO 'crawler'@'localhost' IDENTIFIED BY 'crawler';
flush PRIVILEGES ;
DROP database car_data;
GO CREATE database car_data;
show databases;
GO GRANT ALL PRIVILEGES ON *.* TO 'crawler'@'%' IDENTIFIED BY 'crawler';
flush PRIVILEGES;
GO
show PRIVILEGES;
CREATE TABLE
    IF NOT EXISTS car_data.province
    (
        `id` INT(11) NOT NULL AUTO_INCREMENT,
        `name` VARCHAR(20),
        `show` VARCHAR(20),
        `url` VARCHAR(200),
        PRIMARY KEY (id)
    )
    ENGINE=InnoDB DEFAULT CHARSET=utf8
UPDATE
    mysql.user
SET
    Password=PASSWORD('root')
WHERE
    USER='root';
GO
SELECT
    COUNT(*)
FROM
    dealer_raw;
SELECT
    *
FROM
    promotion_price limit 100;
    
SELECT
    CAST(create_time AS DATE) AS create_date,
    COUNT(*) as cnt
FROM
    promotion_price
GROUP BY
    CAST(create_time AS DATE) ;
    
SELECT
    *
FROM
    promotion_price
WHERE
    create_time >=CAST('2018-1-23' AS DATETIME) limit 100
    
 show create table dealer_raw;
 
 select * from dealer_raw where id = 3808
select m.* from dealer_raw as m
where m.dealer_id in (select s. dealer_id from dealer_raw as  s group by s.dealer_id having count(*) >1 )
order by m.dealer_id
drop table if exists dealer
 --发现有重复的dealer，所以，需要首先去除重复的dealer，原因：经营多个主品牌
create table if not exists dealer as 
SELECT distinct dealer_id, province_name, city_name, location_name, dealer_type,dealer_url, dealer_name, dealer_brand, dealer_add, dealer_tel FROM dealer_raw

create temporary table tmp_dealer as 
SELECT distinct dealer_id, province_name, city_name, location_name, dealer_type, dealer_name, dealer_brand, dealer_add, dealer_tel, sale_area FROM dealer_raw
create temporary table tmp_dealer2 as 
SELECT distinct dealer_id, province_name, city_name, location_name, dealer_type, dealer_name, dealer_brand, dealer_add, dealer_tel, sale_area FROM dealer_raw
drop table if exists tmp_dealer
drop table if exists tmp_dealer2

select * from tmp_dealer as m where m.dealer_id in (select s. dealer_id from tmp_dealer2 as  s group by s.dealer_id having count(*) >1 )

select count(*) from (SELECT distinct dealer_id, province_name, city_name, location_name, dealer_type, dealer_name, dealer_brand, dealer_add, dealer_tel, sale_area FROM dealer_raw) s;

select count(distinct dealer_id) from dealer_raw

select * from promotion_price limit 10;
GO
--创建表格 car
-- 见car.sql
INSERT INTO car_data.car ( main_brand_id, main_brand_name, brand_id, brand_name, serial_id, serial_name, serial_spell, serial_show_name, car_id, car_name, car_gear, car_engine_displacement, car_msrp, car_sale_year, create_time) VALUES ( 0, '', 0, '', 0, '', '', '', 0, '', '', '', 0, '', now());

