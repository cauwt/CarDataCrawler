-- INSERT INTO dbo.tbCrawlCompleteFlat (ProjectName,CompleteSuccess,StartTime)

create table if not exists crawl_log (
`id` int(11) unsigned not null auto_increment,
`project_name` varchar(20) default null,
`complete_success` smallint not null default 0,
`start_time` datetime default null,
`end_time` datetime default null,
primary key (`id`)
) engine = InnoDB DEFAULT charset=utf8 auto_increment =1