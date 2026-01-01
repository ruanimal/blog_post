---
title: MySQL 表分区使用
date: 2021-10-10 15:00:00
updated: 2021-10-10 23:11:39
categories: 编程
tags: [MySQL,]

---
使用MySQL数据库时，当表的数据条数比较大时（1000w以上），数据查询会很慢，索引的效果也不好。

这时我们可以把表的数据分区存储，安装数据值的前缀或者时间字段来分区。
<!--more-->
## 建表
```
CREATE TABLE test_part (
    appid int(11),
    val int(11),
    username VARCHAR(25) NOT NULL,
    start_time DATETIME
)
PARTITION BY RANGE (TO_DAYS(start_time) )(
    PARTITION p20190305 VALUES LESS THAN (TO_DAYS('2019-03-06 00:00:00') )
)
```

## 删除分区
alter table test_part drop partition p1;

不可以删除hash或者key分区。

一次性删除多个分区，alter table test_part drop partition p1,p2;

## 增加分区
ALTER TABLE test_part ADD partition (partition p20190306 VALUES LESS THAN (TO_DAYS('2019-03-07 00:00:00')));  


## 生成测试数据
创建储存过程
```
DROP PROCEDURE IF EXISTS proc1;
DELIMITER $$
SET AUTOCOMMIT = 0$$
CREATE  PROCEDURE proc1()
BEGIN
DECLARE v_cnt DECIMAL (10)  DEFAULT 0 ;
dd:LOOP
    INSERT  INTO test_part VALUES (
        FLOOR(RAND()*100), 
        FLOOR(RAND()*1000), 
        UUID(), 
        DATE_ADD('2019-03-04 00:00:00', INTERVAL FLOOR(v_cnt / 5000) MINUTE)
    );
    COMMIT;
    SET v_cnt = v_cnt+1 ;
        IF  v_cnt = 10000000 THEN LEAVE dd;
        END IF;
    END LOOP dd ;
END;$$
DELIMITER ;
``` 

调用储存过程
```
 call proc1;
```
