---
title: 使用gdb调试Python程序
date: 2020-12-29 09:48:00
updated: 2020-12-30 21:18:00
categories: 编程
tags: [Python] 

---
由于Python解释器是由C语言编写，我们可以使用GDB来调试Python进程，对于程序卡死等异常情况调试比较有帮助。

<!--more-->

用gdb调试Python程序，主要有两个部分
1. 原生的gdb命令，调试的的Python解释器的C代码
2. `py-bt`等以py-为前缀的Python扩展命令，可以调试Python程序

我们需要通过原生gdb命令，如`n`(next)，`b`(break)等，使Python程序运行到我们需要调试的位置。
然后，通过`py-print`等命令输出我们想要的变量信息

## 环境配置
不同的Python环境，配置方法不太一样，这里推荐ubuntu 20.04以上版本

### ubuntu 20.04
```
sudo apt install gdb python3 python3-dbg
```

## gdb命令速查
### gdb原生命令
run or r –> executes the program from start to end.
break or b –> sets breakpoint on a particular line.
disable -> disable a breakpoint.
enable –> enable a disabled breakpoint.
next or n -> executes next line of code, but don’t dive into functions.
step –> go to next instruction, diving into the function.
list or l –> displays the code.
print or p –> used to display the stored value.
quit or q –> exits out of gdb.
clear –> to clear all breakpoints.
continue –> continue normal execution.

### gdb python命令
py-bt: 输出Python调用栈
py-bt-full: 输出Python调用栈
py-down: 在调用栈向下一级
py-list: 显示代码
py-locals: 输出locals变量
py-print: 输出
py-up: 在调用栈向上一级

## 使用示例
### 测试代码
一个斐波那契数列函数`fib.py`
```python
import time
def fib(n):
    time.sleep(0.01)
    if n == 1 or n == 0:
        return 1
    for i in range(n):
        return fib(n-1) + fib(n-2)

fib(100)
```

### 启动程序
1. `python3 fib.py &`
2. `gdb python3 148`, 148为Python的进程id

gdb输出，注意所需要的symbols是否都加载了
```
GNU gdb (Ubuntu 9.2-0ubuntu1~20.04) 9.2
Copyright (C) 2020 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from python3...
Reading symbols from /usr/lib/debug/.build-id/02/526282ea6c4d6eec743ad74a1eeefd035346a3.debug...
Attaching to program: /usr/bin/python3, process 148
Reading symbols from /lib/x86_64-linux-gnu/libc.so.6...
Reading symbols from /usr/lib/debug//lib/x86_64-linux-gnu/libc-2.31.so...
Reading symbols from /lib/x86_64-linux-gnu/libpthread.so.0...
Reading symbols from /usr/lib/debug/.build-id/4f/c5fc33f4429136a494c640b113d76f610e4abc.debug...
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Reading symbols from /lib/x86_64-linux-gnu/libdl.so.2...
Reading symbols from /usr/lib/debug//lib/x86_64-linux-gnu/libdl-2.31.so...
Reading symbols from /lib/x86_64-linux-gnu/libutil.so.1...
Reading symbols from /usr/lib/debug//lib/x86_64-linux-gnu/libutil-2.31.so...
Reading symbols from /lib/x86_64-linux-gnu/libm.so.6...
Reading symbols from /usr/lib/debug//lib/x86_64-linux-gnu/libm-2.31.so...
Reading symbols from /lib/x86_64-linux-gnu/libexpat.so.1...
(No debugging symbols found in /lib/x86_64-linux-gnu/libexpat.so.1)
Reading symbols from /lib/x86_64-linux-gnu/libz.so.1...
(No debugging symbols found in /lib/x86_64-linux-gnu/libz.so.1)
Reading symbols from /lib64/ld-linux-x86-64.so.2...
(No debugging symbols found in /lib64/ld-linux-x86-64.so.2)
0x00007fec057c10da in __GI___select (nfds=nfds@entry=0, readfds=readfds@entry=0x0, writefds=writefds@entry=0x0, exceptfds=exceptfds@entry=0x0, timeout=timeout@entry=0x7fff99ce33a0) at ../sysdeps/unix/sysv/linux/select.c:41
41	../sysdeps/unix/sysv/linux/select.c: No such file or directory.
```

### 调试
gdb调试Python没有pdb那么方便，主要是没法直接给python代码打断点，断点都是打在解释器代码中的。
所以，定位到脚本对应位置比较麻烦，需要一点耐心。

```
(gdb) py-list
   1    import time
   2    def fib(n):
  >3        time.sleep(0.01)
   4        if n == 1 or n == 0:
   5            return 1
   6        for i in range(n):
   7            return fib(n-1) + fib(n-2)
   8
(gdb) n
4970	in ../Python/ceval.c
(gdb) py-locals
n = 4
(gdb) b
Breakpoint 2 at 0x56acbe: file ../Include/object.h, line 459.
(gdb) c
Continuing.

Breakpoint 2, _PyEval_EvalFrameDefault (f=<optimized out>, throwflag=<optimized out>) at ../Include/object.h:459
459	in ../Include/object.h
... # 省略一些c命令
(gdb) py-locals
n = 3
(gdb) py-bt
Traceback (most recent call first):
  File "fib.py", line 4, in fib
    if n == 1 or n == 0:
  File "fib.py", line 7, in fib
    return fib(n-1) + fib(n-2)
   ... 省略一些输出
(gdb)
(gdb) py-up
#6 Frame 0x7fec0531a580, for file fib.py, line 7, in fib (n=4, i=0)
    return fib(n-1) + fib(n-2)
(gdb) py-locals
n = 4
i = 0
(gdb) py-up
#18 Frame 0x7fec0531c040, for file fib.py, line 7, in fib (n=7, i=0)
    return fib(n-1) + fib(n-2)
(gdb) py-print i
local 'i' = 0
(gdb) py-print n
local 'n' = 7
(gdb) py-down
#12 Frame 0x7fec0531a900, for file fib.py, line 7, in fib (n=6, i=0)
    return fib(n-1) + fib(n-2)
(gdb) py-print n
local 'n' = 6
```

## 参考
1. https://wiki.python.org/moin/DebuggingWithGdb
2. https://www.geeksforgeeks.org/gdb-step-by-step-introduction/

