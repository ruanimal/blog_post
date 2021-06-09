title: 雪花算法原理及实现
date: 2021-06-08 7:48 PM
categories: 编程
tags: [分布式, Python, 算法]

----

分布式系统中，全局唯一id的生成是个常见的问题。在互联网的业务系统中，涉及到各种各样的ID，如在支付系统中就会有支付ID、退款ID等。
<!--more-->
## 常见ID生成方案
### UUID
算法的核心思想是结合机器的网卡、当地时间、一个随记数来生成UUID。
* 优点：本地生成，生成简单，性能好，没有高可用风险
* 缺点：长度过长，存储冗余，且无序不可读，查询效率低

### 数据库自增ID
使用数据库的id自增策略，如 MySQL 的 auto_increment。并且可以使用两台数据库分别设置不同步长，生成不重复ID的策略来实现高可用。
* 优点：数据库生成的ID绝对有序，高可用实现方式简单
* 缺点：需要独立部署数据库实例，成本高，有性能瓶颈

### Redis生成ID
Redis的所有命令操作都是单线程的，本身提供像 incr 和 increby 这样的自增原子命令，所以能保证生成的 ID 肯定是唯一有序的。
* 优点：不依赖于数据库，灵活方便，且性能优于数据库；数字ID天然排序，对分页或者需要排序的结果很有帮助。
* 缺点：如果系统中没有Redis，还需要引入新的组件，增加系统复杂度；需要编码和配置的工作量比较大。

## 雪花算法原理
SnowFlake 算法，是 Twitter 开源的分布式 id 生成算法。

其核心思想就是：使用一个 64 bit 的 long 型的数字作为全局唯一 id。在分布式系统中的应用十分广泛，且ID 引入了时间戳，保持自增性且不重复。

![](http://image.runjf.com/mweb/2021-06-08-16231545423727.jpg)

主要分为 5 个部分：
1. 1 个 bit：0，无特殊意义，主要是为防止歧义，因为负数的第一位是1。
2. 41 个 bit：表示的是时间戳，毫秒值，可表示范围0到2^41-1。
3. 10 个 bit: 代表分区或者机器，可以表示范围0到1024
4. 12 个 bit：表示分区内的自增序号，可表示范围0到4096

所以理论上每秒可以生成`1000 * 1024 * 4096 = 4194304000`个id，完全足够使用

## Python 实现
有几个需要注意的点
- 系统时间可能会不准，要防止时间戳回拨
- 分区的10bit也可以进行二次分组，如前2bit代表机房，后8个bit代表机器
- 时间戳不一定要存储实际的时间戳，可以存储相对某个时间的变化，更节省空间

```Python
from time import time

MAX_WORKER = 2 ** 10 - 1
MAX_SEQ = 2 ** 12 - 1
TIME_OFFSET = 1577808000000  # datetime.datetime(2020, 1, 1, 0, 0)

class SnowFlake:
    def __init__(self, worker_id):
        assert 0 <= worker_id < MAX_WORKER
        self._worker_id = int(worker_id)
        self._timestamp = int(time() * 1000)
        self._seq = 0

    def get_id(self):
        res = 0
        res |= self._seq
        res |= (self._worker_id << 12)
        res |= ((self._timestamp - TIME_OFFSET) << 22)
        return res

    def next_id(self):
        t = int(time() * 1000)
        assert t >= self._timestamp
        assert self._seq < MAX_SEQ
        if t > self._timestamp:
            self._timestamp = t
            self._seq = 0
        else:
            self._seq += 1
        return self.get_id()

    @staticmethod
    def get_bin(val):
        return '{:0>64}'.format(bin(val)[2:])

if __name__ == '__main__':
    sf = SnowFlake(1)
    for _ in range(100):
        print(sf.get_bin(sf.next_id()), sf._timestamp, sf._seq)
```

## 参考
1. https://juejin.cn/post/6844903631137800200
2. https://www.cnblogs.com/wuzhenzhao/p/13295382.html