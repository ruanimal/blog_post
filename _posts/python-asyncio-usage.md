title: Python asyncio 简易教程
date: 2020-05-24 9:48 AM
categories: 编程
tags: [Python, 异步]

--------

`asyncio`是Python 3.4版本引入的标准库，直接内置了对异步IO的支持。

`asyncio`的编程模型就是一个消息循环。我们从`asyncio`模块中直接获取一个`EventLoop`的引用，然后把需要执行的协程扔到`EventLoop`中执行，就实现了异步IO。

<!--more-->

## 例子
```python
import asyncio

async def hello_world():
    print('hello')
    await asyncio.sleep(1)
    print(' world')
    
loop = asyncio.get_event_loop()
loop.run_until_complete(hello_world())
loop.close()
```

## 执行逻辑
`async def` 定义的每一个函数, 本质上是一个协程.
当await调用一个函数时, 程序就切换到该函数中执行了, 当执行完成时, 程序又回到await调用处继续执行. 

当函数的调用链上碰到系统io相关函数时，程序执行的控制权就会回到eventloop主循环，eventloop就会调度执行别的函数，等到该函数的io就绪时，再从该函数暂停的地方继续执行。

再搭配上支持非阻塞io的异步库, 这样就实现了高效的异步编程.

所有异步函数是在同一个线程中执行的, 在该进程内我们还可启用其他线程, 执行其他同步代码. 下图展示了Python中协程、线程、进程的逻辑关系。

![](http://image.runjf.com/mweb/2020-05-24-15903277834535.jpg)

 
## 如何在event loop内调用同步代码

一旦使用async, 整个线程内都必须使用异步, 否则整个线程都会阻塞。
所以，必须另起线程, 将同步操作放在线程中执行。

```python
import asyncio
import time
import concurrent.futures

executor = concurrent.futures.ThreadPoolExecutor(
    max_workers=2,  # 线程池大小
)

def some_block_things(x):
    time.sleep(1)
    return x

async def hello_world(x):
    print('hello world', time.time())
    loop = asyncio.get_event_loop()
    fut = loop.run_in_executor(executor, some_block_things, x)
    num =  await asyncio.wait_for(fut, timeout=10)
    print('num %s' % num)

async def main():
    start = time.time()
    await asyncio.wait([hello_world(i) for i in range(8)])
    end = time.time()
    print("Complete in {} seconds".format(end - start))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```

输出 
```
hello world 1533904346.37133
hello world 1533904346.371683
hello world 1533904346.37199
hello world 1533904346.372059
hello world 1533904346.372122
hello world 1533904346.372176
hello world 1533904346.372245
hello world 1533904346.372295
num 0
num 3
num 4
num 1
num 5
num 6
num 7
num 2
Complete in 4.015289068222046 seconds
[Finished in 4.2s]
```

因为这里我的线程池大小为2, 所以8个sleep整体耗时4s, 但是'hello world' 几乎是同一时刻输出的, 这就是asyncio的魅力所在.

## 总结
asyncio使用`async`和`await`的语法，使得原来回调函数形式的异步代码变为同步代码，更易于理解。
使用asyncio可以方便地构建高性能的网络服务, 单进程qps可以轻松地达到2000以上。
基于asyncio也出现了一些异步web框架，比如sanic，相比传统框架性能提升较大。
