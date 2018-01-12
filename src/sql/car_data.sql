update crawl_log set complete_success = 1, end_time = now() where id = (select id from ( select max(id) as id from crawl_log as a where project_name='易车商家抓取') as s)
