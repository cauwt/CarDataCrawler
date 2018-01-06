create table if not exists main_brand(
`id` int(11) not null,
`name` varchar(40) default null,
`url` varchar(200) default null,
primary key (`id`)
) engine = InnoDB  DEFAULT charset=utf8
