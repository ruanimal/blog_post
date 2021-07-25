title: Redis主从复制机制
date: 2021-07-21 10:48 PM
categories: 编程
tags: [Redis,]

----

Redis作为内存型数据，为了高可用，必须有数据备份，这里采取主从的模式。
用户可以通过执行 SLAVEOF 命令或者设置 slaveof 选项，让一个服务器去复制 （replicate) 另一个服务器。
<!--more-->
如果服务器 `127.0.0.1:12345` 向 `127.0.0.1:6379` 发送 `SLAVEOF 127.0.0.1 6379`, 则服务器（12345）将成为服务器（6379）的从服务器。

## 旧版复制功能（全量复制）
Redis的复制功能分为同步（RDB文件）和命令传播（同步写命令）两个阶段，具体步骤如下。
1. 从服务器发送`SYNC`
2. 主服务器接收`SYNC`后执行`BGSAVE`生成RDB文件，同时用缓冲区记录之后所有写命令。
3. 主服务器发送RDB到从服务器，从服务器加载RDB
4. 主服务器发送缓冲区内的写命令
5. 之后主服务器写命令都需要同时发一份给从服务器（命令传播）

![-w908](http://image.runjf.com/mweb/2021-07-25-16272051223635.jpg)

## 缺陷及解决方案
由于RDB的生成发送非常耗时，主从短暂断线的情况下，也需要重复生成，主从同步的效率就非常低了。

Redis从2.8版本开始, 使用`PSYNC`命令替换`SYNC`，增加了部分同步功能，对断线重连的情况进行了优化。

主从服务器都记录了**复制偏移量**，记录了主服务器发出的字节数和从服务器收到的字节数,并且主服务器使用一个**复制积压缓冲区**记录最近发出的数据（FIFO）。

同步时，从服务器会发送复制偏移量。
- 如果，主从偏移量相差的这部分数据在缓冲区中，则主服务器就发送这部分数据
- 否则，执行全量复制。

同时，主服务器每次启动时会生成**运行id**，防止主服务器重启后复制混乱。

![-w586](http://image.runjf.com/mweb/2021-07-25-16272066103593.jpg)
![-w552](http://image.runjf.com/mweb/2021-07-25-16272066397939.jpg)

## 参考
- redis 3.0 源码
- redis 设计与实现