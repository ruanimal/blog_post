---
title: Python装饰器详解
date: 2019-09-23 09:48:00
updated: 2020-05-05 10:54:46
categories: 编程
tags: [装饰器, Python] 

---
装饰器应该是Python最富有表现力的语法结构之一了，基于装饰器很多功能可以实现得比较优雅。
Python中的装饰器，来源于设计模式中的装饰器模式。顾名思义，所谓装饰器就是对原有的对象做一些装饰，也就是给已有的对象添加一些功能。

## 简易装饰器
装饰器本质上是函数替换. 装饰器被调用会返回一个函数, 被装饰函数会被返回的这个函数替换. 
要使用装饰器，先得定义一个装饰器函数，然后在需要装饰的函数的前一行使用`@`符号加上装饰器名称。
下面是一个简单是例子, `hello`函数被`running`装饰器装饰, `running`返回了`fuck`函数, 此时调用`hello`就变成了调用`fuck`, 实现了函数功能的改变.

<!--more-->

```Python
def fuck(who='nobody'):
    return "fuck, %s!" % who

def running(function):
    print('replace %r to %r' % (function, fuck))
    return fuck

@running
def hello(who='nobody'):
    return "hello, %s!" % who

print('--- before call hello ---')
print(hello())
print(hello('foo'))
```

output

```
replace <function hello at 0x1052e98c8> to <function fuck at 0x104d15f28>
--- before call hello ---
fuck, nobody!
fuck, foo!
```

装饰器在这里的效果等效于函数嵌套，不过看起来有点别扭。

```Python
def fuck(who='nobody'):
    return "fuck, %s!" % who

def running(function):
    print('replace %r to %r' % (function, fuck))
    return fuck

def hello(who='nobody'):
    return "hello, %s!" % who


hello = running(hello)
print(hello())
print(hello('foo'))
```

**注意：一旦通过`@running`装饰了函数，不管被装饰函数是否运行，python解释器都会执行一遍running函数。**

## 普通装饰器
前面这个装饰器将hello函数替换成fuck函数之外就没有别的功能了, 只是为了演示装饰器的原理, 并没有什么实际用处

现在我们写一个计时器装饰器. 
还是将hello函数替换成fuck, 这里我们将fuck函数的定义移动到runing内部, fuck函数在调用hello的同时, 实现计时功能. 
这样有一个好处, 这个fuck函数就不是全局可见的, 不会污染全局环境, 还可以用到闭包的一些特性.

```Python
import time

def running(func):
    def fuck(*args, **kwargs):
        start = time.time()
        print('`%s` is running...' % func.__name__)
        _result = func(*args, **kwargs)
        print('run `%s` takes %s seconds' % (func.__name__, time.time()-start))
        return _result
    return fuck

@running
def hello(who='nobody'):
    return "hello, %s!" % who


print(hello('foo'))
print(hello('bar'))
print(hello.__name__)
```

输出

```
`hello` is running...
run `hello` takes 3.981590270996094e-05 seconds
hello, foo!
`hello` is running...
run `hello` takes 3.814697265625e-06 seconds
hello, bar!
fuck

```

## 消除装饰器的副作用
上一个装饰器也有一个问题，因为装饰器本质上是函数替换. 就是经过装饰的函数一些属性变了, 比如`hello.__name__`变成了`fuck`。

所以我们要将这些属性复制到新函数上, 同时由于fuck函数已经没有fuck功能了, 我们将它重命名为wrapper

```Python
import time

def running(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        print('`%s` is running...' % func.__name__)
        _result = func(*args, **kwargs)
        print('run `%s` takes %s seconds' % (func.__name__, time.time()-start))
        return _result

    wrapper.__name__ = func.__name__
    return wrapper

@running
def hello(who='nobody'):
    return "hello, %s!" % who

print(hello.__name__)
```

output

```
hello
```

这个问题也可以通过python内置的`functools.wraps`装饰器解决，这个装饰器对原函数的一些属性进行了复制。

```Python
import time
import functools

def running(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        print('`%s` is running...' % func.__name__)
        _result = func(*args, **kwargs)
        print('run `%s` takes %s seconds' % (func.__name__, time.time()-start))
        return _result
    return wrapper
```

## 带参数的装饰器
上一个装饰器还有一个缺点是, 装饰器不能接受参数, 现在我们来实现带参数的装饰器

带参数的装饰器其实就是多嵌套一层函数

```Python
import time
import functools

def running(system):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            print('`%s` is running at %s' % (func.__name__, system))
            _result = func(*args, **kwargs)
            print('run `%s` takes %s seconds' % (func.__name__, time.time()-start))
            return _result
        return wrapper
    return decorator

@running('mac')
def hello(who='nobody'):
    return "hello, %s!" % who

print(hello('foo'))
```

output

```
`hello` is running at mac
run `hello` takes 3.910064697265625e-05 seconds
hello, foo!
```

## 可选带参数的装饰器
有时我们希望装饰器更为通用, 适用于带参数和不带参数的场景

```Python
import time
import functools

def running(*running_args, system='mac', **running_kwargs):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            print('`%s` is running at %s' % (func.__name__, system))
            _result = func(*args, **kwargs)
            print('run `%s` takes %s seconds' % (func.__name__, time.time()-start))
            return _result
        return wrapper

    if len(running_args) == 1 and callable(running_args[0]):
        return decorator(running_args[0])
    else:
        return decorator

@running(system='linux')
def hello(who='nobody'):
    return "hello, %s!" % who

@running
def hello2(who='nobody'):
    return "hello, %s!" % who

print(hello('foo'))
print(hello2('bar'))
```

output

```
`hello` is running at linux
run `hello` takes 2.5033950805664062e-05 seconds
hello, foo!
`hello2` is running at mac
run `hello2` takes 3.814697265625e-06 seconds
hello, bar!
```


