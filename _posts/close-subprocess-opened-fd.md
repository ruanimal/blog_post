title: 关闭子进程打开的文件描述符
date: 2022-08-30 10:48 PM
categories: 编程
tags: [Python,]

----

我们在测试代码时，由于需要经常重启服务，经常会发现服务端口被占用。
一般kill掉后台进程就ok了，但是如果服务有启动一些常驻的后台程序，可能也会导致端口不能释放。

在类UNIX系统中，一切被打开的文件、端口被抽象为文件描述符（file descriptor）
从python3.4开始，文件描述符默认是non-inheritable，也就是子进程不会共享文件描述符。
<!--more-->

## 问题
一般为了实现多进程、多线程的webserver，服务端口fd必须设置为继承（set_inheritable），这样才能多进程监听一个端口（配合SO_REUSEPORT）
典型的是使用flask的测试服务器的场景，这里我们写一段代码模拟。

```python
import socket, os
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 22222))
server.set_inheritable(True)

os.system("python -c 'import time;time.sleep(1000)' ")
```

我们通过`lsof -p {pid}`可以看到这两个进程的所有文件描述符
server进程, 可以看到服务端口的fd是4
```
COMMAND   PID  FD      TYPE             DEVICE  SIZE/OFF       NODE NAME
ptpython 6214 cwd       DIR              253,0      4096  872946898 /
...
ptpython 6214   0u      CHR             136,13       0t0         16 /dev/pts/13
ptpython 6214   1u      CHR             136,13       0t0         16 /dev/pts/13
ptpython 6214   2u      CHR             136,13       0t0         16 /dev/pts/13
ptpython 6214   3r      CHR                1,9       0t0       2057 /dev/urandom
ptpython 6214   4u     sock                0,7       0t0   58345077 protocol: TCP
ptpython 6214   5u  a_inode               0,10         0       8627 [eventpoll]
ptpython 6214   6u     unix 0x0000000000000000       0t0   58368029 socket
ptpython 6214   7u     unix 0x0000000000000000       0t0   58368030 socket
```

sleep子进程，也拥有fd=4的文件描述符
```
COMMAND   PID  FD   TYPE DEVICE  SIZE/OFF       NODE NAME
python  18022 cwd    DIR  253,0      4096  872946898 /
...
python  18022   0u   CHR 136,13       0t0         16 /dev/pts/13
python  18022   1u   CHR 136,13       0t0         16 /dev/pts/13
python  18022   2u   CHR 136,13       0t0         16 /dev/pts/13
python  18022   4u  sock    0,7       0t0   58345077 protocol: TCP
```

如果server进程退出时，sleep进程没有退出fd=4对应的端口就被占用了，服务也就不能正常启动了。


## 解决方法
### 手动清理
```Python
import os
import time

os.system(f'lsof -p {os.getpid()}')
os.closerange(3, 100)  # 这里假定打开文件描述符不会超过100
time.sleep(5)
os.system(f'lsof -p {os.getpid()}')
# 后面执行需要的业务代码
```

### 使用close_fds
使用subprocess库而不是os来启动子程序， 通过close_fds参数关闭多余的文件描述符
```python
import subprocess
subprocess.call("python -c 'import time;time.sleep(1000)'", shell=True, close_fds=True)
```

## 参考
- https://docs.python.org/3/library/os.html#inheritance-of-file-descriptors
- https://docs.python.org/3/library/subprocess.html#subprocess.Popen
- https://stackoverflow.com/questions/2023608/check-what-files-are-open-in-python#answer-25069136