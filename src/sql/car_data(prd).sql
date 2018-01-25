SELECT
    Host,
    USER,
    Password,
    Select_priv,
    Insert_priv,
    Update_priv,
    Delete_priv,
    Create_priv,
    Drop_priv,
    Reload_priv,
    Shutdown_priv,
    Process_priv,
    File_priv,
    Grant_priv,
    References_priv,
    Index_priv,
    Alter_priv,
    Show_db_priv,
    Super_priv,
    Create_tmp_table_priv,
    Lock_tables_priv,
    Execute_priv,
    Repl_slave_priv,
    Repl_client_priv,
    Create_view_priv,
    Show_view_priv,
    Create_routine_priv,
    Alter_routine_priv,
    Create_user_priv,
    Event_priv,
    Trigger_priv,
    ssl_type,
    ssl_cipher,
    x509_issuer,
    x509_subject,
    max_questions,
    max_updates,
    max_connections,
    max_user_connections
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
 
 show create table promotion_price;