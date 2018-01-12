-- [Name],[Show],[URL],[CreateTime]
create table if not exists province(
`id` int(11) unsigned not null auto_increment,
`name` varchar(20) default null,
`show` varchar(20) default null,
`url` varchar(300) default null,
`create_time` datetime default null,
primary key (`id`)
) engine = InnoDB default charset=utf8 auto_increment =1
