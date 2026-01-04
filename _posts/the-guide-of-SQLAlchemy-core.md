---
title: SQLAlchemy Core 使用教程
date: 2019-10-28 20:17:00
updated: 2021-07-22 16:21:00
categories: 编程
tags: [SQLAlchemy, Python, ORM]
---

SQLAlchemy core 是SQLAlchemy的核心部件，主要负责生成sql查询和具体的数据库操作，SQLAlchemy orm 就是构建在core之上的。

在不需要对象映射的时候，使用core而不是orm，可以降低数据库操作成本，提高性能。

## Table映射
### 创建数据库连接
```python
from sqlalchemy import create_engine
engine = create_engine('sqlite:///test.sqlite3', echo=True)
```

### 表结构定义
```python
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Index
metadata = MetaData()
users = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('fullname', String),
    
    # place an index on col1, col2
    Index('idx_col12', 'name', 'fullname'),   # 添加索引
)

addresses = Table('addresses', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', None, ForeignKey('users.id')),
    Column('email_address', String, nullable=False)
)
```
<!--more-->

### 映射已存在的数据表
```python
# 单个表
>>> from sqlalchemy import Table , MetaData
>>> metadata = MetaData(engine)
>>> users = Table('users', metadata, autoload=True)
>>> users.c.keys()
['id', 'name', 'fullname']

# 整个数据库
>>> metadata.reflect()
>>> addresses = metadata.tables['addresses']
```

### 创建表
```python
from sqlalchemy import MetaData

metadata = MetaData()
metadata.create_all(engine)
```

## 增删查改
### 插入
```python 
## 获得连接对象
conn = engine.connect()

## 插入一条
ins = users.insert().values(name='jack', fullname='Jack Jones')
conn.execute(ins)

ins = users.insert()
conn.execute(ins, name='wendy', fullname='Wendy Williams')

## 批量插入
conn.execute(addresses.insert(), [
    {'user_id': 1, 'email_address' : 'jack@yahoo.com'},
    {'user_id': 1, 'email_address' : 'jack@msn.com'},
])
```

### 查询
基本查询示例，复杂过滤条件查看[文档](https://docs.sqlalchemy.org/en/13/core/tutorial.html#operators)

```python
# select * from users
>>> from sqlalchemy.sql import select
>>> cur = conn.execute(select([users]))
>>> cur.fetchall()
[(1, 'jack', 'Jack Jones'), (2, 'wendy', 'Wendy Williams')]

# select name, fullname from users
>>> cur = conn.execute(select([users.c.name, users.c.fullname]))
>>> cur.fetchall()
[('jack', 'Jack Jones'), ('wendy', 'Wendy Williams')]

# select name, fullname from users limit 1
>>> cur = conn.execute(select([users.c.name, users.c.fullname]).limit(1))
>>> cur.fetchall()
[('jack', 'Jack Jones')]

# 联表查询
# SELECT users.name, addresses.email_address FROM users, addresses WHERE users.id = addresses.user_id
>>> s = select([users.c.name, addresses.c.email_address]).where(users.c.id == addresses.c.user_id)
>>> cur = conn.execute(s)
>>> cur.fetchall()
[('jack', 'jack@yahoo.com'), ('jack', 'jack@msn.com')]

# 原始sql语句
>>> from sqlalchemy.sql import text
... s = text(
...     "SELECT users.fullname, addresses.email_address AS title "
...         "FROM users, addresses "
...         "WHERE users.id = addresses.user_id "
...         "AND users.name BETWEEN :x AND :y "
...         "AND (addresses.email_address LIKE :e1 "
...             "OR addresses.email_address LIKE :e2)")
... conn.execute(s, x='m', y='z', e1='%@aol.com', e2='%@msn.com').fetchall()

## 遍历大表，每N条数据请求数据库一次
for p in conn.execute(select([users])).yield_per(5):
    print(p)
```

### 更改
```python
>>> from sqlalchemy.sql import update, select, delete, insert
# 更改为具体值
>>> stmt = users.update().\
...             where(users.c.name == 'jack').\
...             values(name='ed')
>>> conn.execute(stmt)

# 更改为另一个字段的值
>>> stmt = users.update().values(name=users.c.fullname)
>>> conn.execute(stmt)
```

### 删除
```python
>>> stmt = users.delete().where(users.c.id == 1)
>>> conn.execute(stmt)
```

## 其他特性
### 监听DBAPI事件
监听connect事件，在初始化数据库连接时设置数据库参数变量，或者执行语句
[参考文档](https://docs.sqlalchemy.org/en/13/core/engines.html#modifying-the-dbapi-connection-after-connect-or-running-commands-after-connect)
```python
from sqlalchemy import event

engine = create_engine(
    "postgresql://user:pass@hostname/dbname"
)

@event.listens_for(engine, "connect")
def connect(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("SET some session variables")
    cursor.close()
```