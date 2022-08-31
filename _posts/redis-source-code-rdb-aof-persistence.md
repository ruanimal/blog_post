title: Redis持久化：RDB与AOF
date: 2021-07-20 10:48 PM
categories: 编程
tags: [Redis,]

----

Redis是内存型数据库，所有数据都存储在内存中。而内存是易失型存储，一旦进程退出所有数据都会丢失。

所谓持久化，就是将Redis在内存中的数据库状态以某次格式保存到磁盘里面，避免数据意外丢失。

Redis有两种持久化方式：RDB (Redis Database)、AOF (Append Only File)
<!--more-->
## RDB持久化
RDB持久化功能所生成的RDB文件是一个经过压缩的二进制文件，包含了Redis数据库的所有数据。

RDB是将redis中所有db中的所有键值对以如下格式进行储存

![](http://image.runjf.com/mweb/2021-07-21-16268563558568.jpg)

### RDB文件创建
有两个命令可以生成RDB文件，`SAVE` 和 `BGSAVE`。生成RDB文件时，redis会遍历所有非空db的所有键值对按一定格式存储到RDB文件中。

`SAVE` 命令会在当前进程进行，期间服务器会阻塞，不能处理任何请求。
`BGSAVE` 命令会fork一个子进程来创建RDB（利用Copy-on-write），服务继续处理命令请求。

为了避免竞争条件和性能问题，`SAVE` 和 `BGSAVE`任意时刻只能有一个在执行。

用户可以通过save选项设置多个保存条件,但只要其中任意一个条件被满足，就会触发RDB保存.
save选项的格式是 `save seconds option_times`。例如`save 900 1`，若服务器在900秒之内, 对数据库进行了至少1次修改，则执行BGSAVE。

BGSAVE也已可能会阻塞请求，因为磁盘io满了，这时如果有fsync操作，服务也会阻塞。
可以设置 `no-appendfsync-on-rewrite yes`, 在子进程处理和写硬盘时, 主进程不调用 fsync() 操作。

### RDB文件读取
服务器启动时会自动载入RDB文件，Redis并没有专门用于载人RDB文件的命令。

如果服务器开启了AOF持久化功能，那么服务器会优先使用AOF文件来还原数据库状态。

## AOF持久化
由于RDB生成的机制决定了，RDB文件总是会和redis内存有部分不一致，**RDB文件会缺少从上次BGSAVE开始到当前时刻的所有改动**。AOF持久化的存在就是为了解决该问题。

AOF持久化是通过保存执行的写命令来记录数据库状态。
因为Redis的命令请求协议是纯文本格式，所以AOF文件类似如下。
```
*2\r\n$6\r\nSELECT\r\n$l\r\nO\r\n 
*3\r\n$3\r\nSET\r\n$3\r\nmsg\r\n$5\r\nhello\r\n 
```

### AOF持久化实现
1. 命令追加：执行完命令，将所有**写命令**追加到aof_buf缓冲区末尾
2. 文件写入：将aof_buf的内容写入文件，并清空aof_buf
3. 文件同步：清空完aof_buf之后，根据appendfsync配置的策略，决定如何刷新文件缓存到硬盘。

appendfsync决定如何刷新文件缓存到硬盘，该选项的值直接影响的效率和安全性。
当故障停机时，文件缓冲区内的数据会丢失。
appendfsync有以下选项
- always: 每次都会进行文件缓冲区刷新，最安全，效率也最低。
- no: 不主动刷新文件缓冲区，由系统决定刷新时机，安全性最低，效率最高
- everysec: 每秒刷新一次文件缓冲区，安全性和效率的折中方案。

### AOF文件还原
AOF的还原就是模仿客户端逐条执行文件里的命令。

AOF的还原时机也是服务启动时，并且在还原过程中能正常执行的只有 PUBSUB 等模块。

步骤如下：
1. 创建不带网络连接的伪客户端(fake client)
2. 从AOF文件中分析和读取一条命令
3. 使用伪客户端执行该命令
4. 重复步骤2、3，直到处理完所有命令

### AOF重写
由于AOF是直接记录的写命令而不是数据库状态，所以文件中包含很多冗余语句，导致文件膨胀。

比如下面的这些命令，其实最终数据库状态等价于`lpush numbers 333`, 前4条语句都是冗余的。
```
127.0.0.1:6379> lpush numbers 111
(integer) 1
127.0.0.1:6379> lpush numbers 222
(integer) 2
127.0.0.1:6379> lpop numbers
"222"
127.0.0.1:6379> lpop numbers
"111"
127.0.0.1:6379> lpush numbers 333
(integer) 1
127.0.0.1:6379> lrange numbers 0 -1
1) "333"
```

为了解决AOF文件体积膨胀的问题，Redis提供了AOF文件重写(rewrite) 功能。

AOF文件重写是遍历redis的所有键值对，生成对应的redis命令，写入到一个新的文件中，并替换旧AOF文件。
所以AOF文件重写和旧AOF文件并没有关系，更应该称之为**AOF重生成**。

AOF重写程序在子进程里执行, 这样做可以同时达到两个目的: 
- 子进程进行AOF重写期间, 服务器进程可以继续处理命令请求。
- 子进程带有服务器进程的数据副本，可以在避免使用锁的情况下，保证数据的安全性（Copy-on-write）。

在AOF重新过程中，所有命令会额外会写一份到**AOF重写缓冲区**中，当新AOF文件生成时，父进程会将AOF重写缓冲区的内容追加到新AOF文件中，并替换旧AOF文件。

![](http://image.runjf.com/mweb/2021-07-21-16268637141893.jpg)

为防止AOF重写失败，AOF缓冲区在重写过程中依然正常工作。

![](http://image.runjf.com/mweb/2021-07-21-16268635658876.jpg)

**注意**：redis主从是基于`RDB + 命令传播`，并没有利用AOF文件，与MySQL的binlog不同。

## 参考
- redis 3.0 源码
- redis 设计与实现