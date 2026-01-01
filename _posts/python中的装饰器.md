title: Python中的装饰器（decorator）
date: April 27, 2016 8:37 PM
categories: 编程
tags:  [Python, ]

----

## 概述
顾名思义，所谓装饰器就是对原有的对象做一些装饰，也就是给已有的对象添加一些功能。

假如我现在想在函数运行时输出一些信息

## 小学水平
```python
def running(func):
    print '`%s` is running...' % func.__name__
    return func
    
@running
def my_sum():
    return "I cat't sum right now!"
    
print my_sum()
```
输出
```
`my_sum` is running...
I cat't sum right now!
```
要使用装饰器，先得定义一个装饰器函数，然后在需要装饰的函数的前一行使用`@`符号加上`装饰器名称`。  
在这里的效果等效于running(my_sum)()，不过看起来有点别扭。
**注意：一旦通过`@running`装饰了函数，不管被装饰函数是否运行，python解释器都会执行一遍`running`函数。**

## 中学水平
上一个装饰器用起来还行，但是有一个致命的问题，它不能装饰带参数的函数。所以我们在装饰器内部定义`_wrapper`函数，并返回它。这个函数接收所有位置参数`*args`，和关键字参数`*kwargs`，在`_wrapper`内部执行`func(*args, **kwargs)`。

<!--more-->
```python
def running(func):
    def _wrapper(*args, **kwargs):
        print '`%s` is running...' % func.__name__
        return func(*args, **kwargs)
    return _wrapper
    
@running
def my_sum(a, b=2):
    return a + b

print my_sum(1,2)
print my_sum.__name__
```

输出
```
`my_sum` is running...
3
_wrapper
```

这也是python中最普通的装饰器，假如需要在`my_sum`运行之后添加一些功能，则可以改成这样。
```python
import time

def running(func):
    def _wrapper(*args, **kwargs):
        start = time.time()
        print '`%s` is running...' % func.__name__
        _result = func(*args, **kwargs)
        print 'run `%s` takes %s seconds' % (func.__name__, time.time()-start)
        return _result
    return _wrapper
```

## 大学水平
上一个装饰器也有一个问题，就是经过装饰的`my_sum.__name__`变成了`_wrapper`。
这个问题可以通过python内置的`functools.wraps`解决，这个装饰器对原函数的一些属性进行了复制。

```python
import time
import functools

def running(func):
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        start = time.time()
        print '`%s` is running...' % func.__name__
        _result = func(*args, **kwargs)
        print 'run `%s` takes %s seconds' % (func.__name__, time.time()-start)
        return _result
    return _wrapper

@running
def my_sum(a=1, b=2):
    time.sleep(1)
    return a + b

print my_sum(1,2)
print my_sum.__name__
```

输出
```
`my_sum` is running...
run `my_sum` takes 1.0 seconds
3
my_sum
```




