select * from main_brand

select distinct `name`, `show` from province

select * from crawl_log where id = (select max(id) from crawl_log where project_name='易车商家抓取')
select * from crawl_log

update crawl_log set complete_success = 1, end_time = now() where id = (
select id from ( select max(id) as id from crawl_log as a where project_name='易车商家抓取'
) as s
)

GO
delete from main_brand;
delete from province;
delete from crawl_log;
delete from dealer_raw;

select count(*) from dealer_raw
