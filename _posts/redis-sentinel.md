title: Redis Sentinel 高可用
date: 2021-08-04 10:48 PM
categories: 编程
tags: [Redis,]

----

## sentinel 状态储存
## sentinel 连接 Redis 服务器
## sentinel 互相连接

## 下线检测与选举
### 主观下线
### 客观下线
### sentinel 选举
## 故障转移
## 相关问题
### 脑裂
所谓脑裂问题（类似于精神分裂），就是同一个集群中的不同节点，对于集群的状态有了不一样的理解。

由于网络原因或者一些特殊原因，哨兵失去了对master节点器的感知，将会通过选举进行故障转移，将slave节点提升为master节点，这就导致了当前集群中有2个master，也就是集群产生两个网络分区。
不同的 client 链接到不同的 redis 进行读写，那么在两台机器上的 redis 数据，就出现了不一致的现象了。
当哨兵恢复对老master节点的感知后，会将其降级为slave节点，然后从新master同步数据，导致脑裂期间老master写入的数据丢失。

![](media/16283286405956.jpg)

**解决方案**
所以关键是，两个分区状态不能分叉（其中一个的状态可以落后），也就是同时只能有一个master可写。可以要求连到master上的slaves数量和状态必须达到某个标准，master才可写。

redis的配置文件中，存在两个参数
```
min-slaves-to-write 3  # 连接到master的最少slave数量
min-slaves-max-lag 10  # slave连接到master的最大延迟时间
```

按照上面的配置，要求至少3个slave节点，且数据复制和同步的延迟不能超过10秒，否则的话master就会拒绝写请求，就可以减少数据同步之后的数据丢失。

## 参考
- redis 3.0 源码
- redis 设计与实现