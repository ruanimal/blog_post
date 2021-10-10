title: SQLAlchemy ORM 使用教程
date: 2019-10-26 8:17 PM
categories: 编程
tags: [SQLAlchemy, Python, ORM]

---
ORM是指对象关系映射（英语：Object Relational Mapping），是一种程序设计技术，是数据库记录和程序对象之间的映射关系。

使用ORM可以简化数据库的操作，使数据操作更加面向对象，并且程序逻辑和具体数据库解耦。缺点是会有一定的性能损耗。

Python中的ORM主要有Django ORM，SQLAlchemy, peewee； 其中Django ORM只能和Django框架一起使用，SQLAlchemy功能比较全，peewee较为轻量。

SQLAlchemy还可以不使用其ORM，只使用SQLAlchemy core作为一个通用数据库连接器。

<!--more-->

## 关系映射
### 创建model
```python
from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SomeData(Base):
    __tablename__ = 'table11'
    __table_args__ = (
        Index('message_idx', 'message'),
    )
    
    id = Column(Integer, primary_key=True)
    status = Column('status', String(4) , comment='状态', quote=True)   # 转义关键字
    message = Column(String(50), comment='描述',)
    the_time = Column(DateTime, comment='请求时间', index=True)
    cost_time = Column(String(8), comment='请求耗时',)
    # created_at = Column(TIMESTAMP, comment='创建时间', server_default=text('CURRENT_TIMESTAMP'))
```

### 数据库URI
SQLAlchemy使用类似`sqlite:///test.sqlite3`的URI来表示数据库连接
格式为：`dialect+driver://username:password@host:port/database`, 具体查看[官方文档](https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls)

### 生成Model对应数据表
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///test.sqlite3', echo=True)
Base.metadata.create_all(engine)  # 如果表不存在，则生成
```

### 自动映射已存在的数据表
```Python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

Base = automap_base()

dbname = 'test.sqlite3'
engine = create_engine('sqlite:///' + dbname)

Base.prepare(engine, reflect=True)

Base.classes.keys()  # 所有映射列表

SomeData = Base.classes.table11
```

## 增删查改
### 创建会话session
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///test.sqlite3', echo=True)
Session = sessionmaker(bind=engine)

session = Session()
```

### 插入
```python
# 插入单条
session.add(SomeData(status='1', message='aa'))
# 插入多条
session.add_all([
    SomeData(status='2', message='bb'),
    SomeData(status='2', message='cc'),
])
session.commit()
# session.rollback()  # 也可以回滚
```

### 查询

一些基本查询，更多查看[官方文档](https://docs.sqlalchemy.org/en/13/orm/tutorial.html#common-filter-operators)
```python
## select * from table11
session.query(SomeData).all()
# return: [<__main__.SomeData object at 0x1040e6278>, <__main__.SomeData object at 0x103aa13c8>, <__main__.SomeData object at 0x103aa1438>]

## 通过主键获取数据
session.query(SomeData).get(1)

## select * from table11 where status='2' order by the_time limit 1
data = session.query(SomeData).filter_by(status='2').order_by(SomeData.the_time).first()
# data: <__main__.SomeData object at 0x103aa13c8>

## select * from table11 where status in ('1', '2')
session.query(SomeData).filter(SomeData.status.in_(['1', '2'])).all()

## select status, message from table11
session.query(SomeData.status, SomeData.message).all()
# return: [('1', 'aa'), ('2', 'bb'), ('2', 'cc')]

## 原始sql语句
stmt = text("SELECT message, id, status FROM table11 Where status=:status")
stmt = stmt.columns(SomeData.message, SomeData.id, SomeData.status,)
session.query(SomeData).from_statement(stmt).params(status='1').all()

## 遍历大表，每N条数据请求数据库一次
for p in session.query(SomeData).yield_per(5):
    print(p)
```

多表join查询
```python
>>> for u, a in session.query(User, Address).\
...                     filter(User.id==Address.user_id).\
...                     filter(Address.email_address=='jack@google.com').\
...                     all():
...     print(u)
...     print(a)
<User(name='jack', fullname='Jack Bean', nickname='gjffdd')>
<Address(email_address='jack@google.com')>
```

### 更新
```python
## 更新单条
data = session.query(SomeData).get(1)
data.cost_time = 22
session.commit()

## 批量更新
session.query(SomeData).update({SomeData.cost_time: '3456'})
session.commit()
```

### 删除
```python
session.query(SomeData).filter_by(id=2).delete()
session.commit()
```

## seesion管理最佳实践
```python
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session  # 使session可以用于多线程环境

# pool_recycle 数据库连接的回收周期, 按需调整
# pool_size 连接池大小, 按需调整, 0为不限制连接数
# pool_pre_ping=True 每次从连接池中取出连接时, 都判断是否有效, 可替代pool_recycle参数
# engine = create_engine('mysql://database', pool_pre_ping=True, pool_size=0)
engine = create_engine('sqlite:///test.sqlite3')
Session = scoped_session(sessionmaker(bind=engine))

# session 自动管理
@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

# 使用示例
with get_session() as session:
    session.execute('select 1')
    session.add(SomeData(status='1', message='aa'))
```
