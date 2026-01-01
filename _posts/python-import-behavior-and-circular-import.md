---
title: 循环import导致的模块被多次import
date: 2020-06-20 09:48:00
updated: 2020-09-20 15:00:10
categories: 编程
tags: [Python, ]

---
## 缘起
循环import是很多Python初学者都会遇到问题，网上有也有很多文章讲解决方法，比如[这篇](https://www.jianshu.com/p/a1e91cc53b07)，不清楚的可以自行查阅，这里就不赘述了。

那么，为啥老司机也会遇到这个问题呢？这段时间一直在搞把redis复刻一个python版本，在复刻代码时就遇到了这个问题。而且我也使用了延迟import，却没能解决。

下面我们来详细分析下

<!--more-->

## 症状
先看两段代码

run.py
```python
import logging
import sys

logging.basicConfig(level='DEBUG', 
    format='[{asctime} {module}.{funcName:<11}] {message}', style='{')
logging.info(sys.modules['__main__'])
logging.info('begin load')

class Server:
    pass

server = Server()

def start():
    from foo import do_someting
    logging.info('call')
    assert not hasattr(server, 'name')
    server.name = 'aaa'
    logging.info(repr(server))
    logging.info('%s\t%s', repr(Server), id(Server))
    do_someting()

logging.info('end load')

if __name__ == '__main__':
    start()
```

foo.py
```python
import logging
import sys

logging.info('begin load')

def do_someting():
    logging.info('begin call')
    import run

    logging.info(repr(run.server))
    logging.info('%s\t%s', (run.Server), id(run.Server))
    if hasattr(run.server, 'name'):
        logging.info('found attr name')
    else:
        logging.info('not found attr name')
    logging.info('end call')

logging.info('end load')
```

再看执行`python run.py`的结果
```
[2020-06-20 10:57:03,659 run.<module>   ] <module '__main__' from '/Volumes/study/Projects/code_snippet/circular_import/run.py'>
[2020-06-20 10:57:03,659 run.<module>   ] begin load
[2020-06-20 10:57:03,659 run.<module>   ] end load
[2020-06-20 10:57:03,662 foo.<module>   ] begin load
[2020-06-20 10:57:03,662 foo.<module>   ] end load
[2020-06-20 10:57:03,662 run.start      ] call
[2020-06-20 10:57:03,662 run.start      ] <__main__.Server object at 0x1064eb940>
[2020-06-20 10:57:03,662 run.start      ] <class '__main__.Server'> 140250245614784
[2020-06-20 10:57:03,662 foo.do_someting] begin call
[2020-06-20 10:57:03,663 run.<module>   ] <module '__main__' from '/Volumes/study/Projects/code_snippet/circular_import/run.py'>
[2020-06-20 10:57:03,663 run.<module>   ] begin load
[2020-06-20 10:57:03,663 run.<module>   ] end load
[2020-06-20 10:57:03,663 foo.do_someting] <run.Server object at 0x1065d8b50>
[2020-06-20 10:57:03,663 foo.do_someting] <class 'run.Server'>  140250247610512
[2020-06-20 10:57:03,663 foo.do_someting] not found attr name
[2020-06-20 10:57:03,663 foo.do_someting] end call
```

这里已经用延迟导入，这个典型方法，解决了执行时报错的问题

但是，还是可以发现几个问题
1. run.py 被加载了两次
2. 在run模块中的server实例和Server类，与foo模块中的id一样，也就是不是同一个对象。（第8行和14行）

## 分析
先复习下import机制

import 语句结合了两个操作；它先搜索指定名称的模块，然后将搜索结果绑定到当前作用域中的名称。 import 语句的搜索操作定义为对 `__import__()` 函数的调用并带有适当的参数。 `__import__()` 的返回值会被用于执行 import 语句的名称绑定操作。 

对 `__import__()` 的直接调用将仅执行模块搜索以及在找到时的模块创建操作。 不过也可能产生某些副作用，例如导入父包和更新各种缓存 (包括 sys.modules)，只有 import 语句会执行名称绑定操作。

`sys.modules`是一个字典，缓存了已加载的模型，以模块名称为key，模块对象为value。
执行import 语句时，先在`sys.modules`缓存中查询该模块，如已存在者返回该对象，否则从文件系统中加载该模块。

```
[2020-06-20 10:57:03,662 run.start      ] <__main__.Server object at 0x1064eb940>
```
从上面的这行输出可以看出，当run作为程序入口时，模块名称变为了`__main__`, 查看 `sys.modules`，也只发现了`__main__`，没有发现`run`. 
所以， 当`do_someting` import `run` 模块时，肯定是发现没有加载，最终导致加载了两次，Server类id不一致也可以理解了。

## 解决
所以只要能从`sys.modules`正确地找到run模块，问题就可以解决。

具体来说有三种方法

### 方法A
修改foo.py, 把`import run`改为`import __main__ as run`
```python
import logging
import sys

logging.info('begin load')

def do_someting():
    logging.info('begin call')
    import __main__ as run

    logging.info(repr(run.server))
    logging.info('%s\t%s', (run.Server), id(run.Server))
    if hasattr(run.server, 'name'):
        logging.info('found attr name')
    else:
        logging.info('not found attr name')
    logging.info('end call')

logging.info('end load')
```

### 方法B
修改`sys.modules`，增加key`run`，指向`__main__`模块
```python
sys.modules['run'] = sys.modules['__main__']
```

### 方法C（推荐）
启动文件单独使用一个文件，里面不包含其他代码。
这时`__main__`模块变成了bar, 这时run模块的名称就不会改变了，import行为也就正常了

bar.py
```python
from run import start

start()
```

### 输出结果
上面三种方法，殊途同归，结果都是一样的。

```
[2020-06-20 11:43:31,508 run.<module>   ] begin load
[2020-06-20 11:43:31,508 run.<module>   ] end load
[2020-06-20 11:43:31,509 foo.<module>   ] begin load
[2020-06-20 11:43:31,509 foo.<module>   ] end load
[2020-06-20 11:43:31,509 run.start      ] call
[2020-06-20 11:43:31,509 run.start      ] <run.Server object at 0x10f542fa0>
[2020-06-20 11:43:31,509 run.start      ] <class 'run.Server'>  140660950954304
[2020-06-20 11:43:31,509 foo.do_someting] begin call
[2020-06-20 11:43:31,509 foo.do_someting] <run.Server object at 0x10f542fa0>
[2020-06-20 11:43:31,509 foo.do_someting] <class 'run.Server'>  140660950954304
[2020-06-20 11:43:31,509 foo.do_someting] found attr name
[2020-06-20 11:43:31,509 foo.do_someting] end call
```

## 总结
因为C是编译型语言，可以理解为模块的导入在编译期就完成了，也就不会出现模块的循环依赖，而且全局对象的内存位置也在编译期就固定了。

而Python作为解释型语言，模块的导入加载和执行是混在一起的，所有对象都是可以更改的，也就容易出现这种问题。

切记：

**复杂Python程序的入口文件最好保持单一的文件，不要混入其他对象定义，谨慎使用`if __name__ == '__main__'`写法。**

## 参考
1. https://docs.python.org/zh-cn/3/reference/import.html
2. https://docs.python.org/zh-cn/3/library/sys.html?#sys.modules