SELECT Host, User, Password, Select_priv, Insert_priv, Update_priv, Delete_priv, Create_priv, Drop_priv, Reload_priv, Shutdown_priv, Process_priv, File_priv, Grant_priv, References_priv, Index_priv, Alter_priv, Show_db_priv, Super_priv, Create_tmp_table_priv, Lock_tables_priv, Execute_priv, Repl_slave_priv, Repl_client_priv, Create_view_priv, Show_view_priv, Create_routine_priv, Alter_routine_priv, Create_user_priv, Event_priv, Trigger_priv, ssl_type, ssl_cipher, x509_issuer, x509_subject, max_questions, max_updates, max_connections, max_user_connections FROM user;

create user 'zkpk'@'localhost' identified by 'zkpk';

GO
use myql;
create database car_data;
GO
use car_data
GO
create user 'crawler'@'localhost' identified by 'crawler';
GO
use mysql;
GO
grant all privileges on car_data.* to 'crawler'@'localhost'  identified by 'crawler';
flush privileges ;

drop database car_data;

GO
create database car_data;
show databases;
GO
grant all privileges on *.* to 'crawler'@'%'  identified by 'crawler';
flush privileges;

GO

show privileges;

CREATE TABLE if not exists
    car_data.province
    (
        `id` INT(11) NOT NULL AUTO_INCREMENT,
         `name` VARCHAR(20),
        `show` VARCHAR(20),
        `url` VARCHAR(200),
        PRIMARY KEY (id)
    )
    ENGINE=InnoDB DEFAULT CHARSET=utf8
    
    
    UPDATE mysql.user SET Password=PASSWORD('root') where USER='root';
    
  GO