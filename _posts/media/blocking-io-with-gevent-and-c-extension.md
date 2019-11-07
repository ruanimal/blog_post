title: C扩展与gevent共存时的问题
date: 2019-11-07 9:48 AM
categories: 编程
tags: [gevent, Python] 

----
 
gevent是一个使用完全同步编程模型的可扩展的异步I/O框架。

通用monkey.patch_all() 所有io操作函数, gevent可以以同步的方式编写异步代码. 在不更改代码的同时就可以使系统并发性能得到指数级提升。

这里有一个局限, c扩展中的io操作无法被patch, 会导致整个server阻塞

<!--more-->

## 一、一个简单的web server
这里使用flask写了web server 用于测试
```python
# filename: flask_app.py
import time 
from flask import Flask, request

app = Flask(__name__)

@app.route('/test', methods=['GET', 'POST'])
def test():
    time.sleep(0.2)
    return 'hello'
    
if __name__ == "__main__":
    app.run()
```

### 1.1 不使用gevent
安装依赖：`pip install flask gunicorn gevent`

启动服务器：`gunicorn -w 1 --bind 127.0.0.1:5000 flask_app:app`

测试性能：`siege -c 20 -r 1 'http://127.0.0.1:5000/test'` 

![](http://image.runjf.com/mweb/2019-11-07-15731309158635.jpg)

由于只有一个worker进程，可以看到只有5qps，每个请求sleep 0.2秒，是符合预期的。

### 1.2 使用gevent
启动服务器：`gunicorn -w 1 -k gevent --bind 127.0.0.1:5000 flask_app:app`

测试性能：`siege -c 20 -r 1 'http://127.0.0.1:5000/test'` 

![-w348](http://image.runjf.com/mweb/2019-11-07-15731311981620.jpg)

可以看到，性能有接近20倍的提升

## 二、C扩展阻塞io与gevent协作的问题
### 2.1 加入阻塞io的C扩展
这个程序通过sleep 2s 来模拟阻塞的io操作，所以每次调用会阻塞2s

```c
#include <unistd.h>

// sleep.c 

int main(){
  sleep(2);
  return 0;
}
```

然后，自然是把这个C文件编成动态链接库：

Linux下的编译：

```shell
gcc -c -fPIC sleep.c
gcc -shared sleep.o -o sleep.so
```

然后在我们的web server 中调用这个动态库，使用ctypes调用

```python
def socket_block():
    from ctypes import cdll
    lib = cdll.LoadLibrary('./sleep.so')
    lib.main()
    return 0
    
@app.route('/test', methods=['GET', 'POST'])
def test():
    socket_block()
    return 'hello'
```

测试后发现，gevent失效了，整个服务基本是串行阻塞状态
![-w454](http://image.runjf.com/mweb/2019-11-07-15731339898524.jpg)


### 2.2 解决方案
#### 2.2.1 尝试thread
使用线程, 基本没啥用, 不能解决问题

```python
@app.route('/test', methods=['GET', 'POST'])
def test():
    t = threading.Thread(target=socket_block, args=())
    t.setDaemon(1)
    t.start()
    return 'hello'
```

使用 siege 进行测试, 看请求耗时, 所有请求基本是串行的, gevent没有效果
```
➜  ~/projects siege -c 10 -r 1 'http://127.0.0.1:5000/test'  -v
** SIEGE 4.0.4
** Preparing 10 concurrent users for battle.
The server is now under siege...
HTTP/1.1 200    16.02 secs:       9 bytes ==> GET  /test
HTTP/1.1 200    16.02 secs:       9 bytes ==> GET  /test
HTTP/1.1 200    16.02 secs:       9 bytes ==> GET  /test
HTTP/1.1 200    16.02 secs:       9 bytes ==> GET  /test
HTTP/1.1 200    16.02 secs:       9 bytes ==> GET  /test
HTTP/1.1 200    16.03 secs:       9 bytes ==> GET  /test
HTTP/1.1 200    16.02 secs:       9 bytes ==> GET  /test
HTTP/1.1 200    16.02 secs:       9 bytes ==> GET  /test
HTTP/1.1 200    20.03 secs:       9 bytes ==> GET  /test
HTTP/1.1 200    20.04 secs:       9 bytes ==> GET  /test
```

#### 2.2.2 尝试multiprocess
问题解决

```python
@app.route('/test', methods=['GET', 'POST'])
def test():
    p = multiprocessing.Process(target=socket_block, args=())
    p.start()
    return 'hello'
```

使用 siege 进行测试, 请求没有被阻塞

```    
➜  ~/projects siege -c 5 -r 1 'http://127.0.0.1:5000/test'  -v
** SIEGE 4.0.4
** Preparing 5 concurrent users for battle.
The server is now under siege...
HTTP/1.1 200     0.01 secs:       5 bytes ==> GET  /test
HTTP/1.1 200     0.02 secs:       5 bytes ==> GET  /test
HTTP/1.1 200     0.03 secs:       5 bytes ==> GET  /test
HTTP/1.1 200     0.03 secs:       5 bytes ==> GET  /test
HTTP/1.1 200     0.04 secs:       5 bytes ==> GET  /test
```

### 2.3 总结
webserver主体进程使用gevent, 将阻塞的c扩展网络io操作放到另一个进程中执行, 可以改造成一个服务

具体可以用这下面两种实现
- celery
- multiprocess

还有一种对动态库进行patch的方案（[greenify](https://github.com/douban/greenify)），只在linux下有效，就没怎么研究了