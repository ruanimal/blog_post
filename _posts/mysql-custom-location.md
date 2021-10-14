title: MySQL 自定义数据库路径
date: 2021-10-14 8:17 PM
categories: 编程
tags: [MySQL,]

---

*最近的一些文章是整理以前的笔记*
MySQL 是最常用的数据，有时希望将数据库文件存放在自定义路径，或者在系统中启动多个 MySQL服务。
<!--more-->
当然，如果条件允许，建议直接使用 docker 
## 创建 my.cnf 配置文件
```ini
[mysqld]
datadir=/home/ruan/data/mysql_data
socket=/home/ruan/data/mysql.sock
user=ruan
# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0
bind-address=127.0.0.1
port = 12345

character-set-server=utf8
collation-server=utf8_general_ci

[mysqld_safe]
log-error=/home/ruan/data/mysqld.log
pid-file=/home/ruan/data/mysqld.pid
```

## 启动和初始化
```shell
# 启动MySQL
mysqld_safe --defaults-file=my.cnf --user=ruan
# 初始化数据库
mysql_install_db --defaults-file=my.cnf --user=ruan
```

## 目录结构
```
$ tree data
data
├── my.cnf
├── mysql_data
│   ├── ibdata1
│   ├── ib_logfile0
│   ├── ib_logfile1
├── mysqld.log
├── mysqld.pid
└── mysql.sock
```

## 设置密码
```
mysql> use mysql; update user set password=password('m654321') where user='root'; flush privileges;
```