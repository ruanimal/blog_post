title: 通过适配器模式优化Python代码
date: June 19, 2016 10:40 PM
categories: 编程
tags: 
----



　　当你维护旧项目的时候，可能要优化一些原有的代码，又不想大改特改。毕竟设计模式的原则是对更改关闭，对扩展开放。假如大改特改势必会引入新的bug，增加测试的工作量。优化代码的目的是提高稳定性和效率，如果引入了新bug就得不偿失了。

　　这时我们**可使用适配器或装饰器，在不改变调用的情况下，优化代码。**
  
<!--more-->

### 旧代码例子

　　比如下面这代码段，封装了一个MySQL的连接，但是**只返回了游标对象（cursor），没有返回连接对象（connnection）**。这样每次调用完这个函数之后，**数据库连接不能关闭**，很可能会导致连接量到达上限，引起性能问题。
```python
import MySQLdb

def mysql_connect():
    conn = MySQLdb.connect(host='localhost',
                         port=3306,
                         user='root',
                         passwd='123456',
                         db='db',
                         charset='utf8',
                         use_unicode=False,
                         unix_socket='/tmp/mysql3306.sock')
    cur = conn.cursor()
    return cur
```


### 使用适配器优化
　　所以我写了一个适配器类，**通过适配器对象包装游标和连接**，并且使`mysql_connect`函数返回适配器对象，以解决连接不能关闭的问题。
　　`MySQLConnectAdapter`适配器组合了`cursor`和`connnection`，**调用`close`方法的时候会同时关闭`cursor`和`connnection`。**重写`__getattribute__`方法，将除`close`之外的属性和方法重定向的`self._cur`对象上，实现对原有调用的兼容。需要注意，**一旦重写`__getattribute__`方法，所以属性和方法查找都会通过自定义的`__getattribute__`，注意防止无穷递归。**


```python
import MySQLdb

class MySQLConnectAdapter(object):
    def __init__(self, conn, cur):
        self._conn = conn
        self._cur = cur

    def __getattribute__(self, name):
        if name in ('close', '_conn', '_cur'):
            return object.__getattribute__(self, name)
        else:
            return object.__getattribute__(self, '_cur').__getattribute__(name)

    def close(self):
        self._cur.close()
        self._conn.close()


def mysql_connect():
    conn = MySQLdb.connect(host='localhost',
                         port=3306,
                         user='root',
                         passwd='123456',
                         db='db',
                         charset='utf8',
                         use_unicode=False,
                         unix_socket='/tmp/mysql3306.sock')
    cur = conn.cursor()
    safe_cur = MySQLConnectAdapter(conn, cur)
    return safe_cur
```