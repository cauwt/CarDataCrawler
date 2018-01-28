create table if not exists car(
`id` bigint not null auto_increment,
`main_brand_id` bigint default null,
`main_brand_name` varchar(10) default null,
`brand_id` bigint default null,
`brand_name` varchar(10) default null,
`serial_id` bigint default null,
`serial_name` varchar(30) default null,
`serial_spell` varchar(10) default null,
`serial_show_name` varchar(50) default null,
`car_id` bigint default null,
`car_name` varchar(200) default null,
`car_gear` varchar(20) default null,
`car_engine_displacement` varchar(50) default null,
`car_msrp` decimal(10,4) default null,
`car_sale_year` varchar(10) default null,
`create_time` datetime default null,
primary key (`id`)
) engine = InnoDB default charset=utf8 auto_increment =1
