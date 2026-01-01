---
title: 限流算法之漏桶与令牌桶
date: 2021-05-30 10:48:00
updated: 2024-07-09 22:02:56
categories: 编程
tags: [限流, Python,]

---
后端一个常见且比较让人头疼的问题是服务限流，没有做好限流开始导致单个服务耗时增加，进而影响上下游服务，最终可能导致整个系统被拖垮。

限流的目的是通过对并发请求进行限速来保护系统，一旦达到限制速率则可以拒绝服务、排队 或等待、降级。
<!--more-->
一般使用的限流算法有漏桶（Leaky Bucket）和令牌桶(Token Bucket)。

这里有个需要注意的点，这两种算法的名称和示意图都是为了便于理解，实现时并不需要一模一样。

## 漏桶算法
漏桶作为计量工具（The Leaky Bucket Algorithm as a Meter )时，可以用于流量整形 (Traffic Shaping ) 和流量控制 （Traffic Policing )，漏桶算法的描述如下。

* 一个固定容量的漏桶，按照常量固定速率流出水滴。
* 如果桶是空的， 则不需流出水滴。
* 可以以任意速率流入水滴到漏桶。
* 如果流入水滴超出了桶的容量， 则流入的水滴溢出了（被丢弃）。

![-w962](https://image.ponder.work/mweb/2021-05-31-16223879750903.jpg)

漏桶的关键在于漏出速度恒定，超出的流量会被丢弃，最终请求看起来会是这样，峰值完全被砍掉了，过于粗暴了，适用的场景不多。
![-w1308](https://image.ponder.work/mweb/2021-05-31-16223889987592.jpg)

### 漏桶Python实现
网上常见的一种实现是用个队列直接存储请求来模拟漏桶，其实大可不必，内存空间占用大而且效率低。

其实只需要通过一个队列记录请求时间，结合漏桶漏出速率进行计算，然后移动窗口就可以实现漏桶了。

这里的实现对漏桶进行了简化，漏桶的容量恰好等于单位时间漏出的量。

```Python
from time import time, sleep
from collections import deque

class LeakyBucket(object):
    def __init__(self, leaky_rate):
        self.leaky_rate = float(leaky_rate)    # 漏出速度
        self._que = []   # 请求时间队列

    def size(self):
        return len(self._que)

    def inspect_expired_items(self, time: int):
        """检查已经漏出的请求
        args:
            time: 上一个时间窗口, 默认是秒
        returns:
            item_count: 已漏出的请求个数
            remaining_time: 第一个未漏出请求的剩余时间
        """
        volume = self.size()
        item_count, remaining_time = 0, 0

        for log_idx, log_item in enumerate(self._que):
            if log_item > time:
                item_count = volume - log_idx
                remaining_time = log_item - time
                break
        return item_count, remaining_time

    def acquire(self, block=True):
        """
        args:
            block: 是否阻塞直到可以请求
        returns:
            - 是否可以请求
        """

        now = time()
        volume = self.size()
        if volume >= self.leaky_rate:   # 容量已满需要清理已漏出请求
            pre_tick = now - 1  # 上一个时间窗口, 默认单位为秒
            item_count, remaining_time = self.inspect_expired_items(pre_tick)
            if item_count >= self.leaky_rate:   # 上个周期请求已超限
                if block:
                    sleep(remaining_time)   # 等到出现一个空位
                    print('Bucket Full, sleep {} seconds'.format(remaining_time))
                    return self.acquire()   # 再次尝试
                return False
            self._que[:volume-item_count] = []    # 清除上个周期数据
        self._que.append(now)
        return True

if __name__ == '__main__':
    rate_limiter = LeakyBucket(2)
    for i in range(10):
        if rate_limiter.acquire(block=False):
            print(time(), 'succ', i)
        else:
            print(time(), 'skip', i)
        sleep(0.2)

```

## 令牌桶
令牌桶算法，是一个存放固定容量令牌的桶，按照固定速率往桶里添加令牌。

令牌桶算法的描述如下。
- 假设限制2r/s ，则按照500毫秒的固定速率往桶中添加令牌。
- 桶中最多存放b个令牌， 当桶满时，新添加的令牌被丢弃或拒绝。
- 当一个n个字节的数据包到达，将从桶中删除n个令牌，然后发送请求
- 如果桶中的令牌不足n个，则该数据包将被限流（要么丢弃， 要么在缓冲区等待）。

![-w846](https://image.ponder.work/mweb/2021-05-31-16223906628083.jpg)

由于令牌放置速度恒定，取出速度不限，所以令牌桶的限流是有一定弹性的，能够接受请求的一定波动。

![-w1288](https://image.ponder.work/mweb/2021-05-31-16223908269384.jpg)

### 令牌桶Python实现
通过计算令牌桶容量和产生速率就可以实现令牌桶，并不需要真的实现“把令牌放桶里”和“取出令牌”。

```Python
from time import time, sleep

class TokenBucket(object):
    def __init__(self, tokens, fill_rate):
        self.capacity = float(tokens)   # 容量
        self._tokens = float(tokens)
        self.fill_rate = float(fill_rate)    # 产生速度
        self.timestamp = time()

    def consume(self, tokens, block=True):
        assert tokens <= self.capacity, 'Attempted to consume {} tokens from a bucket with capacity {}'.format(tokens, self.capacity)

        if block and tokens > self.tokens:
            deficit = tokens - self._tokens
            delay = deficit / self.fill_rate
            print('Have {} tokens, need {}; sleeping {} seconds'.format(self._tokens, tokens, delay))
            sleep(delay)

        if tokens <= self.tokens:
            self._tokens -= tokens
            return True
        else:
            return False

    @property
    def tokens(self):
        if self._tokens < self.capacity:
            now = time()   # 获取当前时间
            delta = self.fill_rate * (now - self.timestamp)   # 算出这段时间产出的令牌
            self._tokens = min(self.capacity, self._tokens + delta)   # 丢弃超出容量的令牌
            self.timestamp = now   # 更新基准时间
        return self._tokens


def rate_limit(data, bandwidth_or_burst, steady_state_bandwidth=None):
    # bandwidth_or_burst 令牌桶容量
    # steady_state_bandwidth 令牌产生速度
    bandwidth = steady_state_bandwidth or bandwidth_or_burst
    rate_limiter = TokenBucket(bandwidth_or_burst, bandwidth)

    for thing in data:
        rate_limiter.consume(len(str(thing)))
        yield thing


if __name__ == '__main__':
    stream = rate_limit(range(10), 5, 1)
    for i in stream:
        print(time(), i)
```

注意：以上算法都是单机单线程的实现，如果需要多个机器限流则需要将桶的状态通过redis等外部服务来存储。

## 令牌桶和漏桶算法对比
- 令牌桶是按照**固定速率往桶中添加令牌**，请求是否被处理需要看桶中令牌是否足够，当令牌数减为零时，则拒绝新的请求。
- 漏桶则是按照**固定速率流出请求**，流入请求速率任意，当流入的请求数累积到漏桶容量时，则新流入的请求被拒绝。
- 令牌桶限制的是平均流入速率（允许突发请求，只要有令牌就可以处理，支持一次拿3个令牌，或4个令牌）， 并允许一定程度的突发流量。
- 漏桶限制的是常量流出速率（即流出速率是一个固定常量值，比如都是1的速率流出，而不能一次是1，下次又是2) , 从而平滑突发流入速率。
- 令牌桶允许一定程度的突发，而漏桶主要目的是平滑流入速率。

## 参考
- 《亿级流量网站架构核心技术》
- https://github.com/vutran1710/PyrateLimiter
- https://gist.github.com/drocco007/6155452
- https://vim0.com/post/interview/
