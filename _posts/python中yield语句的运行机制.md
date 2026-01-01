---
title: Python中yield语句的运行机制
date: 2016-04-16 20:17:00
updated: 2020-04-30 22:39:01
categories: 编程
tags: [Python, ]

---
## 概述
如果一个在函数中存在yield关键字，那么这个函数就构成了生成器。生成器是一个函数，它生成一个序列，以便在迭代中使用。
调用这个函数，并不会马上开始执行函数体中的代码，而是返回一个生成器对象，通过调用生成器对象的`next()`方法（python3中是`__netx__()`）执行函数。

那么，具体的函数中语句的执行顺序是怎么样的呢？

## 代码

```python
def func(x=10):
    print 'the beginning of function'
    if x <= 0 or not isinstance(x, int):
        return
    for i in range(x):
        print 'before yield', i
        yield i
        print 'after yield', i

gen = func(2)
print '*'*20
print '-> yielding: %s' % gen.next()
print '*'*20
print '-> yielding: %s' % gen.next()
print '*'*20
print '-> yielding: %s' % gen.next()
```

输出
```
********************
the beginning of function
before yield 0
-> yielding: 0
********************
after yield 0
before yield 1
-> yielding: 1
********************
after yield 1
Traceback (most recent call last):
  File "D:\Projects\test.py", line 28, in <module>
    print '-> yielding: %s' % gen.next()
StopIteration
```

## 分析
1. 首先运行`func(2)`，这时函数的所有语句都没有执行，返回一个生成器赋值给`gen`。
2. 第一次执行`gen.next()`，函数从头开始执行，运行完yield语句暂停住了。
3. 再次运行`gen.next()`，从停下的地方继续，直到遇到遇到下一个yield，运行完yield语句又暂停住了。
4. 第三次尝试运行`gen.next()`，运行完`print 'after yield', i`，由于循环次数已满，找不到下一个yield，就出现`StopIteration`错误

