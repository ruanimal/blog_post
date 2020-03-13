title: OpenBLAS blas_thread_init pthread_creat Resource temporarily unavailable 问题分析与解决
date: 2020-02-28 9:48 AM
categories: 编程
tags: [Python, 机器学习] 

----

## 症状
最近在在一台服务器上发现, 一个服务的工作进程会异常退出, 但部署有相同代码的其他服务却没有类似的情况.

查看日志发现以下错误

```
Traceback (most recent call last):
	...
  File "/home/q/hawkeye_mid_dev/src/model/b_card_model.py", line 5, in <module>
    import numpy as np
  File "/home/sync360/miniconda3/envs/xd_mid/lib/python2.7/site-packages/numpy/__init__.py", line 142, in <module>
    from . import add_newdocs
  File "/home/sync360/miniconda3/envs/xd_mid/lib/python2.7/site-packages/numpy/add_newdocs.py", line 13, in <module>
    from numpy.lib import add_newdoc
  File "/home/sync360/miniconda3/envs/xd_mid/lib/python2.7/site-packages/numpy/lib/__init__.py", line 8, in <module>
    from .type_check import *
  File "/home/sync360/miniconda3/envs/xd_mid/lib/python2.7/site-packages/numpy/lib/type_check.py", line 11, in <module>
    import numpy.core.numeric as _nx
  File "/home/sync360/miniconda3/envs/xd_mid/lib/python2.7/site-packages/numpy/core/__init__.py", line 16, in <module>
    from . import multiarray
KeyboardInterrupt
OpenBLAS blas_thread_init: pthread_create: Resource temporarily unavailable
OpenBLAS blas_thread_init: RLIMIT_NPROC 1024 current, 516033 max
```

## 分析
### Resouce limit
在上面的错误输出里有一个关键词 `RLIMIT_NPROC`, 涉及到了linux的Resouce limit.

在Linux系统中，Resouce limit指在一个进程的执行过程中，它所能得到的资源的限制，比如进程的core file的最大值，虚拟内存的最大值等。

<!--more-->

Resouce limit的大小可以直接影响进程的执行状况。其有两个最重要的概念：soft limit 和 hard limit。

softlimit是指内核所能支持的资源上限, hard limit在资源中只是作为softlimit的上限。当你设置hard limit后，你以后设置的softlimit只能小于hard limit。

要说明的是，hardlimit只针对非特权进程，也就是进程的有效用户ID(effective user ID)不是0的进程。具有特权级别的进程(具有属性CAP_SYS_RESOURCE)，softlimit则只有内核上限。

> resource：可能的选择有
>
> RLIMIT_AS 	进程的最大虚内存空间，字节为单位。
> RLIMIT_CORE 	内核转存文件的最大长度。
> RLIMIT_CPU 	最大允许的CPU使用时间，秒为单位。当进程达到软限制，内核将给其发送SIGXCPU信号，这一信号的默认行为是终止进程的执行。然而，可以捕捉信号，处理句柄可将控制返回给主程序。如果进程继续耗费CPU时间，核心会以每秒一次的频率给其发送SIGXCPU信号，直到达到硬限制，那时将给进程发送 SIGKILL信号终止其执行。
> RLIMIT_DATA 	进程数据段的最大值。
> RLIMIT_FSIZE 	进程可建立的文件的最大长度。如果进程试图超出这一限制时，核心会给其发送SIGXFSZ信号，默认情况下将终止进程的执行。
> RLIMIT_LOCKS 	进程可建立的锁和租赁的最大值。
> RLIMIT_MEMLOCK 	进程可锁定在内存中的最大数据量，字节为单位。
> RLIMIT_MSGQUEUE 	进程可为POSIX消息队列分配的最大字节数。
> RLIMIT_NICE 	进程可通过setpriority() 或 nice()调用设置的最大完美值。
> RLIMIT_NOFILE 	指定比进程可打开的最大文件描述词大一的值，超出此值，将会产生EMFILE错误。
> **RLIMIT_NPROC 	用户可拥有的最大进程数。**
> RLIMIT_RTPRIO 	进程可通过sched_setscheduler 和 sched_setparam设置的最大实时优先级。
> RLIMIT_SIGPENDING 	用户可拥有的最大挂起信号数。
> RLIMIT_STACK 	最大的进程堆栈，以字节为单位。

### 用户可拥有的最大进程数
可以看到`RLIMIT_NPROC`是指的	是用户可拥有的最大进程数.

通过读取`/proc/${PID}/limits`文件, 可以得知对应进程的Resouce limit数值

```
$ sudo cat /proc/13839/limits 

Limit                     Soft Limit           Hard Limit           Units     
Max cpu time              unlimited            unlimited            seconds   
Max file size             unlimited            unlimited            bytes     
Max data size             unlimited            unlimited            bytes     
Max stack size            10485760             unlimited            bytes     
Max core file size        0                    unlimited            bytes     
Max resident set          unlimited            unlimited            bytes     
Max processes             1024                 516033               processes 
Max open files            32768                32768                files     
Max locked memory         65536                65536                bytes     
Max address space         unlimited            unlimited            bytes     
Max file locks            unlimited            unlimited            locks     
Max pending signals       516033               516033               signals   
Max msgqueue size         819200               819200               bytes     
Max nice priority         0                    0                    
Max realtime priority     0                    0                    
Max realtime timeout      unlimited            unlimited            us    
```

可以看到, `Max processes`一项的Soft Limit为1024, Hard Limit为516033, 与错误输出中的信息一致.

通过`ps -ef -T |grep $(whoami) | wc -l`可以查得当前用户的总进程(线程)数目, 结果是`1016`.

显然1016已结接近Soft Limit了, 当程序尝试启动更多进程时就回出错, 所以我们需要增大Soft Limit.

### 增大RLIMIT_NPROC数值

通过修改`/etc/security/limits.d/90-nproc.conf`配置文件

增加以下内容, 将RLIMIT_NPROC设置为10240
```
*    soft    nproc    10240

```

执行`ulimit -u`, 确认已经生效
```
$ ulimit -u
10240
```

### 重启进程问题依然存在
但是问题依然存在, 不能解决. 

再次查看进程的`RLIMIT_NPROC`, 发现并没有变化.
```
$ cat /proc/13839/limits   |grep 'Max processes'
Max processes             1024                 516033               processes
```

但是从终端启动新服务, 其`RLIMIT_NPROC`数值已经是10240了. 

由此初步判断, 应该是修改limits配置文件, 只对新启动的进程生效.

由于工作进程都是由supervisor托管的, 查看了supervisord进程的`RLIMIT_NPROC`, 发现也是1024.
由supervisord启动的所有进程的父进程都是supervisord进程, 都继承了它的`RLIMIT_NPROC`数值.

最终, 将supervisord进程重启, 问题得到解决.

## 为什么1024的进程数不够用呢?
这个服务是个多进程的tornado服务, 共10个工作进程. 但是最终用了241个进程/线程(Linux进程和线程某种意义上是等价的).

```
$ ps -ef -T |grep sync360  | grep mid  | wc -l   
241  
```

这台服务器上类似的服务又有三四个, 1024的量很快就用完了.

所以问题又回到了`OpenBLAS`身上

### OpenBLAS
OpenBLAS是高度优化的线性代数库, 很多机器学习的库都依赖了OpenBLAS.

OpenBLAS通过多线程的方式来加速计算, 所以241个进程很很好解释了.
由于我的服务器是24核心的, 一般多线程程序的默认线程数与cpu核心数一致.
所以: `241 = 10 * 24 + 1` 

### 减少使用的进程数
因为服务本身已经是多进程的, 再启用OpenBLAS的多线程, 加速的意义其实不大了.

*查阅资料后发现, 如果应用是多线程的，将会与多线程下的OpenBLAS发生冲突。因此OpenBLAS只能运行在单线程下。(未充分验证)*

可以通过设置环境变量`OPENBLAS_NUM_THREADS`, 调整OpenBLAS的线程数.

设置之后, 重启程序, 出现另一个类似的问题
```
libgomp: Thread creation failed: Resource temporarily unavailable
```

这里的libgomp是OpenMP的动态库, OpenMP会被用来优化编译OpenBLAS.
所以我们将环境变量`OMP_NUM_THREADS`也设置为1

在python启动文件前面加入以下语句
```
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1' 
os.environ['OMP_NUM_THREADS'] = '1'
```

重启程序, 发现只使用了11个进程, 与预期相符合, 问题解决.

## 总结
该问题的根本原因是最大进程数`RLIMIT_NPROC`不够用.

所以解决方法有两个

### 增大最大进程数
通过修改`/etc/security/limits.d/90-nproc.conf`配置文件, 增大最大进程数

同时注意, 修改最大进程数等limits配置文件, 只对新启动的进程生效. 需要将相关进程都重启

### 减小当前使用的进程
通过关闭多线程, 来减少占用的进程数.

设置环境变量`OPENBLAS_NUM_THREADS`和`OMP_NUM_THREADS`的值为1

## 参考
1. https://github.com/numpy/numpy/issues/14868#issuecomment-552561001
2. https://stackoverflow.com/questions/51256738/multiple-instances-of-python-running-simultaneously-limited-to-35#answer-51257384
3. https://stackoverflow.com/questions/52026652/openblas-blas-thread-init-pthread-create-resource-temporarily-unavailable#answer-57549064
4. https://www.tecmint.com/set-limits-on-user-processes-using-ulimit-in-linux/
5. https://blog.csdn.net/hellochenlu/article/details/51604007
6. https://blog.csdn.net/iteye_10725/article/details/82452978
7. https://blog.csdn.net/dingding_tao/article/details/81043304